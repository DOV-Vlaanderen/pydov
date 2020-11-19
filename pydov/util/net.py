from queue import Empty, Queue
from threading import Thread

import requests
import urllib3
from requests.adapters import HTTPAdapter

import pydov

request_timeout = 300


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = request_timeout
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class SessionFactory:
    @staticmethod
    def get_session():
        session = requests.Session()

        session.headers.update(
            {'user-agent': 'pydov/{}'.format(pydov.__version__)})

        try:
            retry = urllib3.util.Retry(
                total=10, connect=10, read=10, redirect=5, backoff_factor=1,
                allowed_methods=set(['GET', 'POST']))
        except TypeError:
            retry = urllib3.util.Retry(
                total=10, connect=10, read=10, redirect=5, backoff_factor=1,
                method_whitelist=set(['GET', 'POST']))

        adapter = TimeoutHTTPAdapter(timeout=request_timeout,
                                     max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session


class LocalSessionThreadPool:
    def __init__(self, workers=4):
        self.workers = []
        self.input_queue = Queue(maxsize=100)
        self.result_queue = Queue()

        for i in range(workers):
            self.workers.append(
                LocalSessionThread(self.input_queue, self.result_queue))

        self.start()

    def start(self):
        for w in self.workers:
            w.start()

    def stop(self):
        for w in self.workers:
            w.stop()

    def execute(self, fn, args):
        r = WorkerResult()
        self.input_queue.put((fn, args, r))
        self.result_queue.put(r)

    def join(self):
        self.input_queue.join()
        self.stop()

        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get().get_result())
        return results


class WorkerResult:
    def __init__(self):
        self.result = None

    def set_result(self, value):
        self.result = value

    def get_result(self):
        return self.result


class LocalSessionThread(Thread):
    def __init__(self, input_queue, result_queue):
        super().__init__()
        self.input_queue = input_queue
        self.result_queue = result_queue

        self.stopping = False
        self.session = SessionFactory.get_session()

    def stop(self):
        self.stopping = True

    def run(self):
        while not self.stopping:
            try:
                fn, args, r = self.input_queue.get(timeout=0.5)
                args = list(args)
                args.append(self.session)
                result = fn(*args)
                r.set_result(result)
                self.input_queue.task_done()
            except Empty:
                pass
