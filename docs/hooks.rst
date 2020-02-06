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

    pydov.hooks = []


Writing custom hooks
********************
Users can write custom hooks and add them to pydov at runtime, to be able to
interact with pydov at the occurance of certain 'events'.

To implement custom hooks, create a new subclass of
:class:`pydov.util.hooks.AbstractHook`. An instance of this class can then by
registered as a pydov hook, and implemented methods will be subsequently be
called when the user interacts with pydov code. The AbstractHook class
provides default, empty, implementation of all
available methods allowing users to only implement the methods for the
events they need.

Note that certain events (notably the XML related events) will be called from
multiple threads simultaneously, so implementations must be threadsafe or use
locking. Nonetheless, hooks are executed inline in the processing threads and
as a result can halt or slow down usage of the package, depending on the
implementation of the hooks itself.


Available event hooks
.....................

meta_received (url: str, response: bytes)
    This method will be called whenever a response for a metadata request is
    received. There are two parameters, `url` with the full URL of the metadata
    request and `response` with the response from the server.

    Metadata requests include, amongst others: WFS GetCapabilities,
    requests for MD_Metadata, FC_FeatureCatalogue and XSD schemas. These are
    all calls except for WFS GetFeature requests and XML downloads of DOV data
    - these are other hooks.

inject_meta_response (url: str) -> bytes
    This method can be used to inject a custom response for a metadata request
    with the given URL. There is one parameter `url` with the full URL of the
    metadata request.

    When at least one registered hook returns a response for a given URL,
    the remote call is not executed and instead the response from the
    last registered hook (that is non-null) is used instead.

wfs_search_init (typename: str)
    This method will be called whenever a WFS search is initiated. There is
    one parameter `typename` with the WFS typename that is queried.

wfs_search_result (number_of_results: int)
    This method will be called whenever a WFS search is completed. There is
    one parameter `number_of_results` with the number of search results.

wfs_search_result_received (query: etree.ElementTree, features: etree.ElementTree)
    This method will be called whenever a WFS search finished. There are two
    parameters, `query` is the WFS GetFeature request sent to the server and
    `features` is the FeatureCollection received in response.

inject_wfs_getfeature_response (query: etree.ElementTree) -> bytes
    This method can be used to inject a custom response for a WFS GetFeature
    request with the given query. There is one parameter `query` with the WFS
    GetFeature request sent to the server.

    When at least one registered hook returns a response for a given query,
    the remote call is not executed and instead the response from the
    last registered hook (that is non-null) is used instead.

xml_received (pkey_object: str, xml: bytes)
    This method will be called whenever an XML document is received, either
    from the cache or from the remote DOV service. There are two parameters,
    `pkey_object` with the permanent key of the DOV object and `xml` containing
    the full XML representation.

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

xml_cache_hit (pkey_object: str)
    This method will be called whenever an XML document is reused from the
    cache. There is one parameter `pkey_object` with the permanent key of
    the DOV object.

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

    class MyHooks(pydov.util.hooks.AbstractHook):
        def wfs_search_result(self, number_of_results):
            print('WFS search completed with %i results.' % number_of_results)

        def xml_requested(self, pkey_object):
            print('Requested XML document for object %s.' % pkey_object)

    pydov.hooks.append(MyHooks())
