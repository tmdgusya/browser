import pytest

from src.url import URL

def test_validate_url_creation():
  try:
    url = URL("http://example.com")
  except Exception as e:
    pytest.fail(f"Failed to create URL: {e}")

def test_validate_url_creation_with_invalid_scheme():
  with pytest.raises(AssertionError):
    URL("ftp://example.com")
  

def test_validate_root_path():
  url = URL("http://example.com")
  assert url.scheme == "http"
  assert url.host == "example.com"
  assert url.path == "/"
  
def test_validate_path():
  url = URL("http://example.com/path")
  assert url.scheme == "http"
  assert url.host == "example.com"
  assert url.path == "/path"
  
def test_validate_path_with_query():
  url = URL("http://example.com/path?query=value")
  assert url.scheme == "http"
  assert url.host == "example.com"
  assert url.path == "/path?query=value"
  
def test_validate_https_url():
  url = URL("https://example.com")
  assert url.scheme == "https"
  assert url.host == "example.com"
  assert url.path == "/"
  
def test_validate_https_url_with_path():
  url = URL("https://example.com/path")
  assert url.scheme == "https"
  assert url.host == "example.com"
  assert url.path == "/path"
  
def test_validate_https_url_with_query():
  url = URL("https://example.com/path?query=value")
  assert url.scheme == "https"
  assert url.host == "example.com"
  assert url.path == "/path?query=value"
  
def test_validate_https_url_with_query_and_fragment():
  url = URL("https://example.com/path?query=value#fragment")
  assert url.scheme == "https"
  assert url.host == "example.com"

def test_validate_parser_proper_port():
  url = URL("http://example.com")
  assert url.port == 80
  url = URL("https://example.com")
  assert url.port == 443
  
def test_validate_parser_proper_port_with_path():
  url = URL("http://example.com/path")
  assert url.port == 80
  url = URL("https://example.com/path")
  assert url.port == 443
  
def test_validate_parsing_port_with_host():
  url = URL("http://example.com:8080")
  assert url.port == 8080
  url = URL("https://example.com:8080")
  assert url.port == 8080
  
def test_validate_parsing_port_with_path():
  url = URL("http://example.com:8080/path")
  assert url.port == 8080
  url = URL("https://example.com:8080/path")
  assert url.port == 8080

def test_show_lt_and_gt_as_tag():
  url = URL("http://example.com:8080")
  text = url.show("<html><div><p>&lt;p&gt;</p></div></html>")
  assert text == "<p>"
  
def test_show_lt_and_gt_as_tag_2():
  url = URL("http://example.com:8080")
  text = url.show("<html><div><p>&lt;p&gt;</p>&lt;div&gt;</div></html>")
  assert text == "<p><div>"