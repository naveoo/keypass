import wx
import sys
import os
from pathlib import Path

from src.core.crypto import (
    derive_key,
    is_first_run,
    store_master_verification,
    verify_master_password,
)
from src.core.storage import Database
from src.interfaces.password_generator_ui import PasswordGeneratorFrame
from src.interfaces.security_checker_ui import SecurityCheckerFrame


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class LoginFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Connexion sécurisée", size=(350, 200))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.password_label = wx.StaticText(panel, label="Mot de passe maître :")
        self.password_input = wx.TextCtrl(panel, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.password_input.Bind(wx.EVT_TEXT_ENTER, self.on_login)

        self.login_button = wx.Button(panel, label="Connexion")
        self.login_button.Bind(wx.EVT_BUTTON, self.on_login)

        self.error_text = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER)
        self.error_text.SetForegroundColour(wx.RED)

        if is_first_run():
            info = wx.StaticText(
                panel,
                label="Première utilisation : choisissez votre mot de passe maître.",
                style=wx.ALIGN_CENTER,
            )
            info.SetForegroundColour(wx.Colour(0, 100, 200))
            vbox.Add(info, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add(self.password_label, flag=wx.ALL, border=10)
        vbox.Add(self.password_input, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        vbox.Add(self.login_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        vbox.Add(self.error_text, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        panel.SetSizer(vbox)
        self.Centre()

    def on_login(self, event):
        password = self.password_input.GetValue().strip()

        if not password:
            self.error_text.SetLabel("Veuillez entrer un mot de passe.")
            return

        try:
            key = derive_key(password)

            if is_first_run():
                store_master_verification(key)
            elif not verify_master_password(key):
                self.error_text.SetLabel("Mot de passe invalide.")
                self.password_input.SetValue("")
                return

            self.Hide()
            db = Database(key)
            main_frame = MainFrame(None, db)
            main_frame.Show()

        except Exception as e:
            wx.MessageBox(
                f"Erreur : {e}",
                "Erreur lors de la connexion",
                wx.OK | wx.ICON_ERROR,
            )
            self.error_text.SetLabel("Erreur de clé ou accès à la base.")
            self.password_input.SetValue("")


class MainFrame(wx.Frame):

    def __init__(self, parent, db: Database):
        super().__init__(parent, title="Gestionnaire de mots de passe", size=(600, 500))
        self.db = db

        try:
            self.SetIcon(wx.Icon(resource_path("logo.ico")))
        except Exception:
            pass

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.app_list = wx.ListBox(panel, size=(500, 200))
        self.load_apps()

        buttons = [
            ("Ajouter un mot de passe", self.on_add_password),
            ("Générer un mot de passe", self.on_generate_password),
            ("Supprimer l'entrée", self.on_delete_password),
            ("Afficher le mot de passe", self.on_show_password),
            ("Vérifier la sécurité", self.on_check_security),
        ]

        vbox.Add(self.app_list, flag=wx.EXPAND | wx.ALL, border=10)
        for label, handler in buttons:
            btn = wx.Button(panel, label=label)
            btn.Bind(wx.EVT_BUTTON, handler)
            vbox.Add(btn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)
        self.Centre()

    def load_apps(self):
        applications = self.db.get_applications()
        self.app_list.Set(applications)

    def on_add_password(self, event):
        dialog = wx.TextEntryDialog(
            self,
            "Format : application, utilisateur, mot de passe",
            "Ajouter un mot de passe",
        )
        if dialog.ShowModal() == wx.ID_OK:
            data = [item.strip() for item in dialog.GetValue().split(",")]
            if len(data) != 3:
                wx.MessageBox(
                    "Format incorrect. Utilisez : application, utilisateur, mot de passe",
                    "Erreur",
                    wx.OK | wx.ICON_ERROR,
                )
                return
            application, userid, password = data
            if not all([application, userid, password]):
                wx.MessageBox(
                    "Tous les champs doivent être remplis.",
                    "Erreur",
                    wx.OK | wx.ICON_ERROR,
                )
                return
            self.db.insert(application, userid, password)
            self.load_apps()
        dialog.Destroy()

    def on_generate_password(self, event):
        dialog = PasswordGeneratorFrame(self)
        dialog.ShowModal()
        dialog.Destroy()

    def on_delete_password(self, event):
        selected_app = self.app_list.GetStringSelection()
        if not selected_app:
            wx.MessageBox(
                "Veuillez sélectionner une application.",
                "Erreur",
                wx.OK | wx.ICON_ERROR,
            )
            return

        users = self.db.get_users_for_application(selected_app)
        if not users:
            wx.MessageBox("Aucun utilisateur trouvé.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        dialog = wx.SingleChoiceDialog(
            self,
            f"Choisir l'utilisateur à supprimer pour '{selected_app}' :",
            "Supprimer un mot de passe",
            users,
        )
        if dialog.ShowModal() == wx.ID_OK:
            selected_user = dialog.GetStringSelection()
            confirm = wx.MessageBox(
                f"Supprimer l'entrée de '{selected_user}' pour '{selected_app}' ?",
                "Confirmation",
                wx.YES_NO | wx.ICON_QUESTION,
            )
            if confirm == wx.YES:
                try:
                    self.db.delete_entry_by_app_and_user(selected_app, selected_user)
                    wx.MessageBox("Entrée supprimée.", "Succès", wx.OK | wx.ICON_INFORMATION)
                    self.load_apps()
                except (ValueError, RuntimeError) as e:
                    wx.MessageBox(str(e), "Erreur", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def on_show_password(self, event):
        selected_app = self.app_list.GetStringSelection()
        if not selected_app:
            wx.MessageBox(
                "Veuillez sélectionner une application.",
                "Erreur",
                wx.OK | wx.ICON_ERROR,
            )
            return

        data = self.db.get_info(selected_app)
        if not data:
            wx.MessageBox("Aucune donnée trouvée.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        message = "\n".join(
            f"Utilisateur : {uid}\nMot de passe : {pwd}\n"
            for uid, pwd in data
        )
        wx.MessageBox(message, f"Informations — {selected_app}", wx.OK | wx.ICON_INFORMATION)

    def on_check_security(self, event):
        selected_app = self.app_list.GetStringSelection()
        if not selected_app:
            wx.MessageBox(
                "Veuillez sélectionner une application.",
                "Erreur",
                wx.OK | wx.ICON_ERROR,
            )
            return

        data = self.db.get_info(selected_app)
        if not data:
            wx.MessageBox("Aucune donnée trouvée.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        password = data[0][1]
        dialog = SecurityCheckerFrame(self, password)
        dialog.ShowModal()
        dialog.Destroy()