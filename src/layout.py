
import tkinter
import tkinter.font

from typing import List

from src.url import Tag, Text

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100


class Layout:
  
  def __init__(self, tokens: List[str]) -> None:
    self.display_list = []
    self.line = []
    self.font_cache = {}
    self.cursor_x = HSTEP
    self.cursor_y = VSTEP
    self.size = 12
    self.weight = "normal"
    self.style = "roman"
    
    for tok in tokens:
      self.token(tok)
    
    self.flush()
    
  def get_font(self, size, weight, style):
    key = (size, weight, style)
    if key not in self.font_cache:
      font = tkinter.font.Font(size=size, weight=weight, slant=style)
      label = tkinter.Label(font=font)
      self.font_cache[key] = (font, label)
      
    return self.font_cache[key][0]
      
  def flush(self):
    if not self.line: return
    metrics = [font.metrics() for x, word, font in self.line]
    max_ascent = max([metric["ascent"] for metric in metrics])
    baseline = self.cursor_y + 1.25 * max_ascent
    
    for x, word, font in self.line:
      y = baseline - font.metrics("ascent")
      self.display_list.append((x, y, word, font))
      
    self.cursor_x = HSTEP
    self.line = []
      
  def word(self, word):
    word = word.replace("&lt;", "<")
    word = word.replace("&gt;", ">")
    
    font = self.get_font(size=self.size, weight=self.weight, style=self.style)
    w = font.measure(word)
    self.line.append((self.cursor_x, word, font))
    self.cursor_x += w + font.measure(" ")
    
    if self.cursor_x + w > WIDTH - HSTEP:
      self.flush()
      self.cursor_y += font.metrics('linespace') * 1.25
      self.cursor_x = HSTEP
  
  def token(self, tok):
    if isinstance(tok, Text):
      for word in tok.text.split():
        self.word(word)
    
    if isinstance(tok, Tag):
      if tok.tag == "i":
        self.style = "italic"
      elif tok.tag == "/i":
        self.style = "roman"
      elif tok.tag == "b":
        self.wieght == "bold"
      elif tok.tag == "/b":
        self.wieght = "normal"
      elif tok.tag == "small":
        self.size -= 2
      elif tok.tag == "/small":
        self.size += 2
      elif tok.tag == "big":
        self.size += 4
      elif tok.tag == "/big":
        self.size -= 4
      elif tok.tag == "br":
        self.flush()
      elif tok.tag == "/p":
        self.flush()
        self.cursor_y = VSTEP