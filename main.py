import wx
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from src.interfaces.gui import LoginFrame

if __name__ == "__main__":
    app = wx.App(False)
    frame = LoginFrame()
    frame.Show()
    app.MainLoop()