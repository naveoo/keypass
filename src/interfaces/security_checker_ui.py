import wx
import re

class SecurityCheckerFrame(wx.Dialog):
    def __init__(self, parent, password):
        super().__init__(parent, title="Vérification de la sécurité", size=(400, 250))

        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.password = password
        self.result_text = wx.StaticText(self.panel, label="")
        
        self.analyze_password()

        vbox.Add(self.result_text, flag=wx.EXPAND | wx.ALL, border=10)
        self.panel.SetSizer(vbox)

    def analyze_password(self):
        score = self.get_security_score(self.password)
        if score == 5:
            self.result_text.SetLabel("Mot de passe très sécurisé !")
        elif score == 4:
            self.result_text.SetLabel("Mot de passe sécurisé.")
        elif score == 3:
            self.result_text.SetLabel("Mot de passe moyen.")
        elif score == 2:
            self.result_text.SetLabel("Mot de passe faible.")
        else:
            self.result_text.SetLabel("Mot de passe très faible.")

    def get_security_score(self, password):
        score = 0
        if len(password) >= 8:
            score += 1
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"\d", password):
            score += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
        return score
