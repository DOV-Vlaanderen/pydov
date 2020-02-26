# -*- coding: utf-8 -*-
"""Module implementing a simple hooks system to allow late-binding actions to
PyDOV events."""

from multiprocessing import Lock

import sys
import time

import pydov


class Hooks(list):
    """Runtime representation of registered pydov hooks, i.e. a list of
    instances of AbstractReadHook and/or AbstractInjectHook."""
    def get_read_hooks(self):
        """Get the registered read hooks (i.e. hooks that are subclasses of
        AbstractReadHook), in the order they are defined in the list.

        Returns
        -------
        tuple of AbstractReadHook
            A tuple with the registered read hooks.

        """
        return (h for h in self if isinstance(h, AbstractReadHook))

    def get_inject_hooks(self):
        """Get the registered inject hooks (i.e. hooks that are subclasses of
        AbstractInjectHook), in the order they are defined in the list.

        Returns
        -------
        tuple of AbstractInjectHook
            A tuple with the registered inject hooks.

        """
        return (h for h in self if isinstance(h, AbstractInjectHook))


class HookRunner(object):
    """Class for executing registered hooks."""
    @staticmethod
    def __execute_read(hook_name, args):
        """Execute the read hook with the given name for all registered hooks.

        Parameters
        ----------
        hook_name : str
            Name of the hook function to execute.
        args : list
            List of arguments to pass to the hook function call.

        """
        for h in pydov.hooks.get_read_hooks():
            getattr(h, hook_name)(*args)

    @staticmethod
    def __execute_inject(hook_name, args):
        """Execute the inject hook with given name for all registered hooks
        and return the last non-null result.

        Parameters
        ----------
        hook_name : str
            Name of the hook function to execute.
        args : list
            List of arguments to pass to the hook function call.

        Returns
        -------
        object or bytes or None
            Returns the last non-null result of the execution of the inject
            hook. If all inject hooks return None, return None as well.

        """
        result = None
        for h in pydov.hooks.get_inject_hooks():
            r = getattr(h, hook_name)(*args)
            if r is not None:
                result = r
        return result

    @staticmethod
    def execute_meta_received(url, response):
        """Execute the meta_received method for all registered hooks.

        Parameters
        ----------
        url : str
            URL of the metadata request.
        response : bytes
            The raw response as received from resolving the URL.

        """
        HookRunner.__execute_read('meta_received', [url, response])

    @staticmethod
    def execute_wfs_search_init(typename):
        """Execute the wfs_search_init method for all registered hooks.

        Parameters
        ----------
        typename : str
            The typename (layername) of the WFS service used for searching.

        """
        HookRunner.__execute_read('wfs_search_init', [typename])

    @staticmethod
    def execute_wfs_search_result(number_of_results):
        """Execute the wfs_search_result method for all registered hooks.

        Parameters
        ----------
        number_of_results : int
            The number of features returned by the WFS search.

        """
        HookRunner.__execute_read('wfs_search_result', [number_of_results])

    @staticmethod
    def execute_wfs_search_result_received(query, features):
        """Execute the wfs_search_result_received method for all registered
        hooks.

        Parameters
        ----------
        query : etree.ElementTree
            The WFS GetFeature request sent to the WFS server.
        features : etree.ElementTree
            The WFS GetFeature response containings the features.

        """
        HookRunner.__execute_read('wfs_search_result_received', [
            query, features])

    @staticmethod
    def execute_xml_received(pkey_object, xml):
        """Execute the xml_received method for all registered hooks.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the retrieved object.
        xml : bytes
            The raw XML data of this DOV object as bytes.

        """
        HookRunner.__execute_read('xml_received', [pkey_object, xml])

    @staticmethod
    def execute_xml_cache_hit(pkey_object):
        """Execute the xml_cache_hit method for all registered hooks.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        HookRunner.__execute_read('xml_cache_hit', [pkey_object])

    @staticmethod
    def execute_xml_downloaded(pkey_object):
        """Execute the xml_downloaded method for all registered hooks.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        HookRunner.__execute_read('xml_downloaded', [pkey_object])

    @staticmethod
    def execute_inject_meta_response(url):
        """Execute the inject_meta_response method for all registered hooks.

        Parameters
        ----------
        url : str
            URL of the metadata request.

        Returns
        -------
        bytes, optional
            The response to use in favor of resolving the URL. Returns None if
            this inject hook is unused.

        """
        return HookRunner.__execute_inject(
            'inject_meta_response', [url])

    @staticmethod
    def execute_inject_wfs_getfeature_response(query):
        """Execute the inject_wfs_getfeature_response method for all
        registered hooks.

        Parameters
        ----------
        query : etree.ElementTree
            The WFS GetFeature request sent to the WFS server.

        Returns
        -------
        xml: bytes, optional
            The GetFeature response to use in favor of resolving the URL.
            Returns None if this inject hook is unused.

        """
        return HookRunner.__execute_inject(
            'inject_wfs_getfeature_response', [query])

    @staticmethod
    def execute_inject_xml_response(pkey_object):
        """Execute the inject_xml_response method for all registered hooks.

        Parameters
        ----------
        query : etree.ElementTree
            The WFS GetFeature request sent to the WFS server.

        Returns
        -------
        xml : bytes, optional
            The XML response to use in favor of resolving the URL. Returns
            None if this inject hook is unused.

        """
        return HookRunner.__execute_inject(
            'inject_xml_response', [pkey_object])


