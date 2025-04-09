import wx
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.core.crypto import derive_key
from src.core.storage import Database
from src.interfaces.password_generator_ui import PasswordGeneratorFrame
from src.interfaces.security_checker_ui import SecurityCheckerFrame

class LoginFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Connexion sécurisée", size=(350, 180))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.password_label = wx.StaticText(panel, label="Mot de passe maître :")
        self.password_input = wx.TextCtrl(panel, style=wx.TE_PASSWORD)

        self.login_button = wx.Button(panel, label="Connexion")
        self.login_button.Bind(wx.EVT_BUTTON, self.on_login)

        self.error_text = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER)
        self.error_text.SetForegroundColour(wx.RED)

        vbox.Add(self.password_label, flag=wx.ALL, border=10)
        vbox.Add(self.password_input, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        vbox.Add(self.login_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        vbox.Add(self.error_text, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def on_login(self, event):
        password = self.password_input.GetValue()

        if not password:
            self.error_text.SetLabel("Veuillez entrer un mot de passe.")
            return

        try:
            key = derive_key(password)
            print("Clé dérivée avec succès:", key)

            self.Hide()

            self.db = Database(key)

            self.main = MainFrame(None, self.db)
            self.main.Show()

        except Exception as e:
            self.error_text.SetLabel("Erreur de clé ou accès à la base.")
            self.password_input.SetValue("")



class MainFrame(wx.Frame):
    def __init__(self, parent, db):
        super().__init__(parent, title="Gestionnaire de mots de passe", size=(600, 500))
        self.db = db

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.app_list = wx.ListBox(panel, size=(500, 200))
        self.load_apps()

        self.add_button = wx.Button(panel, label="Ajouter un mot de passe")
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_password)

        self.generate_button = wx.Button(panel, label="Générer un mot de passe")
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate_password)

        self.delete_button = wx.Button(panel, label="Supprimer l'entrée")
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete_password)

        self.show_button = wx.Button(panel, label="Afficher le mot de passe")
        self.show_button.Bind(wx.EVT_BUTTON, self.on_show_password)

        self.check_security_button = wx.Button(panel, label="Vérifier la sécurité du mot de passe")
        self.check_security_button.Bind(wx.EVT_BUTTON, self.on_check_security)

        vbox.Add(self.app_list, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        vbox.Add(self.add_button, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.generate_button, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.delete_button, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.show_button, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.check_security_button, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.Centre()

    def load_apps(self):
        applications = self.db.get_applications()
        self.app_list.Set([app for app in applications])

    def on_add_password(self, event):
        dialog = wx.TextEntryDialog(self, "Application et utilisateur, mot de passe (séparés par des virgules)", "Ajouter un mot de passe", "")
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.GetValue().split(",")
            if len(data) == 3:
                self.db.insert(tuple(data))
                self.load_apps()

    def on_generate_password(self, event):
        dialog = PasswordGeneratorFrame(self)
        dialog.ShowModal()

    def on_delete_password(self, event):
        selected_app = self.app_list.GetStringSelection()

        if not selected_app:
            wx.MessageBox("Veuillez sélectionner une application.", "Erreur", wx.OK | wx.ICON_ERROR)
            return

        dialog = wx.TextEntryDialog(self, "Entrez l'utilisateur à supprimer:", "Supprimer un mot de passe", "")
        if dialog.ShowModal() == wx.ID_OK:
            selected_user = dialog.GetValue()

            if not selected_user:
                wx.MessageBox("Veuillez entrer un utilisateur.", "Erreur", wx.OK | wx.ICON_ERROR)
                return

            try:
                self.db.delete_entry_by_app_and_user(selected_app, selected_user)
                wx.MessageBox("Entrée supprimée avec succès.", "Succès", wx.OK | wx.ICON_INFORMATION)
                self.load_apps()
            except ValueError as e:
                wx.MessageBox(str(e), "Erreur", wx.OK | wx.ICON_ERROR)

    def on_show_password(self, event):
        selected_app = self.app_list.GetStringSelection()
        if selected_app:
            data = self.db.get_info(selected_app)
            if data:
                userid, password = data[0]
                dialog = wx.MessageDialog(self, f"Utilisateur: {userid}\nMot de passe: {password}", "Informations", wx.OK)
                dialog.ShowModal()

    def on_check_security(self, event):
        selected_app = self.app_list.GetStringSelection()
        if selected_app:
            data = self.db.get_info(selected_app)
            if data:
                password = data[0][1]
                dialog = SecurityCheckerFrame(self, password)
                dialog.ShowModal()
