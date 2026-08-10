# Diario progettuale

## Log Commit Recenti

### 2026-08-10 — ~6h26min

- **~20 min** — Inizializzazione progetto, aggiunto .gitignore e diario.md
- **~35 min** — Aggiunta documentazione: diagramma UML casi d'uso, architettura a livelli, diagramma ER, gerarchia dei repository (diagrammi già predisposti nella fase di progettazione)
- **~2h15min** — Setup progetto BE con uv: fastapi, uvicorn, sqlalchemy, pydantic, python-jose, passlib, python-multipart, bcrypt
- **~15 min** — Aggiunto .env.example
- **~50 min** — Analisi delle dipendenze e riorganizzazione della struttura
- **~10 min** — Creato main.py con endpoint root e /health
- **~5 min** — Creata struttura a livelli del backend: routers, services, repositories, models, schemas, core
- **~20 min** — Creato core/config.py per leggere le variabili da .env con pydantic-settings
- **~15 min** — Creato core/database.py: engine SQLAlchemy (SQLite) e get_db() come dependency
- **~25 min** — Creati i modelli SQLAlchemy Utente, Paziente, Medico; corretta la direzione delle foreign key nel diagramma ER
- **~30 min** — Creati i modelli catalogo (Specialita, Prestazione, Sede), agenda (Disponibilita, Appuntamento) e finali (Pagamento, Referto, tabella ponte medico_specialita); revisione e controllo di correttezza rispetto allo schema SQL
- **~21 min** — Creato seed.py con dati eterogenei generati casualmente e controllo di esistenza per evitare duplicati

**Attività**
- Riorganizzata la struttura del backend eliminando un livello di cartelle superfluo
- Uniformata la nomenclatura dei file di documentazione
- Sostituite due dipendenze non più manutenute con alternative attuali

**Difficoltà incontrate**  
- Incompatibilità tra `passlib` e le versioni recenti di `bcrypt`, dovuta al
  mancato aggiornamento della prima → sostituita con `bcrypt` diretto
- Per coerenza sostituita anche `python-jose`, non più manutenuta, con `PyJWT`
- Diagramma dei casi d'uso esportato in formato non adatto ai disegni a linee
  → riesportato in PNG
