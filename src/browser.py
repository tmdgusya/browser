import tkinter

from .url import URL

class Browser:
  def __init__(self) -> None:
    self.WIDTH, self.HEIGHT = 800, 600
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
    self.canvas.pack()
    
  def load(self, url: URL):
    HSTEP, VSTEP = 13, 18

    text = url.load()
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
      self.canvas.create_text(cursor_x, cursor_y, text=c)
      cursor_x += HSTEP
      if cursor_x >= self.WIDTH - HSTEP:
        cursor_y += VSTEP
        cursor_x = HSTEP

if __name__ == "__main__":
  import sys
  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()