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
pydov.util.hooks.AbstractHook. An instance of this class can then by
registered as a pydov hook, and implemented methods will be subsequently be
called when the user interacts with pydov code. The AbstractHook class
provides default, empty, implementation of all
available methods allowing users to only implement the methods for the
events they need.

Note that hooks are executed inline in pydov and as a result can halt or
slow down usage of the package, depending on the implementation of the hooks
itself.

Available event hooks
.....................

wfs_search_init
    This method will be called whenever a WFS search is initiated. There is
    one parameter `typename` with the WFS typename that is queried.

wfs_search_result
    This method will be called whenever a WFS search is completed. There is
    one parameter `number_of_results` with the number of search results.

xml_requested
    This method will be called whenever an XML document is needed. There is
    one parameter `pkey_object` with the permanent key of the DOV object.
    This event is either followed by `xml_cache_hit` or `xml_downloaded`.

xml_cache_hit
    This method will be called whenever an XML document is reused from the
    cache. There is one parameter `pkey_object` with the permanent key of
    the DOV object.

xml_downloaded
    This method will be called whenever an XML document is downloaded from
    the DOV webservices. There is one parameter `pkey_object` with the
    permanent key of the DOV object.

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
