# -*- coding: utf-8 -*-
"""Module implementing a simple hooks system to allow late-binding actions to
PyDOV events."""

from multiprocessing import Lock

import sys
import time


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


class AbstractReadHook(object):
    """Abstract base class for custom hook implementations.

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
