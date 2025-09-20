import socket
import ssl
import sys

from typing import Literal
from .http import HttpBuilder

SUPPORT_SCHEME = Literal["http", "https", "file"]
class URL:
  
  def __init__(self, url: str) -> None:
    self.scheme, url = url.split("://", 1)
    assert self.scheme in ["http", "https", "file"]

    if self.scheme in ["http", "https"]:
      if "/" not in url:
        url += "/"
      if self.scheme == "https":
        self.port = 443
      if self.scheme == "http":
        self.port = 80
      self.host, url = url.split("/", 1)
      if ":" in self.host:
        self.host, self.port = self.host.split(":", 1)
        self.port = int(self.port)
      self.path = "/" + url
    if self.scheme in ["file"]:
      self.path = url
  
  def requests(self) -> str:
    try:
      s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
      )
      s.connect((self.host, self.port))
      if self.scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=self.host)
      request_builder = HttpBuilder()
      request_builder = request_builder.set_method("GET")
      request_builder = request_builder.set_http_version("HTTP/1.0")
      request_builder = request_builder.set_path(self.path)
      request_builder = request_builder.set_host(self.host)
      s.send(request_builder.build())
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
  
  def read_file(self):
    assert self.scheme == "file"
    
    with open(self.path, "r+") as f:
      while True:
        body = f.readline()
        if len(body) == 0: break
        print(body)
      
  def show(self, body: str):
    in_tag = False
    printed = ""
    for c in body:
      if c == "<":
        in_tag = True
      elif c == ">":
        in_tag = False
      elif not in_tag:
        printed += c
        print(c, end="")
    
    printed = printed.replace("&lt;", "<")
    printed = printed.replace("&gt;", ">")
    return printed
  
  def load(self):
    if self.scheme == "file":
      self.read_file()
    else:
      body = self.requests()
      self.show(body)
  
if __name__ == "__main__":
  url = URL(sys.argv[1])
  url.load()