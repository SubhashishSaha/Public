from http.server import HTTPServer, BaseHTTPRequestHandler


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # First send 200 OK Response
        self.send_response(200)

        # Then send the Header
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()

        # Now write the response body
        self.wfile.write("Hello,HTTP!\n Subhashish says".encode())


if __name__ == "__main__":
    server_address = ("", 8090)
    httpd = HTTPServer(server_address, HelloHandler)
    print("Server Starting.........")
    httpd.serve_forever()
    print("Server Started.........")
