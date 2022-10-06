# -*- coding: utf-8 -*-
"""Module implementing a simple hooks system to allow late-binding actions to
PyDOV events."""

from hashlib import md5
import importlib
from multiprocessing import Lock
from owslib.etree import etree
from pathlib import Path
import atexit
import json
import math
import os
import sys
import time
import uuid
import zipfile

import pydov
from pydov.util.errors import LogReplayError


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
    def execute_wfs_search_init(params):
        """Execute the wfs_search_init method for all registered hooks.

        Parameters
        ----------
        params : dict
            Parameters used to initiate WFS search. These include:
                typename : str
                    Typename in the WFS service to query.
                location : pydov.util.location.AbstractLocationFilter or None
                    Location filter limiting the features to retrieve.
                filter : str (xml) or None
                    Attribute filter limiting the features to retrieve.
                sort_by : str (xml) or None
                    SortBy clause listing fields to sort by.
                max_features : int
                    Limit the maximum number of features to request.
                propertynames : list of str
                    List of WFS propertynames (attributes) to retrieve.
                geometry_column : str
                    Name of the column/attribute containing the geometry.

        """
        HookRunner.__execute_read('wfs_search_init', [params])

    @staticmethod
    def execute_wfs_search_result(number_matched, number_returned):
        """Execute the wfs_search_result method for all registered hooks.

        Parameters
        ----------
        number_matched : int
            The number of features matched by the WFS search query.
        number_returned : int
            The number of features returned by the WFS search query. Due to
            server limitations this can be less than number_matched.

        """
        HookRunner.__execute_read(
            'wfs_search_result', [number_matched, number_returned])

    @staticmethod
    def execute_wfs_search_result_received(query, features):
        """Execute the wfs_search_result_received method for all registered
        hooks.

        Parameters
        ----------
        query : etree.ElementTree
            The WFS GetFeature request sent to the WFS server.
        features : etree.ElementTree
            The WFS GetFeature response containing the features.

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
    def execute_xml_stale_hit(pkey_object):
        """Execute the xml_stale_hit method for all registered hooks.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        HookRunner.__execute_read('xml_stale_hit', [pkey_object])

    @staticmethod
    def execute_xml_fetch_error(pkey_object):
        """Execute the xml_fetch_error method for all registered hooks.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        HookRunner.__execute_read('xml_fetch_error', [pkey_object])

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

    def wfs_search_init(self, params):
        """Called upon starting a WFS search.

        Parameters
        ----------
        params : dict
            Parameters used to initiate WFS search. These include:
                typename : str
                    Typename in the WFS service to query.
                location : pydov.util.location.AbstractLocationFilter or None
                    Location filter limiting the features to retrieve.
                filter : str (xml) or None
                    Attribute filter limiting the features to retrieve.
                sort_by : str (xml) or None
                    SortBy clause listing fields to sort by.
                max_features : int
                    Limit the maximum number of features to request.
                propertynames : list of str
                    List of WFS propertynames (attributes) to retrieve.
                geometry_column : str
                    Name of the column/attribute containing the geometry.

        """
        pass

    def wfs_search_result(self, number_matched, number_returned):
        """Called after a WFS search query finished.

        Because of parallel processing, this method will be called
        simultaneously from multiple threads. Make sure your implementation is
        threadsafe or uses locking.

        Parameters
        ----------
        number_matched : int
            The number of features matched by the WFS search query.
        number_returned : int
            The number of features returned by the WFS search query. Due to
            server limitations this can be less than number_matched.

        """
        pass

    def wfs_search_result_received(self, query, features):
        """Called after a WFS search finished.

        Includes both the GetFeature query as well as the response from the
        WFS server.

        Because of parallel processing, this method will be called
        simultaneously from multiple threads. Make sure your implementation is
        threadsafe or uses locking.

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

    def xml_stale_hit(self, pkey_object):
        """Called when the XML document of an object failed to be retrieved
        from the DOV service and a stale version has been returned from the
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

    def xml_fetch_error(self, pkey_object):
        """Called when the XML document of an object failed to be retrieved
        from the DOV service and no stale version could be returned from the
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

        Because of parallel processing, this method will be called
        simultaneously from multiple threads. Make sure your implementation is
        threadsafe or uses locking.

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

    class ProgressState(object):
        """Simple class for storing progress state.
        """

        def __init__(self):
            """Initialise a new progress state, with all variable to default.
            """
            self.reset()

        def reset(self):
            """Reset the progress state. Resets all variables to default."""
            self.max_results = None
            self.result_count = 0
            self.prog_counter = 0
            self.init_time = time.time()
            self.previous_remaining = None

    def __init__(self):
        """Initialisation.

        Initialise all variables to default.

        """
        self.wfs_progress = SimpleStatusHook.ProgressState()
        self.xml_progress = SimpleStatusHook.ProgressState()
        self.lock = Lock()

    def _write_progress(self, state, char):
        """Write progress to standard output.

        Progress is grouped on lines per 50 items, adding ``char`` for every
        item processed.

        Parameters
        ----------
        state : ProgressState
            State of current progress.
        char : str
            Single character to print.

        """
        if state.prog_counter == 0:
            sys.stdout.write('[{:03d}/{:03d}] '.format(
                state.prog_counter, state.result_count))
            sys.stdout.flush()
        elif state.prog_counter % 50 == 0:
            time_elapsed = time.time() - state.init_time
            time_per_item = time_elapsed / state.prog_counter
            remaining_mins = int((time_per_item * (
                state.result_count - state.prog_counter)) / 60)
            if remaining_mins > 1 and remaining_mins != \
                    state.previous_remaining:
                remaining = " ({:d} min. left)".format(remaining_mins)
                state.previous_remaining = remaining_mins
            else:
                remaining = ""
            sys.stdout.write('{}\n[{:03d}/{:03d}] '.format(
                remaining, state.prog_counter, state.result_count))
            sys.stdout.flush()

        sys.stdout.write(char)
        sys.stdout.flush()
        state.prog_counter += 1

        if state.prog_counter == state.result_count:
            sys.stdout.write('\n')
            sys.stdout.flush()

    def wfs_search_init(self, params):
        """When a new WFS search is started, reset all counters to 0 and set
        the maximum requested results.

        Parameters
        ----------
        params : dict
            Parameters used to initiate WFS search. These include:
                typename : str
                    Typename in the WFS service to query.
                location : pydov.util.location.AbstractLocationFilter or None
                    Location filter limiting the features to retrieve.
                filter : str (xml) or None
                    Attribute filter limiting the features to retrieve.
                sort_by : str (xml) or None
                    SortBy clause listing fields to sort by.
                max_features : int or None
                    Limit the maximum number of features to request.
                propertynames : list of str
                    List of WFS propertynames (attributes) to retrieve.
                geometry_column : str
                    Name of the column/attribute containing the geometry.

        """
        self.wfs_progress.reset()
        self.xml_progress.reset()

        self.wfs_progress.max_results = params.get('max_features', None)
        self.xml_progress.max_results = params.get('max_features', None)

    def wfs_search_result(self, number_matched, number_returned):
        """When the WFS search completes, set the total result count.

        Parameters
        ----------
        number_matched : int
            The number of features matched by the WFS search query.
        number_returned : int
            The number of features returned by the WFS search query. Due to
            server limitations this can be less than number_matched.

        """
        if self.wfs_progress.result_count == 0:

            if self.wfs_progress.max_results is not None:
                total_results = min(
                    self.wfs_progress.max_results, number_matched)
            else:
                total_results = number_matched

            if number_returned > 0:
                self.wfs_progress.result_count = math.ceil(
                    total_results/number_returned)
            else:
                self.wfs_progress.result_count = 0

            self.xml_progress.result_count = total_results

        self._write_progress(self.wfs_progress, '.')

    def xml_cache_hit(self, pkey_object):
        """When an XML document is retrieved from the cache, print 'c' to
        the progress output.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        with self.lock:
            self._write_progress(self.xml_progress, 'c')

    def xml_stale_hit(self, pkey_object):
        """When a stale XML document is retrieved from the cache, print 'S' to
        the progress output.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        with self.lock:
            self._write_progress(self.xml_progress, 'S')

    def xml_fetch_error(self, pkey_object):
        """When an XML document failed to be fetched from DOV, print 'E' to
        the progress output.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        with self.lock:
            self._write_progress(self.xml_progress, 'E')

    def xml_downloaded(self, pkey_object):
        """When an XML document is downloaded from the DOV services,
        print '.' to the progress output.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        with self.lock:
            self._write_progress(self.xml_progress, '.')


