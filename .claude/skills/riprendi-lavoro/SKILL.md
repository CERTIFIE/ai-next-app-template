---
name: riprendi-lavoro
description: Riprende lo sviluppo multiagente da dove si era interrotto, ricostruendo lo stato dai documenti vivi di docs/ e dal repository.
disable-model-invocation: true
argument-hint: "[indicazioni per questa sessione]"
---

# Ripresa del lavoro

Indicazioni dell'utente per questa sessione: $ARGUMENTS

Agisci come **Coordinatore** secondo `AGENTS.md`.

1. Riesegui la conversione dei documenti (servizio `documents`) e controlla
   in `docs/sources/INDEX.md` se il cliente ha fornito documenti nuovi o
   aggiornati: in quel caso, prima di proseguire, il `product-owner` aggiorna
   i requisiti e tu porti all'utente l'impatto sul perimetro.
2. Leggi `docs/plan.md`, `requirements.md`, `architecture.md` e
   `verification.md`. Controlla `git status` e `git log` recenti per modifiche
   non registrate nei documenti.
3. Ricostruisci in breve: milestone corrente, cosa è integrato, cosa è
   verificato, cosa è in sospeso, decisioni pendenti e blocchi.
4. Se trovi modifiche non integrate o non verificate, falle valutare al
   `tech-lead` prima di proseguire: non sovrascrivere lavoro esistente.
5. Se ci sono decisioni dell'utente ancora aperte, ponile subito, raggruppate.
6. Altrimenti riprendi dal prossimo passo del piano seguendo la Fase 5 di
   `/avvio-progetto`, senza ripetere attività già concluse e verificate.

Mostra all'utente il riepilogo dello stato prima di delegare nuovo lavoro.
