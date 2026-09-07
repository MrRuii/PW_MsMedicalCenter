# MS Medical Center

Applicazione full-stack per la gestione di un centro medico: prenotazione visite, agenda dei medici, referti clinici e dashboard economica. Progetto realizzato per il Project Work del CdS Informatica per le Aziende Digitali (L-31), traccia PW 16.

## Stack

**Backend**: Python, FastAPI, SQLAlchemy, SQLite, autenticazione JWT (PyJWT), password hashate con bcrypt.

**Frontend**: Vue 3 + TypeScript, Vite, Pinia, Vue Router, Axios, Tailwind CSS, Chart.js.

## Struttura

```
backend/    API REST (routers, services, repositories, models, schemas)
frontend/   interfaccia web (viste per paziente, medico, admin)
docs/       diagrammi UML/ER e schema OpenAPI
```

## Avvio del progetto

### Backend

Richiede [uv](https://docs.astral.sh/uv/).

```
cd backend
uv sync
copy .env.example .env      # su Windows; su Linux/Mac: cp .env.example .env
uv run python seed.py       # crea il database con dati di esempio
uv run uvicorn main:app --reload
```

Il backend parte su `http://127.0.0.1:8000`. La documentazione interattiva (Swagger) è su `http://127.0.0.1:8000/docs`.

### Frontend

Richiede Node.js.

```
cd frontend
npm install
copy .env.example .env      # su Windows; su Linux/Mac: cp .env.example .env
npm run dev
```

Il frontend parte su `http://localhost:5173`.

## Credenziali di test

Password per tutti gli utenti creati dal seed: `Password123!`

- **Admin**: `admin@msmedicalcenter.it`
- **Medici e pazienti**: creati con nomi casuali a ogni esecuzione del seed; l'elenco con le rispettive email viene stampato in console al termine di `uv run python seed.py`.

## Documentazione

- Diagrammi UML (casi d'uso) ed ER: cartella `docs/`
- Schema OpenAPI generato dall'API: `docs/openapi.json`
- Esempio di endpoint su Swagger UI: `docs/esempio-swagger.png`
- Diario delle attività di sviluppo: `diario.md`
