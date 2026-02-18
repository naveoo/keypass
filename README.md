<p align="center">
  <img src="logo.ico" alt="KeyPass Logo" width="80" />
</p>

<h1 align="center">KeyPass</h1>

<p align="center">
  <strong>Gestionnaire de mots de passe local, sécurisé et léger</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="Licence MIT" />
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?logo=windows" alt="Windows" />
  <img src="https://img.shields.io/badge/GUI-wxPython-orange" alt="wxPython" />
</p>

---

## 📋 Présentation

**KeyPass** est un gestionnaire de mots de passe **100% local** conçu pour stocker, générer et évaluer vos mots de passe en toute sécurité. Aucune donnée ne quitte votre machine — tout est chiffré et stocké dans une base SQLite locale, protégée par un mot de passe maître.

### Fonctionnalités principales

- 🔐 **Chiffrement AES-256** via Fernet (bibliothèque `cryptography`)
- 🔑 **Dérivation de clé PBKDF2-HMAC-SHA256** — 480 000 itérations (recommandation OWASP)
- 🗄️ **Stockage local SQLite** — aucune connexion réseau requise
- 🎲 **Générateur de mots de passe sécurisé** — utilise `secrets` (CSPRNG)
- 🛡️ **Évaluation de la robustesse** — score de sécurité avec jauge visuelle
- 📋 **Copie dans le presse-papier** en un clic
- 💻 **Interface graphique native** avec wxPython
- 📦 **Empaquetable en `.exe`** via PyInstaller

---

## 🏗️ Architecture

```
keypass/
├── main.py                          # Point d'entrée
├── src/
│   ├── core/
│   │   ├── crypto.py                # Chiffrement, dérivation de clé, vérification
│   │   ├── password_generator.py    # Génération sécurisée de mots de passe
│   │   ├── storage.py               # Accès base de données SQLite
│   │   └── utils.py                 # Évaluation de la force des mots de passe
│   ├── db/
│   │   └── database.db              # Base de données (générée automatiquement)
│   └── interfaces/
│       ├── gui.py                   # Fenêtres de connexion et principale
│       ├── password_generator_ui.py # Interface du générateur
│       └── security_checker_ui.py   # Interface du vérificateur de sécurité
├── logo.ico                         # Icône de l'application
├── requirements.txt                 # Dépendances Python
└── .env                             # Configuration (longueurs min/max)
```

---

## ⚙️ Installation

### Prérequis

- **Python 3.10+**
- **pip** (gestionnaire de paquets Python)

### Mise en place

```bash
# Cloner le dépôt
git clone https://github.com/<votre-utilisateur>/keypass.git
cd keypass

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Windows (CMD)
.\venv\Scripts\activate.bat

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration

Le fichier `.env` permet de configurer les contraintes de longueur des mots de passe :

```env
APP_NAME=Keypass
APP_ENV=production

PASSWORD_MIN_SIZE=12
PASSWORD_MAX_SIZE=50
```

---

## 🚀 Utilisation

### Lancer l'application

```bash
python main.py
```

### Premier lancement

1. Une fenêtre de connexion s'affiche
2. **Choisissez votre mot de passe maître** — il sera utilisé pour chiffrer toutes vos données
3. Ce mot de passe ne peut **pas être récupéré** en cas d'oubli

### Fonctionnalités

| Action | Description |
|--------|-------------|
| **Ajouter** | Enregistrer un mot de passe pour une application |
| **Afficher** | Déchiffrer et afficher un mot de passe stocké |
| **Supprimer** | Retirer une entrée de la base |
| **Générer** | Créer un mot de passe aléatoire sécurisé |
| **Vérifier** | Évaluer la robustesse d'un mot de passe existant |

---

## 📦 Créer un exécutable

Pour distribuer l'application sans nécessiter Python :

```bash
pip install pyinstaller
pyinstaller main.spec
```

L'exécutable sera généré dans le dossier `dist/`. En mode packagé, les données utilisateur (base de données, salt) sont stockées dans `%APPDATA%/KeyPass/`.

---

## 🔒 Sécurité

| Aspect | Implémentation |
|--------|----------------|
| **Algorithme de chiffrement** | AES-256 via Fernet |
| **Dérivation de clé** | PBKDF2-HMAC-SHA256, 480 000 itérations |
| **Salt** | 16 octets aléatoires, unique par installation |
| **Génération aléatoire** | Module `secrets` (CSPRNG du système) |
| **Stockage** | SQLite local, mots de passe chiffrés au repos |
| **Vérification maître** | Token chiffré, aucun mot de passe stocké en clair |

> **⚠️ Important** : Le mot de passe maître est la seule protection de vos données. En cas de perte, les mots de passe stockés ne pourront **pas** être récupérés.

---

## 🛠️ Technologies

| Technologie | Rôle |
|-------------|------|
| [Python 3.10+](https://www.python.org/) | Langage principal |
| [wxPython](https://wxpython.org/) | Interface graphique native |
| [cryptography](https://cryptography.io/) | Chiffrement et dérivation de clé |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gestion des variables d'environnement |
| [SQLite](https://www.sqlite.org/) | Base de données embarquée |
| [PyInstaller](https://pyinstaller.org/) | Empaquetage en exécutable |

---

## 📄 Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<p align="center">
  Développé avec ❤️ en Python
</p>
