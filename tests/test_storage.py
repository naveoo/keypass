from rich import print
import pytest
from src.core.storage import Database

@pytest.fixture
def db_instance():
    """Fixture pour initialiser et nettoyer la base de données."""
    db = Database()
    db.cursor.execute(f"DELETE FROM {db.PASSWORD_TABLE_NAME}")
    db.conn.commit()
    print("[bold red]Table nettoyée avant le test.[/]")
    yield db
    del db 

def test_database_initialization(db_instance):
    """Test l'initialisation de la base de données."""
    print("[bold green]Test de l'initialisation de la base de données[/]")
    assert db_instance.cursor is not None
    assert db_instance.conn is not None

def test_insert_and_get_info(db_instance):
    """Test l'insertion et la récupération d'informations."""
    test_data = ("TestApp", "user123", "password123")
    db_instance.insert(test_data)
    
    print(f"[bold cyan]Données insérées :[/] {test_data}")
    
    result = db_instance.get_info("TestApp")
    print(f"[bold cyan]Résultat récupéré :[/] {result}")
    
    assert len(result) == 1
    assert result[0][0] == "user123"
    assert result[0][1] == "password123"

def test_get_applications(db_instance):
    """Test la récupération des applications."""
    test_data = [("App1", "user1", "password1"), ("App2", "user2", "password2")]
    for data in test_data:
        db_instance.insert(data)
    
    print(f"[bold yellow]Applications insérées :[/] {[d[0] for d in test_data]}")
    
    applications = db_instance.get_applications()
    print(f"[bold yellow]Applications récupérées :[/] {applications}")
    
    assert "App1" in applications
    assert "App2" in applications

def test_invalid_application_request(db_instance):
    """Test une demande pour une application inexistante."""
    result = db_instance.get_info("NonExistentApp")
    print(f"[bold magenta]Résultat pour une application inexistante :[/] {result}")
    assert result == []
def test_delete_entry_by_id(db_instance):
    test_data = [("App1", "user1", "password1"), ("App2", "user2", "password2")]
    for data in test_data:
        db_instance.insert(data)
    
    db_instance.cursor.execute(f"SELECT id FROM {db_instance.PASSWORD_TABLE_NAME} WHERE application = ?", ("App1",))
    entry_id = db_instance.cursor.fetchone()[0]
    
    print(f"[bold green]ID récupéré pour suppression :[/] {entry_id}")
    
    db_instance.delete_entry_by_id(entry_id)
    
    db_instance.cursor.execute(f"SELECT * FROM {db_instance.PASSWORD_TABLE_NAME} WHERE id = ?", (entry_id,))
    result = db_instance.cursor.fetchone()
    
    print(f"[bold yellow]Résultat après suppression de l'entrée (doit être None) :[/] {result}")
    assert result is None
def test_close_connection(db_instance):
    """Test la fermeture de la connexion à la base de données."""
    del db_instance
    print("[bold green]Connexion à la base de données fermée correctement[/]")