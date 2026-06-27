# Eligy

Eligy est un simulateur indicatif d’éligibilité aux aides sociales. Le questionnaire React collecte la situation de l’utilisateur, envoie le profil à une API FastAPI, puis affiche le résultat détaillé du moteur de règles.

Le prototype couvre actuellement :

- la prime d’activité ;
- l’aide médicale de l’État (AME) ;
- les allocations familiales.

> Les résultats sont indicatifs. Les règles et seuils doivent être validés et maintenus à partir de sources administratives officielles avant toute mise en production.

## Lancer le projet

### API

Depuis la racine du dépôt :

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r Requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

L’API est disponible sur `http://127.0.0.1:8000`. Sa documentation interactive se trouve sur `http://127.0.0.1:8000/docs`.

### Interface

Dans un second terminal :

```powershell
cd allocs
npm install
npm run dev
```

Ouvrir ensuite `http://localhost:5173`. Le serveur Vite transmet automatiquement les appels `/api` à FastAPI.

## Vérifications

```powershell
.\.venv\Scripts\python.exe -m pytest -q
cd allocs
npm run lint
npm run build
```

## Structure

- `app/api` : endpoints HTTP FastAPI ;
- `app/core` : moteur de règles et adaptation du profil ;
- `app/models` : schémas Pydantic et configuration des aides ;
- `app/tests` : scénarios métier automatisés ;
- `allocs/src` : questionnaire et rendu des résultats React.
