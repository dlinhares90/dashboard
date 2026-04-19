from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import json
import os

TOKEN = os.environ.get('KOMMO_ACCESS_TOKEN', open('.env').read().split('KOMMO_ACCESS_TOKEN=')[1].split('\n')[0].strip())
DOMAIN = 'arthurdiasimplantodontista.kommo.com'

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('dashboard.html', 'text/html')
        elif self.path.startswith('/api/'):
            self.proxy_kommo(self.path[4:])
        else:
            self.send_response(404)
            self.end_headers()

    def serve_file(self, filename, content_type):
        try:
            with open(filename, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type + '; charset=utf-8')
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def proxy_kommo(self, path):
        url = f'https://{DOMAIN}/api/v4{path}'
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {TOKEN}'})
        try:
            with urllib.request.urlopen(req) as r:
                data = r.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()

if __name__ == '__main__':
    port = 8080
    print(f'Dashboard rodando em http://localhost:{port}')
    HTTPServer(('localhost', port), Handler).serve_forever()
