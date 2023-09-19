import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app


def test_index_route():
    response = app.test_client().get("/")
    assert "Bienvenue sur notre plateforme" in response.text
    assert response.status_code == 200


def test_chose_words_route():
    response = app.test_client().get("/chose_words/")
    assert "Mots à inclure dans le poème" in response.text
    assert response.status_code == 200


def test_chosen_words_route():
    data = {"word1": "chat", "word2": "chien", "word3": "table"}
    response = app.test_client().post("/chosen_words/", data=data)
    assert "Longueur du poème" in response.text
    assert response.status_code == 200


def test_generate_poem_route():
    with app.test_client() as c:
        with c.session_transaction() as session:
            session["word1"] = "chat"
            session["word2"] = "chien"
            session["word3"] = "table"
        response = c.post(
            "/generate_poem/",
            data={"poem": "je suis un poème", "vers": "5 vers"},
            subdomain="blue",
        )
        assert "Voici le poème généré pour les mots" in response.text
        assert response.status_code == 200
