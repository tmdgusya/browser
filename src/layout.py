
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
    self.cursor_x = HSTEP
    self.cursor_y = VSTEP
    self.size = 12
    self.weight = "normal"
    self.style = "roman"
    
    for tok in tokens:
      self.token(tok)
      
  def token(self, tok):
    if isinstance(tok, Text):
      for word in tok.text.split():
        word = word.replace("&lt;", "<")
        word = word.replace("&gt;", ">")
        
        font = tkinter.font.Font(
          size=self.size,
          weight=self.weight,
          slant=self.style,
        )
        w = font.measure(word)
        self.display_list.append((self.cursor_x, self.cursor_y, word, font))
        self.cursor_x += w + font.measure(" ")
        
        if self.cursor_x + w > WIDTH - HSTEP:
          self.cursor_y += font.metrics('linespace') * 1.25
          self.cursor_x = HSTEP
    
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