# -*- coding: utf-8 -*-
"""Module grouping network-related utilities and functions."""

import os
from queue import Empty, Queue
from threading import Thread

import requests
import urllib3
from requests.adapters import HTTPAdapter

import pydov

request_timeout = 300


def proxy_autoconfiguration():
    """Try proxy autoconfiguration via PAC.

    This function tries to autodetect the required proxy server using PAC, and
    sets the HTTP_PROXY and HTTPS_PROXY environment variables accordingly.

    These variables should subsequently be picked up by the requests sessions
    used by pydov and owslib.
    """
    def get_orig_proxy():
        """Get the proxy from current environment, if available.

        Returns
        -------
        tuple(str, str)
            The HTTP and HTTPS proxy respectively.
        """
        return (os.environ.get('HTTP_PROXY', None),
                os.environ.get('HTTPS_PROXY', None))

    def set_proxy_for_url(url):
        """Use PAC to discover the required proxy for the given URL and
        set the environment accordingly.

        Parameters
        ----------
        url : str
            The URL to pass to the PAC to determine the required proxy.
        """
        with pypac.pac_context_for_url(url):
            http_proxy = os.environ.get("HTTP_PROXY", "")
            https_proxy = os.environ.get("HTTPS_PROXY", "")

        os.environ['HTTP_PROXY'] = http_proxy
        os.environ['HTTPS_PROXY'] = https_proxy

    def revert_to_orig_proxy(orig_http_proxy, orig_https_proxy):
        """Revert the proxy environment to the given values.

        Parameters
        ----------
        orig_http_proxy : str
            Proxy server to use for HTTP, or None to disable.
        orig_https_proxy : str
            Proxy server to use for HTTPS, ot None to disable.
        """
        if orig_http_proxy is None:
            del os.environ['HTTP_PROXY']
        else:
            os.environ['HTTP_PROXY'] = orig_http_proxy

        if orig_https_proxy is None:
            del os.environ['HTTPS_PROXY']
        else:
            os.environ['HTTPS_PROXY'] = orig_https_proxy

    try:
        import pypac
    except ImportError:
        # do nothing if PAC not available
        pass
    else:
        # save original proxy from environment
        orig_http_proxy, orig_https_proxy = get_orig_proxy()

        from pydov.util.dovutil import build_dov_url
        dov_url = build_dov_url('/')
        public_url = 'https://pydov.readthedocs.io'

        # set proxy using PAC for DOV URL
        set_proxy_for_url(dov_url)
        try:
            # try if it works
            r = requests.get(dov_url)
            if not r.ok:
                raise RuntimeError
        except Exception:
            # fallback

            # set proxy using PAC for a public URL
            set_proxy_for_url(public_url)
            try:
                # try if it works
                r = requests.get(dov_url)
                if not r.ok:
                    raise RuntimeError
            except Exception:
                # if it does not, revert to original environment
                revert_to_orig_proxy(orig_http_proxy, orig_https_proxy)


