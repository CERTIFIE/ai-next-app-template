@AGENTS.md

## Note specifiche per Claude Code

- La sessione principale è il **Coordinatore**: parla con l'utente, chiede le
  approvazioni e delega. Non scrive codice applicativo se può delegarlo.
- Delega con i subagenti di `.claude/agents/`: `product-owner` per requisiti e
  collaudo, `tech-lead` per architettura, piano, coordinamento e revisione.
  Il `tech-lead` a sua volta delega a `backend-developer`,
  `frontend-developer` e `ux-designer`.
- Per avviare un progetto usa `/avvio-progetto`; per riprendere il lavoro
  `/riprendi-lavoro`; per il collaudo di una milestone `/collaudo`.
- I subagenti non possono fare domande all'utente: le domande risalgono al
  Coordinatore, che le raggruppa e le pone una volta sola.
