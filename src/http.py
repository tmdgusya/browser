
from typing import Literal

METHOD_TYPE = Literal["GET", "POST"]


class HttpBuilder():
  
  def __init__(self) -> None:
    self.method: METHOD_TYPE = "GET"
    self.support_http_version: str = "HTTP/1.1"
    self.headers = {}
    self.path = ""
    self.host = ""
  
  def set_http_version(self, version: str):
    self.support_http_version = version
    return self
  
  def set_method(self, name: METHOD_TYPE):
    self.method = name
    return self
  
  def add_header(self, key: str, value: str):
    self.headers[key] = value
    return self
  
  def set_path(self, path: str):
    self.path = path
    return self
  
  def set_host(self, host: str):
    self.headers["Host"] = host
    return self
  
  def build(self) -> bytes:
    self.headers["Connection"] = "close"
    message = ""
    message += f"{self.method} {self.path} {self.support_http_version}\r\n"
    for header in self.headers.items():
      key, value = header
      message += f"{key}: {value}\r\n"
    message += f"\r\n"
    print(message)
    return message.encode("utf-8")