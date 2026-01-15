import errno
import os

def full_read(fd, count):
    nleft = count
    data = bytearray()

    while nleft > 0:
        try:
            chunk = os.read(fd, nleft)
            if not chunk:  # EOF
                break
            data.extend(chunk)
            nleft -= len(chunk)
        except OSError as e:
            if e.errno == errno.EINTR:
                continue
            else:
                raise

    return bytes(data)