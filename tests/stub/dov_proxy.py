import argparse

import requests
from flask import Flask, request

app = Flask(__name__)

no_xdov = False


def rewrite_content_reverse(content):
    def rewrite(content):
        return content.replace('https://www.dov.vlaanderen.be/',
                               'http://localhost:1337/')

    if isinstance(content, bytes):
        return rewrite(content.decode('utf8')).encode('utf8')
    else:
        return rewrite(content)


def rewrite_content_forward(content):
    def rewrite(content):
        return content.replace('http://localhost:1337/',
                               'https://www.dov.vlaanderen.be/')

    if isinstance(content, bytes):
        return rewrite(content.decode('utf8')).encode('utf8')
    else:
        return rewrite(content)


@app.route('/', defaults={'path': ''}, methods=['HEAD'])
@app.route('/<path:path>', methods=['HEAD'])
def proxy_head(path):
    full_path = request.full_path
    r = requests.head(f'https://www.dov.vlaanderen.be{full_path}')
    return r.content


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def proxy_get(path):
    full_path = request.full_path

    if no_xdov and full_path.startswith('/data'):
        return """<!-- THEME DEBUG -->
            <!-- THEME HOOK: 'html' -->
            <!-- FILE NAME SUGGESTIONS:
            * html--error--502.html.html.twig
            * html--error.html.twig
            x html.html.twig
            -->
            <!-- BEGIN OUTPUT from 'themes/dov_webuniversum/html.html.twig' -->
            <html>
            </html>
            """, 404

    r = requests.get(f'https://www.dov.vlaanderen.be{full_path}')
    return rewrite_content_reverse(r.content)


@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def proxy_post(path):
    full_path = request.full_path
    data = rewrite_content_forward(request.data)
    r = requests.post(f'https://www.dov.vlaanderen.be{full_path}', data)
    return rewrite_content_reverse(r.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DOV proxy')
    parser.add_argument(
        '--no-xdov', dest='no_xdov', default=False, action='store_true',
        help='XDOV requests return 404')
    args = parser.parse_args()

    no_xdov = args.no_xdov

    app.run(host='127.0.0.1', port=1337)
