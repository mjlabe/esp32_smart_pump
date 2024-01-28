try:
    import usocket as socket
except:
    import socket

try:
    from machine import Pin
except ModuleNotFoundError:
    pass

import gc

import ujson

gc.collect()


class Request:
    def __init__(self, request):
        self.text = request.decode("utf-8")
        print("Content = %s" % self.text)
        self.headers = {}
        self.params = {}
        self.method = None
        self._parse_result()

    def get_param(self, param):
        return self.params.get(param)

    def parse_get_params(self, line):
        query_part = line.split("HTTP")[0].strip()
        _, query = query_part.split("?")
        self.params = {
            param.split("=")[0].strip(): param.split("=")[1].strip()
            for param in query.split("&")
        }

    def parse_post_params(self):
        # assume only thing left for now
        text = self.text[0]
        if "{" in text:
            # json parse
            self.params = ujson.loads(text)
        else:
            self.params = {
                param_set.split("=")[0]: param_set.split("=")[1]
                for param_set in text.split("&")
            }

    def _parse_result(self):
        self.text = self.text.split("\r\n")
        while self.text:
            line = self.text.pop(0).strip()
            if line == "":
                break
            _method = line[0:4].strip()
            if _method in ("POST", "GET"):
                self.method = _method
                if self.method == "GET":
                    self.parse_get_params(line)
                continue
            if len(line.split(":")) >= 2:
                data = line.split(":")
                self.headers[data[0]] = (":".join(data[1:])).strip()
                continue
        if self.method == "POST":
            self.parse_post_params()
        self.text = "\r\n".join(self.text)
        return


def process_request(request, param):
    req = Request(request)
    return req.get_param(param)


def respond(conn, message):
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(message)


def start_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", 80))
        sock.listen(5)

        while True:
            try:
                if gc.mem_free() < 102000:
                    gc.collect()
                conn, addr = sock.accept()
                conn.settimeout(3.0)
                print("Got a connection from %s" % str(addr))
                request = conn.recv(1024)
                conn.settimeout(None)

                respond(conn, "")
            except OSError as e:
                conn.close()
                print("Connection closed")
            finally:
                conn.close()
                print("Connection closed")
    finally:
        sock.close()
