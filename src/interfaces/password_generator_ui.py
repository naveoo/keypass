import wx
import random
import string

from src.core.utils import evaluate_password_strength

class PasswordGeneratorFrame(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Générateur de mot de passe", size=(400, 400))

        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.length_label = wx.StaticText(self.panel, label="Longueur du mot de passe:")
        self.length_input = wx.TextCtrl(self.panel, value="12", style=wx.TE_CENTRE)

        self.include_uppercase = wx.CheckBox(self.panel, label="Inclure des majuscules")
        self.include_digits = wx.CheckBox(self.panel, label="Inclure des chiffres")
        self.include_symbols = wx.CheckBox(self.panel, label="Inclure des symboles")

        self.generate_button = wx.Button(self.panel, label="Générer")
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

        self.password_display = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE)

        vbox.Add(self.length_label, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.length_input, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.include_uppercase, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.include_digits, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.include_symbols, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.generate_button, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.password_display, flag=wx.EXPAND | wx.ALL, border=10)

        self.panel.SetSizer(vbox)

    def on_generate(self, event):
        length = int(self.length_input.GetValue())
        include_uppercase = self.include_uppercase.IsChecked()
        include_digits = self.include_digits.IsChecked()
        include_symbols = self.include_symbols.IsChecked()

        password = self.generate_password(length, include_uppercase, include_digits, include_symbols)
        self.password_display.SetValue(password)

    def generate_password(self, length, include_uppercase, include_digits, include_symbols):
        characters = string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_digits:
            characters += string.digits
        if include_symbols:
            characters += string.punctuation

        return ''.join(random.choice(characters) for _ in range(length))
    def on_check_security(self, event):
        password = self.password_input.GetValue()
        issues = evaluate_password_strength(password)

        if issues:
            security_message = "Mot de passe faible :"
            for issue in issues:
                security_message += f"\n - {issue}"
        else:
            security_message = "Mot de passe fort!"

        self.security_label.SetLabel(security_message)
