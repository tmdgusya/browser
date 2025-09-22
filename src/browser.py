import tkinter

from .url import URL

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
    
  def layout(self, text):
    cursor_x, cursor_y = self.HSTEP, self.VSTEP
    for c in text:
      self.display_list.append((cursor_x, cursor_y, c))
      cursor_x += self.HSTEP
      if cursor_x >= self.WIDTH - self.HSTEP:
        cursor_y += self.VSTEP
        cursor_x = self.HSTEP
    
    return self.display_list
  
  def load(self, url: URL):
    text = url.load()
    self.layout(text=text)
    
  def draw(self):
    self.canvas.delete("all")
    for cursor_x, cursor_y, c in self.display_list:
      if cursor_y > self.scroll + self.HEIGHT: continue
      if cursor_y + self.VSTEP < self.scroll: continue
      self.canvas.create_text(cursor_x, cursor_y - self.scroll, text=c)


if __name__ == "__main__":
  import sys
  browser = Browser()
  browser.load(URL(sys.argv[1]))
  browser.draw()
  tkinter.mainloop()