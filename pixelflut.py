import sys
import socket
from PIL import Image

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1], int(sys.argv[2])))

if len(sys.argv) > 4:
    yoffset = sys.argv[5]
    xoffset = sys.argv[4]
else:
    xoffset = 0
    yoffset = 0

def pixel(x, y, r, g, b, a=255):
    if a == 255:
        sock.send(b'PX %d %d %02x%02x%02x\n' % (x, y, r, g, b))
    else:
        sock.send(b'PX %d %d %02x%02x%02x%02x\n' % (x, y, r, g, b, a))

im = Image.open(sys.argv[3]).convert('RGBA')
_, _, w, h = im.getbbox()
payloads = []
for x in range(w):
    for y in range(h):
        r, g, b, a = im.getpixel((x, y))
        payloads.append([int(x) + int(xoffset), int(y) + int(yoffset), r, g, b, a])

while True:
    for payload in payloads:
        try:
            pixel(payload[0], payload[1], payload[2], payload[3], payload[4], payload[5])
        except OSError:
            sock.connect((sys.argv[1], int(sys.argv[2])))
