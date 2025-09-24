import socket
import ssl
import sys

from dataclasses import dataclass
from typing import List, Literal
from .http import HttpBuilder

@dataclass
class Text:
  text: str
  
@dataclass
class Tag:
  tag: str

SUPPORT_SCHEME = Literal["http", "https", "file"]
class URL:
  
  def __init__(self, url: str) -> None:
    self.scheme, url = url.split("://", 1)
    assert self.scheme in ["http", "https", "file", "view-source:http", "view-source:https"]
    if self.scheme in ["http", "https", "view-source:http", "view-source:https"]:
      if "/" not in url:
        url += "/"
      if "https" in self.scheme:
        print("here")
        self.port = 443
      if "http" in self.scheme:
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
      if "https" in self.scheme:
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
    buffer = []
    with open(self.path, "r+") as f:
      while True:
        text = f.readline()
        buffer.append(text)
        if len(text) == 0: break

    return buffer
      
  def show(self, body: str):
    out = []
    buffer = ""
    show_with_out_tag: bool = False if "view-source" in self.scheme else True
    in_tag = False
    
    if show_with_out_tag:
      for c in body:
        if c == "<":
          in_tag = True
          if buffer: out.append(Text(buffer)) # flush
          buffer = ""
        elif c == ">":
          in_tag = False
          out.append(Tag(buffer))
          buffer = ""
        elif not in_tag:
          buffer += c
    else:
      for c in body:
        buffer += c
    

    
    if not in_tag and buffer:
      out.append(Text(buffer))
    return out
  
  def lex(self) -> List[str]:
    if self.scheme == "file":
      return self.read_file()
    else:
      body = self.requests()
      return self.show(body)
  
if __name__ == "__main__":
  url = URL(sys.argv[1])
  url.lex()