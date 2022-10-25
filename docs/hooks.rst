=====
Hooks
=====

pydov uses a simple system of 'hooks' to enable users to integrate custom
code with certain events that occur while using the pydov package.

By default, there is one hook that prints out the progress of XML downloads
to standard output.

Progress hook
*************
By default, pydov uses a single default hook used for printing out the
progress of XML downloads to stdout.

To disable this progress indication, one can disable the progress hook by
issuing::

    import pydov

    pydov.hooks.clear()


Writing custom hooks
********************
Users can write custom hooks and add them to pydov at runtime, to be able to
interact with pydov at the occurrence of certain 'events'.

To implement custom hooks, create a new subclass of
:class:`pydov.util.hooks.AbstractReadHook` and/or
:class:`pydov.util.hooks.AbstractInjectHook`. An instance of this class can
then by registered as a pydov hook, and implemented methods will be
subsequently be called when the user interacts with pydov code. Both classes
provide default, empty, implementation of all available methods allowing users
to only implement the methods for the events they need.

Note that certain events (notably the XML related events) will be called from
multiple threads simultaneously, so implementations must be threadsafe or use
locking. Nonetheless, hooks are executed inline in the processing threads and
as a result can halt or slow down usage of the package, depending on the
implementation of the hooks itself.


Available read-only event hooks
...............................

Read-only events allow you to implement custom behaviour when certain events
occur while running pydov code. They are read-only in the sense that they only
receive data about the event (in form of method parameters) and cannot influence
the execution of pydov's internal code.

They are generally safe to use. Mind that they are executed inline in a
blocking way and consequently can slow down pydov queries depending on your
implementation.

To receive read-only event hooks your class should subclass
:class:`pydov.util.hooks.AbstractReadHook`. The following event hooks are
available:

meta_received (url: str, response: bytes)
    This method will be called whenever a response for a metadata request is
    received. There are two parameters, `url` with the full URL of the metadata
    request and `response` with the response from the server.

    Metadata requests include, amongst others: WFS GetCapabilities,
    requests for MD_Metadata, FC_FeatureCatalogue and XSD schemas. These are
    all calls except for WFS GetFeature requests and XML downloads of DOV data
    - these are other hooks.

wfs_search_init (params: dict)
    This method will be called whenever a WFS search is initiated. There is
    one parameter `params` with a dictionary containing parameters used to
    initiate the WFS search:

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

wfs_search_result (number_matched: int, number_returned: int)
    This method will be called whenever a WFS search is completed. There are
    two parameters: `number_matched` with the number of features matching the
    search, and `number_returned` with the amount of features returned by this
    request. Due to server limitations this can be less than number_matched.

    Because of parallel processing, this method will be called simultaneously
    from multiple threads. Make sure your implementation is threadsafe or uses
    locking.

wfs_search_result_received (query: etree.ElementTree, features: etree.ElementTree)
    This method will be called whenever a WFS search finished. There are two
    parameters, `query` is the WFS GetFeature request sent to the server and
    `features` is the FeatureCollection received in response.

    Because of parallel processing, this method will be called simultaneously
    from multiple threads. Make sure your implementation is threadsafe or uses
    locking.

xml_received (pkey_object: str, xml: bytes)
    This method will be called whenever an XML document is received, either
    from the cache or from the remote DOV service. There are two parameters,
    `pkey_object` with the permanent key of the DOV object and `xml` containing
    the full XML representation.

    Because of parallel processing, this method will be called simultaneously
    from multiple threads. Make sure your implementation is threadsafe or uses
    locking.

xml_cache_hit (pkey_object: str)
    This method will be called whenever an XML document is reused from the
    cache. There is one parameter `pkey_object` with the permanent key of
    the DOV object.

    Because of parallel processing, this method will be called simultaneously
    from multiple threads. Make sure your implementation is threadsafe or uses
    locking.

xml_stale_hit (pkey_object: str)
    This method will be called whenever a fresh XML document fails to be
    retrieved from the DOV webservices, but instead a stale document is
    returned from the cache. There is one parameter `pkey_object` with the
    permanent key of the DOV object.

    Because of parallel processing, this method will be called simultaneously
    from multiple threads. Make sure your implementation is threadsafe or uses
    locking.

xml_downloaded (pkey_object: str)
    This method will be called whenever an XML document is downloaded from
    the DOV webservices. There is one parameter `pkey_object` with the
    permanent key of the DOV object.

    Because of parallel processing, this method will be called simultaneously
    from multiple threads. Make sure your implementation is threadsafe or uses
    locking.

xml_fetch_error (pkey_object: str)
    This method will be called whenever a fresh XML document failes to be
    downloaded from the DOV webservices and no stale version is returned from
    the cache. There is one parameter `pkey_object` with the permanent key of
    the DOV object.

    Because of parallel processing, this method will be called simultaneously
    from multiple threads. Make sure your implementation is threadsafe or uses
    locking.


Available inject event hooks
............................

Contrary to read-only hooks described above, inject events allow you to inject
custom behaviour at certain points in pydov's execution stack.

They should be used with extreme care! It is probably wise to open an issue in
Github if you find yourself needing these hooks, since they are most likely not
the right solution for what you're trying to achieve.

To receive inject event hooks your class should subclass
:class:`pydov.util.hooks.AbstractInjectHook`. The following event hooks are
available:


inject_meta_response (url: str) -> bytes
    This method can be used to inject a custom response for a metadata request
    with the given URL. There is one parameter `url` with the full URL of the
    metadata request.

    When at least one registered hook returns a response for a given URL,
    the remote call is not executed and instead the response from the
    last registered hook (that is non-null) is used instead.

inject_wfs_getfeature_response (query: etree.ElementTree) -> bytes
    This method can be used to inject a custom response for a WFS GetFeature
    request with the given query. There is one parameter `query` with the WFS
    GetFeature request sent to the server.

    When at least one registered hook returns a response for a given query,
    the remote call is not executed and instead the response from the
    last registered hook (that is non-null) is used instead.

    Because of parallel processing, this method will be called simultaneously
    from multiple threads. Make sure your implementation is threadsafe or uses
    locking.

inject_xml_response (pkey_object: str) -> bytes
    This method can be used to inject a custom response for a DOV XML
    request for the given object. There is one parameter `pkey_object` with
    the permanent key of the DOV object.

    When at least one registered hook returns a response for a given pkey,
    the remote call is not executed and instead the response from the
    last registered hook (that is non-null) is used instead.

    Because of parallel processing, this method will be called
    simultaneously from multiple threads. Make sure your implementation is
    threadsafe or uses locking.


Integrating custom hooks
........................

After implementing custom hooks by creating a subclass of AbstractHook as
described above, one needs to register an instance of this class with pydov
to enable the execution of the custom hooks.

One can do so by appending an instance to pydov.hooks::

    import pydov

    pydov.hooks.append(MyHooks())

Example
.......

The following example prints out a message whenever a WFS search is
completed and an XML document is requested.::

    import pydov
    import pydov.util.hooks

    class MyHooks(pydov.util.hooks.AbstractReadHook):
        def wfs_search_result(self, number_of_results):
            print('WFS search completed with %i results.' % number_of_results)

        def xml_received(self, pkey_object, xml):
            print('Received XML document for object %s.' % pkey_object)

    pydov.hooks.append(MyHooks())