class RepeatableLogRecorder(AbstractReadHook, AbstractInjectHook):
    """Class for recording a pydov session into a ZIP archive.

    This enables to save (the results of) all metadata and data requests from
    the DOV services locally on disk.

    The saved ZIP archive can subsequently be used in the
    `RepeatableLogReplayer` to replay the saved session allowing fully
    reproducible pydov runs.

    """

    def __init__(self, log_directory):
        """Initialise a RepeatableLogRecorder hook.

        It will save a ZIP archive with the current pydov session's data in
        the given log directory.

        Replays previously saved responses in the current session too to
        enable full reproducibility between the session being saved and replays
        of the saved ZIP archive. When this would be omitted they would not
        necessarily yield the same results due to timing issues (albeit
        quite far fetched).

        Parameters
        ----------
        log_directory : str
            Path to a directory on disk where the ZIP archive containing the
            pydov session will be saved. Will be created if it does not exist.

        """
        self.log_directory = log_directory

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        self.log_archive = os.path.join(
            self.log_directory,
            time.strftime('pydov-archive-%Y%m%dT%H%M%S-{}.zip'.format(
                str(uuid.uuid4())[0:6]))
        )

        self.log_archive_file = zipfile.ZipFile(
            self.log_archive, 'w', compression=zipfile.ZIP_DEFLATED)

        self.metadata = {
            'versions': dict([m, self._safe_get_version(m)] for m in [
                'pydov', 'owslib', 'pandas', 'numpy', 'requests',
                'fiona', 'geopandas']),
            'timings': {
                'start': time.strftime('%Y%m%dT%H%M%S')
            }
        }
        self.started_at = time.perf_counter()

        self._store_pydov_code()

        self.lock = Lock()
        atexit.register(self._pydov_exit)

    def _safe_get_version(self, module):
        """Try to get the version string of the given module and return None
        on error or when module is not found.

        Parameters
        ----------
        module : string
            Name of the module.

        Returns
        -------
        string
            Version string of the module.
        """
        ms = importlib.util.find_spec(module)
        if ms is not None:
            try:
                return importlib.import_module(module).__version__
            except Exception:
                return None
        else:
            return None

    def _store_pydov_code(self):
        """Store the pydov source code itself in the archive.

        To get a fully reproducible pydov run, one has to a) save and replay
        all remote DOV data and b) rerun with the same pydov version for code
        changes can effect the result too.

        One can rerun an archive with the saved code by prepending the ZIP
        archive to the system path before importing pydov::

            import sys
            sys.path.insert(0, 'C:\\pydov-archive-20200128T134936-96bda7.zip')
            import pydov

        """
        pydov_root = Path(pydov.__file__).parent
        for f in pydov_root.glob('**/*.py'):
            self.log_archive_file.write(
                str(f), 'pydov/' + str(f.relative_to(pydov_root)))

    def _pydov_exit(self):
        """Save metadata and close ZIP archive before ending Python session."""
        self.metadata['timings']['end'] = time.strftime('%Y%m%dT%H%M%S')
        self.metadata['timings']['run_time_secs'] = (
            time.perf_counter() - self.started_at)

        try:
            self.log_archive_file.writestr(
                'metadata.json', json.dumps(self.metadata, indent=2))
            self.log_archive_file.close()
        except ValueError:
            # already closed, this should only happen while running tests
            pass
        else:
            print('pydov session was saved as {}'.format(self.log_archive))

    def meta_received(self, url, response):
        """Called when a response for a metadata requests is received.

        Create a stable hash based on the URL and archive the response.

        Parameters
        ----------
        url : str
            URL of the metadata request.
        response : bytes
            The raw response as received from resolving the URL.

        """
        md5_hash = md5(url.encode('utf8')).hexdigest()
        log_path = 'meta/' + md5_hash + '.log'

        if log_path not in self.log_archive_file.namelist():
            self.log_archive_file.writestr(log_path, response.decode('utf8'))

    def inject_meta_response(self, url):
        """Inject a response for a metadata request.

        Create a stable hash based on the URL and inject a previously saved
        response if available. If no previous response is available, return
        None to resume normal pydov flow.

        Parameters
        ----------
        url : str
            URL of the metadata request.

        Returns
        -------
        bytes, optional
            The response to use in favor of resolving the URL. Returns None if
            no previously recorded response is available for this request.

        """
        md5_hash = md5(url.encode('utf8')).hexdigest()
        log_path = 'meta/' + md5_hash + '.log'

        if log_path not in self.log_archive_file.namelist():
            return None

        with self.log_archive_file.open(log_path, 'r') as log_file:
            response = log_file.read()

        return response

    def wfs_search_result_received(self, query, features):
        """Called after a WFS search finished.

        Create a stable hash based on the query and archive the feature
        response.

        Parameters
        ----------
        query : etree.ElementTree
            The WFS GetFeature request sent to the WFS server.
        features : etree.ElementTree
            The WFS GetFeature response containings the features.

        """
        with self.lock:
            q = etree.tostring(query, encoding='unicode')
            md5_hash = md5(q.encode('utf8')).hexdigest()
            log_path = 'wfs/' + md5_hash + '.log'

            if log_path not in self.log_archive_file.namelist():
                self.log_archive_file.writestr(
                    log_path,
                    etree.tostring(features, encoding='utf8').decode('utf8'))

    def inject_wfs_getfeature_response(self, query):
        """Inject a response for a WFS GetFeature request.

        Create a stable hash based on the query and inject a previously saved
        response if available. If no previous response is available, return
        None to resume normal pydov flow.

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
        with self.lock:
            q = etree.tostring(query, encoding='unicode')
            md5_hash = md5(q.encode('utf8')).hexdigest()
            log_path = 'wfs/' + md5_hash + '.log'

            if log_path not in self.log_archive_file.namelist():
                return None

            with self.log_archive_file.open(log_path, 'r') as log_file:
                tree = log_file.read()

        return tree

    def xml_received(self, pkey_object, xml):
        """Called when the XML of a given object is received, either from
        the cache or from the remote DOV service.

        Create a stable hash based on the pkey_object and archive the xml
        response.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the retrieved object.
        xml : bytes
            The raw XML data of this DOV object as bytes.

        """
        with self.lock:
            md5_hash = md5(pkey_object.encode('utf8')).hexdigest()
            log_path = 'xml/' + md5_hash + '.log'

            if log_path not in self.log_archive_file.namelist():
                self.log_archive_file.writestr(log_path, xml.decode('utf8'))

    def inject_xml_response(self, pkey_object):
        """Inject a response for a DOV XML request.

        Create a stable hash based on the pkey_object and inject a previously
        saved response if available. If no previous response is available,
        return None to resume normal pydov flow.

        Parameters
        ----------
        pkey_object : str
            The permanent key of the DOV object.

        Returns
        -------
        xml : bytes, optional
            The XML response to use in favor of resolving the URL. Return
            None to disable this inject hook.

        """
        with self.lock:
            md5_hash = md5(pkey_object.encode('utf8')).hexdigest()
            log_path = 'xml/' + md5_hash + '.log'

            if log_path not in self.log_archive_file.namelist():
                return None

            with self.log_archive_file.open(log_path, 'r') as log_file:
                xml = log_file.read()

            return xml


class RepeatableLogReplayer(AbstractInjectHook):
    """Class for replaying a saved pydov session from a ZIP archive.

    This will reroute all external requests to the saved results in the ZIP
    archive, enabling fully reproducable pydov runs.

    """

    def __init__(self, log_archive):
        """Initialise a RepeatableLogReplayer hook.

        It will reroute all external requests to the saved results in the
        given ZIP archive.

        Parameters
        ----------
        log_archive : str
            Path to the ZIP archive to use for replay.

        """
        self.log_archive = log_archive

        self.log_archive_file = zipfile.ZipFile(
            self.log_archive, 'r', compression=zipfile.ZIP_DEFLATED)

        self.lock = Lock()

        atexit.register(self._pydov_exit)

    def _pydov_exit(self):
        """Close ZIP archive before ending Python session."""
        self.log_archive_file.close()

    def inject_meta_response(self, url):
        """Inject a response for a metadata request.

        Create a stable hash based on the URL and inject the previously saved
        response.

        Parameters
        ----------
        url : str
            URL of the metadata request.

        Returns
        -------
        bytes, optional
            The response to use in favor of resolving the URL.

        Raises
        ------
        pydov.util.errors.LogReplayError
            When the response required for this URL could not be found in the
            archive. This happens for instance when replaying an archive for
            a different pydov session than the one it was saved for.

        """
        md5_hash = md5(url.encode('utf8')).hexdigest()
        log_path = 'meta/' + md5_hash + '.log'

        if log_path not in self.log_archive_file.namelist():
            raise LogReplayError(
                'Failed to replay log: no entry for '
                'meta response of {}.'.format(md5_hash)
            )

        with self.log_archive_file.open(log_path, 'r') as log_file:
            response = log_file.read()

        return response

    def inject_wfs_getfeature_response(self, query):
        """Inject a response for a WFS GetFeature request.

        Create a stable hash based on the query and inject the previously saved
        response.

        Parameters
        ----------
        query : etree.ElementTree
            The WFS GetFeature request sent to the WFS server.

        Returns
        -------
        xml: bytes, optional
            The GetFeature response to use in favor of resolving the URL.

        Raises
        ------
        pydov.util.errors.LogReplayError
            When the response required for this URL could not be found in the
            archive. This happens for instance when replaying an archive for
            a different pydov session than the one it was saved for.

        """
        q = etree.tostring(query, encoding='unicode')
        md5_hash = md5(q.encode('utf8')).hexdigest()
        log_path = 'wfs/' + md5_hash + '.log'

        if log_path not in self.log_archive_file.namelist():
            raise LogReplayError(
                'Failed to replay log: no entry for '
                'WFS result of {}.'.format(md5_hash)
            )

        with self.log_archive_file.open(log_path, 'r') as log_file:
            tree = log_file.read()

        return tree

    def inject_xml_response(self, pkey_object):
        """Inject a response for a DOV XML request.

        Create a stable hash based on the pkey_object and inject the previously
        saved response.

        Parameters
        ----------
        pkey_object : str
            The permanent key of the DOV object.

        Returns
        -------
        xml : bytes, optional
            The XML response to use in favor of resolving the URL. Return
            None to disable this inject hook.

        Raises
        ------
        pydov.util.errors.LogReplayError
            When the response required for this URL could not be found in the
            archive. This happens for instance when replaying an archive for
            a different pydov session than the one it was saved for.

        """
        with self.lock:
            md5_hash = md5(pkey_object.encode('utf8')).hexdigest()
            log_path = 'xml/' + md5_hash + '.log'

            if log_path not in self.log_archive_file.namelist():
                raise LogReplayError(
                    'Failed to replay log: no entry for '
                    'XML result of {}.'.format(md5_hash)
                )

            with self.log_archive_file.open(log_path, 'r') as log_file:
                xml = log_file.read()

            return xml
