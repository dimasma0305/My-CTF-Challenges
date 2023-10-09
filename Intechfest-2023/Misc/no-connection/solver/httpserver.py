import http.server
import socketserver


def serve(port):
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        print("Serving at port", port)
        httpd.serve_forever()
