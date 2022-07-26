import argparse

import requests
from flask import Flask, request

app = Flask(__name__)

dov_base_url = 'https://www.dov.vlaanderen.be/'
no_xdov = False

error_404 = """<!-- THEME DEBUG -->
<!-- THEME HOOK: 'html' -->
<!-- FILE NAME SUGGESTIONS:
* html--error--502.html.html.twig
* html--error.html.twig
x html.html.twig
-->
<!-- BEGIN OUTPUT from 'themes/dov_webuniversum/html.html.twig' -->
<html>
</html>
"""


def rewrite_content_reverse(content):
    """Rewrite content coming from DOV.

    Parameters
    ----------
    content : str or bytes
        The content to rewrite.

    Returns
    -------
    str or bytes
        The content where all URLs starting with DOV_BASE_URL are rewritten
        to localhost.
    """
    def rewrite(content):
        return content.replace(dov_base_url, 'http://localhost:1337/')

    if isinstance(content, bytes):
        return rewrite(content.decode('utf8')).encode('utf8')
    else:
        return rewrite(content)


def rewrite_content_forward(content):
    """Rewrite content going to DOV.

    Parameters
    ----------
    content : str or bytes
        The content to rewrite.

    Returns
    -------
    str or bytes
        The content where all URLs starting with DOV_BASE_URL are rewritten
        to localhost.
    """
    def rewrite(content):
        return content.replace('http://localhost:1337/', dov_base_url)

    if isinstance(content, bytes):
        return rewrite(content.decode('utf8')).encode('utf8')
    else:
        return rewrite(content)


@app.route('/', defaults={'path': ''}, methods=['HEAD'])
@app.route('/<path:path>', methods=['HEAD'])
def proxy_head(path):
    """Proxy HEAD requests.

    Parameters
    ----------
    path : str
        The path on the DOV server to proxy to.

    Returns
    -------
    flask.Response
        The response of the DOV service.
    """
    full_path = request.full_path
    r = requests.head(f'{dov_base_url.rstrip("/")}{full_path}')
    return r.content


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def proxy_get(path):
    """Proxy GET requests.

    Parameters
    ----------
    path : str
        The path on the DOV server to proxy to.

    Returns
    -------
    flask.Response
        The response from the DOV service, content adjusted according to proxy
        rewrites.

        If --no-xdov was specified, returns 404 on all requests headed for
        XDOV.
    """
    full_path = request.full_path

    if no_xdov and (full_path.startswith('/data')
                    or full_path.startswith('/xdov')):
        return error_404, 404

    r = requests.get(f'{dov_base_url.rstrip("/")}{full_path}')
    return rewrite_content_reverse(r.content)


@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def proxy_post(path):
    """Proxy GET requests.

    Parameters
    ----------
    path : str
        The path on the DOV server to proxy to.

    Returns
    -------
    flask.Response
        The response from the DOV service, content adjusted according to proxy
        rewrites.
    """
    full_path = request.full_path
    data = rewrite_content_forward(request.data)
    r = requests.post(f'{dov_base_url.rstrip("/")}{full_path}', data)
    return rewrite_content_reverse(r.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DOV proxy')

    parser.add_argument(
        '--dov-base-url', dest='dov_base_url',
        default='https://www.dov.vlaanderen.be/', action='store',
        help='DOV base URL to proxy to'
    )
    parser.add_argument(
        '--no-xdov', dest='no_xdov', action='store_true',
        help='XDOV requests return 404')

    args = parser.parse_args()

    no_xdov = args.no_xdov
    dov_base_url = args.dov_base_url

    app.run(host='127.0.0.1', port=1337)
