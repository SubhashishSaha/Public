from email import message, message_from_binary_file
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

memory = []

form = '''<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
  <pre>
 #
  </pre>
'''


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        print('length:' + str(length))
        data = self.rfile.read(length).decode()
        print('data:' + data)
        message = parse_qs(data)["message"][0]
        message = message.replace("<", "&lt;")
        memory.append(message)
        print(memory)
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()
        # self.wfile.write(message.encode())

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        messages = ""
        for message in memory:
            messages = messages + "<br> " + message
            print('t1:' + messages)
        print(messages)
        form1 = form.replace("#", messages)
        print(form1)
        self.wfile.write(form1.encode())


if __name__ == '__main__':
    server_address = ('', 8090)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
