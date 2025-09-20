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