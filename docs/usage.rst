=====
Usage
=====

To use PyDOV in a project::

    import pydov

Caching
-------
To speed up subsequent queries involving similar data, pydov uses a caching
mechanism where raw DOV XML data is cached locally for later reuse.

By default, this is a global cache shared by all usages of pydov on the same
system. This means subsequent calls in the same script, multiple runs of
the same script over time and multiple implementations or applications
using pydov on the same system all use the same cache.

The default cache will reuse cached data for up to two weeks: if cached data
for an object is available and has been downloaded less than two weeks ago,
it will be reused in favor of downloading from the DOV services.

Disabling the cache
*******************
You can (temporarily!) disable the caching mechanism by issuing::

    import pydov

    pydov.cache = None

This disables both the saving of newly downloaded data in the cache, as well
as reusing existing data in the cache. It remains valid for the time being of
the instantiated pydov.cache object.
It does not delete existing data in the cache.

Changing the location of cached data
************************************

By default, pydov stores the cache in a temporary directory provided by the
user's operating system. On Windows, the cache is usually located in::

    C:\Users\username\AppData\Local\Temp\pydov\

If you want the cached xml files to be saved in another location you can define
your own cache, as follows::

    import pydov.util.caching

    pydov.cache = pydov.util.caching.TransparentCache(
        cachedir=r'C:\temp\pydov'
    )

Besides controlling the cache's location, this also allows using a different
cache in different scripts or projects.

Mind that xmls are stored by search type because permalinks are not unique
across types. Therefore, the dir structure of the cache will look like, e.g.::

    ...\pydov\boring\filename.xml
    ...\pydov\filter\filename.xml


Changing the maximum age of cached data
***************************************

If you work with rapidly changing data or want to control when cached data
is renewed, you can do so by changing the maximum age of cached data to
be considered valid for the currenct runtime::

    import pydov.util.caching
    import datetime

    pydov.cache = pydov.util.caching.TransparentCache(
        max_age=datetime.timedelta(days=1)
    )

If a cached version exists and is younger than the maximum age, it is used
in favor of renewing the data from DOV services. If no cached version
exists or is older than the maximum age, the data is renewed and saved
in the cache.

Note that data older than the maximum age is not automatically deleted from
the cache.

Cleaning the cache
******************

Since we use a temporary directory provided by the operating system, we rely
on the operating system to clean the folder when it deems necessary.

Should you want to remove the pydov cache from code yourself, you can do so
by issuing::

    import pydov

    pydov.cache.clean()

Note that this will erase the entire cache, not only the records older than
the maximum age.

Hooks
-----
PyDOV uses a simple system of 'hooks' to enable users to integrate custom
code with certain events that occur while using the PyDOV package.

By default, there is one hook that prints out the progress of XML downloads
to standard output.

Writing custom hooks
********************
Users can write custom hooks and add them to PyDOV at runtime, to be able to
interact with PyDOV at the occurance of certain 'events'.

To implement custom hooks, create a new subclass of
pydov.util.hooks.AbstractHook. An instance of this class can then by
registered as a PyDOV hook, and implemented methods will be subsequently be
called when the user interacts with PyDOV code. The AbstractHook class
provides default, empty, implementation of all
available methods allowing users to only implement the methods for the
events they need.

Note that hooks are executed inline in PyDOV and as a result can halt or
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
described above, one needs to register an instance of this class with PyDOV
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

Progress hook
*************
By default, PyDOV uses a single default hook used for printing out the
progress of XML downloads to stdout.

To disable this progress indication, one can disable the progress hook by
issuing::

    import pydov

    pydov.hooks = []
