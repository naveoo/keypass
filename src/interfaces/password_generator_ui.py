import wx
from secrets import choice
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

from src.core.password_generator import PASSWORD_MIN_SIZE, PASSWORD_MAX_SIZE


class PasswordGeneratorFrame(wx.Dialog):
    """Dialogue de génération de mot de passe sécurisé."""

    def __init__(self, parent):
        super().__init__(parent, title="Générateur de mot de passe", size=(420, 380))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Longueur
        self.length_label = wx.StaticText(
            panel, label=f"Longueur ({PASSWORD_MIN_SIZE}–{PASSWORD_MAX_SIZE}) :"
        )
        self.length_input = wx.SpinCtrl(
            panel,
            value=str(PASSWORD_MIN_SIZE),
            min=PASSWORD_MIN_SIZE,
            max=PASSWORD_MAX_SIZE,
        )

        # Options
        self.include_uppercase = wx.CheckBox(panel, label="Inclure des majuscules")
        self.include_uppercase.SetValue(True)
        self.include_digits = wx.CheckBox(panel, label="Inclure des chiffres")
        self.include_digits.SetValue(True)
        self.include_symbols = wx.CheckBox(panel, label="Inclure des symboles")

        # Bouton et résultat
        self.generate_button = wx.Button(panel, label="Générer")
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

        self.password_display = wx.TextCtrl(
            panel, style=wx.TE_READONLY | wx.TE_CENTRE, size=(-1, 30)
        )
        self.password_display.SetFont(
            wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        )

        self.copy_button = wx.Button(panel, label="Copier dans le presse-papier")
        self.copy_button.Bind(wx.EVT_BUTTON, self.on_copy)
        self.copy_button.Disable()

        # Layout
        vbox.Add(self.length_label, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.length_input, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        vbox.Add(self.include_uppercase, flag=wx.EXPAND | wx.ALL, border=8)
        vbox.Add(self.include_digits, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=8)
        vbox.Add(self.include_symbols, flag=wx.EXPAND | wx.ALL, border=8)
        vbox.Add(self.generate_button, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.password_display, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        vbox.Add(self.copy_button, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

    def on_generate(self, event):
        """Génère un mot de passe avec les options sélectionnées."""
        length = self.length_input.GetValue()
        include_upper = self.include_uppercase.IsChecked()
        include_dig = self.include_digits.IsChecked()
        include_sym = self.include_symbols.IsChecked()

        # Construire le pool de caractères
        pool = ascii_lowercase  # Toujours inclure les minuscules
        required: list[str] = [choice(ascii_lowercase)]

        if include_upper:
            pool += ascii_uppercase
            required.append(choice(ascii_uppercase))
        if include_dig:
            pool += digits
            required.append(choice(digits))
        if include_sym:
            pool += punctuation
            required.append(choice(punctuation))

        # Remplir le reste
        remaining = length - len(required)
        if remaining < 0:
            remaining = 0
        password_chars = required + [choice(pool) for _ in range(remaining)]

        # Mélange sécurisé (Fisher-Yates avec secrets)
        from secrets import randbelow
        for i in range(len(password_chars) - 1, 0, -1):
            j = randbelow(i + 1)
            password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

        password = "".join(password_chars)
        self.password_display.SetValue(password)
        self.copy_button.Enable()

    def on_copy(self, event):
        """Copie le mot de passe dans le presse-papier."""
        password = self.password_display.GetValue()
        if password and wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(password))
            wx.TheClipboard.Close()
            wx.MessageBox("Mot de passe copié !", "Info", wx.OK | wx.ICON_INFORMATION)
