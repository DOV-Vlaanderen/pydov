.. _network_proxy:

========================
Network via proxy server
========================

If your network requires accessing the internet via a proxy server, there are several ways of configuring this so that pydov uses the correct proxy server in order to access online resources.

Environment variables
---------------------

If the required proxy server(s) are available in the correct environment variables, pydov will honor this and use them to connect to the internet.
They should be set using the environment variables ``HTTP_PROXY`` and ``HTTPS_PROXY`` for access to HTTP and HTTPS resources respectively.

Preferably these environment variables are set in your operating system or Python environment, so that they are transparently applied.
Should you however not be in the possility to add them at a higher lever, it is always possible to configure the proxy servers manually by adding
the following statements *at the top* of your pydov script::

    import os
    os.environ['HTTP_PROXY'] = 'http://url-of-proxy.server:port'
    os.environ['HTTPS_PROXY'] = 'http://url-of-proxy.server:port'

Proxy autoconfiguration via PAC
-------------------------------

It is possible that your company network or organisation is using a more complex proxy setup and allows auto discovery of the required proxy servers using PAC.
While not included in the base pydov dependencies, pydov can support this proxy autodiscovery when it is installed additionally.

When installed, pydov will autodiscover and use the required proxy server when connecting to the internet.
This also makes sure the proxy will be enabled only when required by the network you are currently using.

You can install pydov and the optional proxy autodiscovery with a single command::

    pip install pydov[proxy]

Or, when you need the proxy to install remote packages via pip as well::

    pip install --proxy http://url-of-proxy.server:port pydov[proxy]

.. note::

    If you are using conda you can also install the dukpy dependency through conda first:

        #. Configure proxy servers in conda::

            conda config --set proxy_servers.http http://url-of-proxy.server:port
            conda config --set proxy_servers.https http://url-of-proxy.server:port

        #. Install dukpy via conda: :code:`conda install -c conda-forge dukpy`
        #. Then install pydov with proxy support using :code:`pip install --proxy http://url-of-proxy.server:port pydov[proxy]`

