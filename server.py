import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import qrcode
from io import BytesIO

class QRCodeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Welcome to the QR Code Generator!')
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        url = parse_qs(post_data)['url'][0]
        if not url:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Please enter a URL.')
            return

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.send_header('Content-Disposition', f'attachment; filename={url.replace(" ", "_")}.png')
        self.end_headers()
        self.wfile.write(img_io.getvalue())

if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(("", PORT), QRCodeRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
