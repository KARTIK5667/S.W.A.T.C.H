import socket
import argparse
import http.server
import socketserver
import json

parser = argparse.ArgumentParser(description='Serve files from the current directory.')

host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)

parser.add_argument('--host', default=ip, type=str, required=False,
                    help='Specify the IP address to listen on.')

parser.add_argument('--port', default=8080, type=int, required=False,
                    help='Specify the port to listen on.')

args = parser.parse_args()

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/update_data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            json_data = json.loads(post_data)

            # Print and save the data as per your requirements
            print("#########################NEW DATA#######################")
            print(json_data)
            with open('data.json', 'w') as file:
                json.dump(json_data, file)

            # Send a response indicating the success
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Data received and saved successfully.')
        else:
            # For other paths, handle as default
            super().do_POST()

with socketserver.TCPServer((args.host, args.port), MyRequestHandler) as httpd:
    print(f'Server is listening on {args.host} on port {args.port}.')
    httpd.serve_forever()