class AbstractReadHook(object):
    """Abstract base class for custom hook implementations.

    This class contains all read-only hooks: i.e. hooks receiving events but
    otherwise not interfering with pydov's execution stack.

    Provides all available methods with a default implementation to do
    nothing. This allows for hook subclasses to only implement the events
    they need.

    """
    def meta_received(self, url, response):
        """Called when a response for a metadata requests is received.

        Metadata calls include amongst others: WFS GetCapabilities, requests
        for MD_Metadata, FC_FeatureCatalogue and XSD schemas.

        These are all calls except for WFS GetFeature requests and XML
        downloads of DOV data - these are other hooks.

        Parameters
        ----------
        url : str
            URL of the metadata request.
        response : bytes
            The raw response as received from resolving the URL.

        """
        pass

    def wfs_search_init(self, typename):
        """Called upon starting a WFS search.

        Parameters
        ----------
        typename : str
            The typename (layername) of the WFS service used for searching.

        """
        pass

    def wfs_search_result(self, number_of_results):
        """Called after a WFS search finished.

        Parameters
        ----------
        number_of_results : int
            The number of features returned by the WFS search.

        """
        pass

    def wfs_search_result_received(self, query, features):
        """Called after a WFS search finished.

        Includes both the GetFeature query as well as the response from the
        WFS server.

        Parameters
        ----------
        query : etree.ElementTree
            The WFS GetFeature request sent to the WFS server.
        features : etree.ElementTree
            The WFS GetFeature response containings the features.

        """
        pass

    def xml_received(self, pkey_object, xml):
        """Called when the XML of a given object is received, either from
        the cache or from the remote DOV service.

        Includes the permanent key of the DOV object as well as the full XML
        representation.

        Because of parallel processing, this method will be called
        simultaneously from multiple threads. Make sure your implementation is
        threadsafe or uses locking.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the retrieved object.
        xml : bytes
            The raw XML data of this DOV object as bytes.

        """
        pass

    def xml_cache_hit(self, pkey_object):
        """Called when the XML document of an object is retrieved from the
        cache.

        Because of parallel processing, this method will be called
        simultaneously from multiple threads. Make sure your implementation is
        threadsafe or uses locking.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        pass

    def xml_downloaded(self, pkey_object):
        """Called when the XML document of an object is downloaded from the
        DOV services.

        Because of parallel processing, this method will be called
        simultaneously from multiple threads. Make sure your implementation is
        threadsafe or uses locking.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        pass


