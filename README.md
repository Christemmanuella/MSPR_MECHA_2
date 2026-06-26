# MSPR MECHA 2

## Présentation

MSPR MECHA 2 est une plateforme de maintenance prédictive industrielle développée dans le cadre du projet MSPR.

L'objectif est de prédire les risques de panne des machines industrielles grâce à un modèle d'intelligence artificielle intégré à une API FastAPI et visualisé au travers d'un dashboard React.

Le projet repose sur plusieurs composants :

- API REST FastAPI
- Modèle de Machine Learning
- Base de données PostgreSQL
- Dashboard React / TypeScript
- Documentation Swagger
- Docker

---

# Architecture du projet

```
MSPR_MECHA_2
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── requirements.txt
│   └── .env
│
├── database/
│   ├── init_db.sql
│
├── mecha_dashboard_MSPR/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
│
└── README.md
```

---

# Technologies utilisées

## Backend

- Python
- FastAPI
- TensorFlow
- Keras
- XGBoost
- SQLAlchemy
- PostgreSQL

## Frontend

- React
- TypeScript
- Tailwind CSS
- Recharts
- Vite

## Outils

- Docker
- Swagger
- Git
- GitHub

---

# Installation

## 1. Cloner le dépôt

```bash
git clone https://github.com/Christemmanuella/MSPR_MECHA_2.git

cd MSPR_MECHA_2
```

---

## 2. Créer un environnement virtuel

```bash
python -m venv venv
```

Activation sous Windows

```bash
venv\Scripts\activate
```

---

## 3. Installer les dépendances

```bash
pip install -r backend/requirements.txt
```

---

## 4. Configurer les variables d'environnement

Créer le fichier

```
backend/.env
```

Ajouter :

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mspr_mecha

MODEL_PATH=models/lstm_model.keras

SCALER_PATH=models/scaler.pkl

ENCODER_OPERATION_PATH=models/label_encoder_operation.pkl

ENCODER_EFFICIENCY_PATH=models/label_encoder_efficiency.pkl

FEATURE_COLS_PATH=models/feature_cols.txt
```

---

# PostgreSQL avec Docker

Lancer PostgreSQL :

```bash
docker compose up -d
```

Vérifier le conteneur :

```bash
docker ps
```

---

# Initialisation de la base de données

Créer automatiquement les tables SQL :

```bash
python -m backend.app.init_db
```

Les tables créées sont :

- predictions
- alerts

---

# Lancer le Backend

Depuis la racine du projet :

```bash
uvicorn backend.app.main:app --reload
```

L'API est disponible à l'adresse :

```
http://127.0.0.1:8000
```

---

# Documentation Swagger

FastAPI génère automatiquement la documentation interactive.

Accès :

```
http://127.0.0.1:8000/docs
```

Swagger permet de :

- tester les endpoints ;
- envoyer des requêtes ;
- visualiser les réponses JSON ;
- vérifier les codes HTTP.

Routes principales :

```
GET /health

POST /predict
```

---

# Lancer le Frontend

Se placer dans le dossier du dashboard :

```bash
cd mecha_dashboard_MSPR
```

Installer les dépendances :

```bash
npm install
```

Lancer le serveur de développement :

```bash
npm run dev
```

Le dashboard est accessible sur :

```
http://localhost:5173
```

---

# Fonctionnalités

Le dashboard permet de :

- superviser les machines industrielles ;
- afficher les indicateurs de production ;
- suivre les consommations énergétiques ;
- afficher les émissions de CO₂ ;
- analyser une machine avec l'intelligence artificielle ;
- prédire un risque de panne ;
- recommander une action de maintenance ;
- créer un ticket d'intervention ;
- enregistrer automatiquement les prédictions dans PostgreSQL.

---

# Fonctionnement de l'intelligence artificielle

Le processus d'analyse est le suivant :

1. L'utilisateur sélectionne une machine.
2. Les données de la machine sont récupérées.
3. Le frontend envoie une requête POST à FastAPI.
4. Le backend prépare les données.
5. Le modèle de Machine Learning réalise la prédiction.
6. Le résultat est enregistré dans PostgreSQL.
7. Le dashboard affiche :
   - le niveau de risque ;
   - la probabilité de panne ;
   - une recommandation de maintenance.

---

# Dashboard

Le dashboard comprend plusieurs modules :

- Vue générale
- Production
- Maintenance
- Énergie
- Modèles prédictifs
- Plan interactif de l'usine
- Analyse détaillée d'une machine

Chaque machine peut être analysée individuellement grâce au bouton **Analyser avec l'IA**.

---

# Base de données

Deux tables principales sont utilisées.

## predictions

Historique des prédictions réalisées par le modèle.

## alerts

Historique des alertes critiques générées automatiquement.

---

# Dépôts GitHub

Projet Backend :

https://github.com/Christemmanuella/MSPR_MECHA_2

Dashboard Frontend :

https://github.com/momodevfullstack/mecha_dashboard_MSPR

---

# Auteur

Projet réalisé dans le cadre du MSPR.

Développé par :

Oulimata Diedhiou

---

# Licence

Projet réalisé dans un cadre pédagogique.