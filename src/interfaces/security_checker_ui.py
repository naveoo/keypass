import wx

from src.core.utils import evaluate_password_strength, get_strength_label


class SecurityCheckerFrame(wx.Dialog):

    COLORS = {
        5: wx.Colour(0, 150, 0),    # Vert foncé
        4: wx.Colour(100, 180, 0),   # Vert clair
        3: wx.Colour(200, 150, 0),   # Orange
        2: wx.Colour(200, 100, 0),   # Orange foncé
    }
    DEFAULT_COLOR = wx.Colour(200, 0, 0)

    def __init__(self, parent, password: str):
        super().__init__(parent, title="Vérification de la sécurité", size=(400, 200))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        score = evaluate_password_strength(password)
        label = get_strength_label(score)

        self.result_text = wx.StaticText(panel, label=label)
        self.result_text.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        )
        color = self.COLORS.get(score, self.DEFAULT_COLOR)
        self.result_text.SetForegroundColour(color)

        self.gauge = wx.Gauge(panel, range=5, size=(-1, 20))
        self.gauge.SetValue(score)

        score_text = wx.StaticText(panel, label=f"Score : {score}/5")

        vbox.Add(self.result_text, flag=wx.EXPAND | wx.ALL, border=15)
        vbox.Add(self.gauge, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)
        vbox.Add(score_text, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        close_btn = wx.Button(panel, id=wx.ID_CLOSE, label="Fermer")
        close_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
        vbox.Add(close_btn, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)
