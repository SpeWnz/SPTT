from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
from pathlib import Path

port = 80

httpd = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="snakeoil.pem",keyfile="snakeoil.key")
httpd.socket = ssl_context.wrap_socket(
    httpd.socket,
    server_side=True,
)

httpd.serve_forever()