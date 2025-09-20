
import socket


class URL:
  
  def __init__(self, url: str) -> None:
    self.scheme, url = url.split("://", 1)
    assert self.scheme in ["http"]
    if "/" not in url:
      url += "/"
    
    self.host, url = url.split("/", 1)
    self.path = "/" + url
  
  def requests(self) -> str:
    try:
      s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
      )
      s.connect((self.host, 80))
      s.send(f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\nConnection: close\r\n\r\n".encode())
      response = s.makefile("r", encoding="utf-8", newline="\r\n")

      statusline = response.readline()
      version, status, explanation = statusline.split(" ", 2)

      print(f"status: {status}, version: {version}, explanation: {explanation}")

      response_headers = {}
      while True:
        line = response.readline()
        if line == "\r\n": break
        header, value = line.split(": ", 1)
        response_headers[header.casefold()] = value
      
      if 'content-length' in response_headers:
        content_length = int(response_headers['content-length'].strip())
        response_body = response.read(content_length)
      else:
        response_body = response.read()
      return response_body
    except Exception as e:
      raise e
    finally:
      s.close()
      
  def show(self, body: str):
    in_tag = False
    print(f"body: {body}")
    for c in body:
      if c == "<":
        in_tag = True
      elif c == ">":
        in_tag = False
      elif not in_tag:
        print(c, end="")
  
  def load(self):
    body = self.requests()
    self.show(body)
  
if __name__ == "__main__":
  url = URL("http://example.org/")
  url.load()