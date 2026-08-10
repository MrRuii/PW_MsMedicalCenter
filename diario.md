# Diario progettuale

## Log Commit Recenti

### 2026-08-10 — ~4h

- **~30 min** — Inizializzazione progetto, aggiunto .gitignore e diario.md
- **~10 min** — Aggiunta documentazione: diagramma UML casi d'uso, architettura a livelli, diagramma ER, gerarchia dei repository (diagrammi già predisposti nella fase di progettazione)
- **~1h** — Setup progetto BE con uv: fastapi, uvicorn, sqlalchemy, pydantic, python-jose, passlib, python-multipart, bcrypt
- **~15 min** — Aggiunto .env.example
- **~2h** — Analisi delle dipendenze e riorganizzazione della struttura

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
