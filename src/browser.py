import tkinter
import tkinter.font

from src.layout import Layout

from .url import URL, Tag, Text

class Browser:
  def __init__(self) -> None:
    self.WIDTH, self.HEIGHT = 800, 600
    self.HSTEP, self.VSTEP = 13, 18
    self.SCROLL_STEP = 100
    self.display_list = []
    self.scroll = 0
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
    self.canvas.pack()

    # key binding
    self.window.bind("<Down>", self.scrolldown)
    
  def scrolldown(self, e):
    self.scroll += self.SCROLL_STEP
    self.draw()
    
  def load(self, url: URL):
    tokens = url.lex()
    self.display_list = Layout(tokens).display_list
    self.draw()
    
  def draw(self):
    self.canvas.delete("all")
    for cursor_x, cursor_y, c, f in self.display_list:
      if cursor_y > self.scroll + self.HEIGHT: continue
      if cursor_y + self.VSTEP < self.scroll: continue
      if isinstance(c, Tag):
        text_content = c.tag
      elif isinstance(c, Text):
        text_content = c.text
      else:
        text_content = str(c)
      self.canvas.create_text(cursor_x, cursor_y - self.scroll, text=text_content, anchor="nw", font=f)


if __name__ == "__main__":
  import sys
  browser = Browser()
  browser.load(URL(sys.argv[1]))
  browser.draw()
  tkinter.mainloop()