class TimeoutHTTPAdapter(HTTPAdapter):
    """HTTPAdapter which adds a default timeout to requests. Allows timeout
    to be overridden on a per-request basis.
    """

    def __init__(self, *args, **kwargs):
        """Initialisation."""
        self.timeout = request_timeout
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        """Sends PreparedRequest object. Returns Response object.

        Parameters
        ----------
        request : requests.PreparedRequest
            The PreparedRequest being sent.

        Returns
        -------
        requests.Response
            The Response of the request.
        """
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class SessionFactory:
    """Class for generating pydov configured requests Sessions. They are used
    to send HTTP requests using our user-agent and with added retry-logic.

    One global session is used for all requests, and additionally one
    session is used per thread executing XML requests in parallel.
    """

    @staticmethod
    def get_session():
        """Request a new session.

        Returns
        -------
        requests.Session
            pydov configured requests Session.
        """
        session = requests.Session()

        session.headers.update(
            {'user-agent': 'pydov/{}'.format(pydov.__version__)})

        try:
            retry = urllib3.util.Retry(
                total=10, connect=10, read=10, redirect=5, backoff_factor=1,
                allowed_methods=set(
                    ['HEAD', 'GET', 'POST', 'PUT', 'OPTIONS']))
        except TypeError:
            # urllib3 < 1.26.0 used method_whitelist instead
            retry = urllib3.util.Retry(
                total=10, connect=10, read=10, redirect=5, backoff_factor=1,
                method_whitelist=set(
                    ['HEAD', 'GET', 'POST', 'PUT', 'OPTIONS']))

        adapter = TimeoutHTTPAdapter(timeout=request_timeout,
                                     max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session


class LocalSessionThreadPool:
    """Thread pool of LocalSessionThreads used to perform HTTP I/O operations
    in parallel.
    """

    def __init__(self, workers=4):
        """Initialisation.

        Set up the pool and start all workers.

        Parameters
        ----------
        workers : int, optional
            Number of worker threads to use, defaults to 4.
        """
        self.workers = []
        self.input_queue = Queue(maxsize=100)
        self.result_queue = Queue()

        for i in range(workers):
            self.workers.append(LocalSessionThread(self.input_queue))

        self._start()

    def _start(self):
        """Start all worker threads. """
        for w in self.workers:
            w.start()

    def stop(self):
        """Stop all worker threads. """
        for w in self.workers:
            w.stop()

    def execute(self, fn, args):
        """Execute the given function with its arguments in a worker thread.

        This will add the job to the queue and will not wait for the result.
        Use join() to retrieve the result.

        Parameters
        ----------
        fn : function
            Function to execute. It should take all arguments from args, and
            after that a single argument with the requests Session.
        args : tuple
            Arguments that will be passed to the function.
        """
        r = WorkerResult()
        self.input_queue.put((fn, args, r))
        self.result_queue.put(r)

    def join(self):
        """Wait for all the jobs to be executed and return the results of all
        jobs in a list.

        Yields
        ------
        WorkerResult
            Results of the executed functions in the order they were
            submitted.
        """
        self.input_queue.join()
        self.stop()

        while not self.result_queue.empty():
            yield self.result_queue.get()


class WorkerResult:
    """Class for storing the result of a job execution in the result queue.

    This allows putting a result instance in the queue on job submission and
    fill in the result later when the job completes. This ensures the result
    output is in the same order as the jobs were submitted.
    """

    def __init__(self):
        """Initialisation. """
        self.result = None
        self.error = None

    def set_result(self, value):
        """Set the result of this job.

        Parameters
        ----------
        value : any
            The result of the execution of the job.
        """
        self.result = value

    def get_result(self):
        """Retrieve the result of this job.

        Returns
        -------
        any
            The result of the execution of the job.
        """
        return self.result

    def set_error(self, error):
        """Set the error, in case the jobs fails with an exception.

        Parameters
        ----------
        error : Exception
            The exception raised while executing this job.
        """
        self.error = error

    def get_error(self):
        """Retrieve the error, if any, of this job.

        Returns
        -------
        Exception
            The exception raised while executing this job.
        """
        return self.error


class LocalSessionThread(Thread):
    """Worker thread using a local Session to execute functions. """

    def __init__(self, input_queue):
        """Initialisation.

        Bind to the input queue and create a Session.

        Parameters
        ----------
        input_queue : queue.Queue
            Queue to poll for input, this should be in the form of a tuple with
            3 items: function to call, list with arguments and WorkerResult
            instance to store the output. The list with arguments will be
            automatically extended with the local Session instance.
        """
        super().__init__()
        self.input_queue = input_queue

        self.stopping = False
        self.session = SessionFactory.get_session()

    def stop(self):
        """Stop the worker thread at the next occasion. This can take up to
        500 ms. """
        self.stopping = True

    def run(self):
        """Executed while the thread is running. This is called implicitly
        when starting the thread. """
        while not self.stopping:
            try:
                fn, args, r = self.input_queue.get(timeout=0.5)
                args = list(args)
                args.append(self.session)

                try:
                    result = fn(*args)
                except BaseException as e:
                    r.set_error(e)
                else:
                    r.set_result(result)
                finally:
                    self.input_queue.task_done()
            except Empty:
                pass
