import wx
from src.interfaces.gui import LoginFrame


def main():
    app = wx.App(False)
    frame = LoginFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()