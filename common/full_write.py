import errno
import socket

def full_write(fd, buf):
    nleft = len(buf)
    while nleft > 0:
        try:
            nwritten = fd.send(buf)
            nleft -= nwritten
            buf = buf[nwritten:]
        except socket.error as e:
            if e.errno == errno.EINTR:
                continue
            else:
                raise
    return nleft