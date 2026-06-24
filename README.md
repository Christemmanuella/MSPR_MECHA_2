# MSPR MECHA 2

Projet de maintenance prédictive industrielle.

## Technologies

- Python
- FastAPI
- TensorFlow / Keras
- XGBoost
- PostgreSQL
- Docker
- Swagger

## Lancement

Créer un environnement virtuel :

```bash
python -m venv venv
Installer les dépendances :

pip install -r backend/requirements.txt

Lancer Docker :

docker compose up -d

Créer les tables :

python -m backend.app.init_db

Lancer l'API :

uvicorn backend.app.main:app --reload

Swagger :

http://127.0.0.1:8000/docs

On l'améliorera plus tard pour le rendu final.

---

# Étape 3 — Initialiser Git

Depuis ton terminal :

```bash
git init