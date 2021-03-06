import http.server
import requests
from urllib.parse import unquote, parse_qs

from requests.api import patch

memory = {}

form = '''<!DOCTYPE html>
<title>Bookmark Server</title>
<form method="POST">
     <label>Long Uri:
         <input name="longuri">
     </label>
     <br>
     <label>Short name:
         <input name="shortname">
     </label>
     <br>
     <button type="submit">Save it!</button>
</form>
<p>Uri I Know about
<pre>
{}
</pre>
'''


def checkURI(uri, timeout=5):

    try:
        r = requests.get(uri, timeout=timeout)

        return r.status_code == 200
    except requests.RequestException:
        return False


class Shortner(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        name = unquote(self.path[1:])

        if name:
            if name in memory:
                self.send_response(303)
                self.send_header('Location', memory[name])
                self.end_headers()
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("I don't know '{}'.".format(name).encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            known = "\n".join("{} : <a href='{}'>{}</a>".format(key, memory[key], memory[key])
                              for key in sorted(memory.keys()))
            print(known)
            self.wfile.write(form.format(known).encode())

    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        if "longuri" not in params or "shortname" not in params:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Missing form fields!".encode())
            return

        longuri = params["longuri"][0]
        shortname = params["shortname"][0]

        if checkURI(longuri):
            memory[shortname] = longuri

            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(
                "Couldn't fetch URI '{}'. Sorry!".format(longuri).encode())


if __name__ == '__main__':
    server_address = ('', 8090)
    httpd = http.server.HTTPServer(server_address, Shortner)
    print("Server Starting")
    httpd.serve_forever()