class AbstractInjectHook(object):
    """Abstract base class for custom hook implementations.

    This class contains all inject hooks: i.e. hooks receiving events and
    possibly returning custom data for injection into pydov's execution stack.

    Inject hooks allow you to capture and intercept remote server calls,
    influencing pydov's inner workings. Use with care! If you reached this
    part of the code, it is probably wise to open an issue in Github,
    since this is most likely not what you need.

    Provides all available methods with a default implementation to do
    nothing. This allows for hook subclasses to only implement the events
    they need.

    """
    def inject_meta_response(self, url):
        """Inject a response for a metadata request.

        This allows to intercept a metadata request and return a response of
        your choice.

        When at least one registered hook returns a response for a given URL,
        the remote call is not executed and instead the response from the
        last registered hook (that is non-null) is used instead.

        Metadata calls include amongst others: WFS GetCapabilities, requests
        for MD_Metadata, FC_FeatureCatalogue and XSD schemas.

        These are all calls except for WFS GetFeature requests and XML
        downloads of DOV data - these are other hooks.

        Parameters
        ----------
        url : str
            URL of the metadata request.

        Returns
        -------
        bytes, optional
            The response to use in favor of resolving the URL. Return None to
            disable this inject hook.

        """
        return None

    def inject_wfs_getfeature_response(self, query):
        """Inject a response for a WFS GetFeature request.

        This allows to intercept a WFS GetFeature request and return a
        response of your choice.

        When at least one registered hook returns a response for a given query,
        the remote call is not executed and instead the response from the
        last registered hook (that is non-null) is used instead.

        Parameters
        ----------
        query : etree.ElementTree
            The WFS GetFeature request sent to the WFS server.

        Returns
        -------
        xml: bytes, optional
            The GetFeature response to use in favor of resolving the URL.
            Return None to disable this inject hook.

        """
        return None

    def inject_xml_response(self, pkey_object):
        """Inject a response for a DOV XML request.

        This allows to intercept a DOV XML request and return a response of
        your choice.

        When at least one registered hook returns a response for a given pkey,
        the remote call is not executed and instead the response from the
        last registered hook (that is non-null) is used instead.

        Because of parallel processing, this method will be called
        simultaneously from multiple threads. Make sure your implementation is
        threadsafe or uses locking.

        Parameters
        ----------
        query : etree.ElementTree
            The WFS GetFeature request sent to the WFS server.

        Returns
        -------
        xml : bytes, optional
            The XML response to use in favor of resolving the URL. Return
            None to disable this inject hook.

        """
        return None


class SimpleStatusHook(AbstractReadHook):
    """Simple hook implementation to print progress to stdout."""
    def __init__(self):
        """Initialisation.

        Initialise all variables to 0.

        """
        self.result_count = 0
        self.prog_counter = 0
        self.init_time = None
        self.previous_remaining = None
        self.lock = Lock()

    def _write_progress(self, char):
        """Write progress to standard output.

        Progress is grouped on lines per 50 items, adding ``char`` for every
        item processed.

        Parameters
        ----------
        char : str
            Single character to print.

        """
        if self.prog_counter == 0:
            sys.stdout.write('[{:03d}/{:03d}] '.format(
                self.prog_counter, self.result_count))
            sys.stdout.flush()
        elif self.prog_counter % 50 == 0:
            time_elapsed = time.time() - self.init_time
            time_per_item = time_elapsed/self.prog_counter
            remaining_mins = int((time_per_item*(
                self.result_count-self.prog_counter))/60)
            if remaining_mins > 1 and remaining_mins != \
                    self.previous_remaining:
                remaining = " ({:d} min. left)".format(remaining_mins)
                self.previous_remaining = remaining_mins
            else:
                remaining = ""
            sys.stdout.write('{}\n[{:03d}/{:03d}] '.format(
                remaining, self.prog_counter, self.result_count))
            sys.stdout.flush()

        sys.stdout.write(char)
        sys.stdout.flush()
        self.prog_counter += 1

        if self.prog_counter == self.result_count:
            sys.stdout.write('\n')
            sys.stdout.flush()

    def wfs_search_init(self, typename):
        """When a new WFS search is started, reset all counters to 0.

        Parameters
        ----------
        typename : str
            The typename (layername) of the WFS service used for searching.

        """
        self.result_count = 0
        self.prog_counter = 0
        self.init_time = time.time()
        self.previous_remaining = None

    def wfs_search_result(self, number_of_results):
        """When the WFS search completes, set the total result count to
        ``number_of_results``.

        Parameters
        ----------
        number_of_results : int
            The number of features returned by the WFS search.

        """
        self.result_count = number_of_results

    def xml_cache_hit(self, pkey_object):
        """When an XML document is retrieved from the cache, print 'c' to
        the progress output.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        with self.lock:
            self._write_progress('c')

    def xml_downloaded(self, pkey_object):
        """When an XML document is downloaded from the DOV services,
        print '.' to the progress output.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        with self.lock:
            self._write_progress('.')
