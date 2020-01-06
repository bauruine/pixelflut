import sys
import socket
import argparse
import logging
import ipaddress
from PIL import Image


def pixel(sock, x, y, r, g, b, a=255):
    if a == 255:
        sock.send(b'PX %d %d %02x%02x%02x\n' % (x, y, r, g, b))
    else:
        sock.send(b'PX %d %d %02x%02x%02x%02x\n' % (x, y, r, g, b, a))

def connect():
    if ipaddress.ip_address(args.host).version == 4:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.bind((args.bind, 0))
    sock.connect((args.host, args.port))
    return sock

def main():
    sock = connect()
    im = Image.open(args.image).convert('RGBA')
    _, _, w, h = im.getbbox()
    payloads = []
    for x in range(w):
        for y in range(h):
            r, g, b, a = im.getpixel((x, y))
            payloads.append([int(x) + args.xoffset, int(y) + args.yoffset, r, g, b, a])

    while True:
        for payload in payloads:
            try:
                pixel(sock, payload[0], payload[1], payload[2], payload[3], payload[4], payload[5])
            except OSError:
                sock = connect()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Pixelflut')

    # Global arguments
    parser.add_argument('--imagename', dest='image', type=str, required=True, help='The output image name')
    parser.add_argument('--host', dest='host', required=True, help='Pixelflut ip')
    parser.add_argument('--port', dest='port', type=int, required=True, help='Port of the pixelflut server')
    parser.add_argument('--xoffset', dest='xoffset', type=int, required=False, default=0, help='X offset')
    parser.add_argument('--yoffset', dest='yoffset', type=int, required=False, default=0, help='X offset')
    parser.add_argument('--bind', dest='bind', type=int, required=False, default=0, help='X offset')


    #Logging
    # For some reasons urllib does not like the custom logger with inc_names on the debug level.
    # There is a keyerror for inc_name if used with the custom logger but it does work for ERROR levels and
    # therefore we just disable everything except ERROR.
    logging.basicConfig(filename='pixelflut.log', level=logging.DEBUG, filemode='a', format='%(name)s - %(levelname)s - %(message)s')
    logging.getLogger("urllib3").setLevel(logging.ERROR)

    args = parser.parse_args()

    main()

