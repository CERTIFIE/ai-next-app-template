---
name: avvio-progetto
description: Avvia lo sviluppo multiagente di un nuovo prodotto partendo dal brief e dai documenti concordati con il cliente (DOCX, XLSX, PDF) in .documents/. Analisi, approvazione, scheletro, milestone e consegna.
disable-model-invocation: true
argument-hint: "[note aggiuntive per questo progetto]"
---

# Avvio di un nuovo progetto — sviluppo multiagente

Note aggiuntive dell'utente per questo avvio: $ARGUMENTS

## Il tuo incarico

Agisci come **Coordinatore** responsabile dell'intero progetto, secondo
`AGENTS.md`. Delega ai subagenti di `.claude/agents/`: questa istruzione
autorizza esplicitamente la delega.

Il risultato richiesto è un'applicazione **funzionante, aderente al perimetro
dell'offerta, verificata e predisposta per il target di produzione** indicato
nel brief. Una demo, uno scheletro o contributi non integrati non sono la
consegna.

Se l'ambiente non offre subagenti, dichiaralo e proponi come procedere: non
presentare ruoli simulati come agenti realmente eseguiti.

## Fase 1 — Analisi (Product Owner)

1. Verifica che `docs/brief.md` sia compilato e che in `.documents/` ci siano
   almeno l'offerta commerciale e le specifiche funzionali. Se manca qualcosa
   di essenziale, fermati e dillo.
2. Converti i documenti con il servizio Docker `documents` (vedi `AGENTS.md`
   §1) e leggi `docs/sources/INDEX.md`. Riporta subito errori, formati non
   supportati e PDF scansionati.
3. Affida al `product-owner` la lettura integrale dei documenti e la stesura di
   `docs/requirements.md`. Per documenti molto voluminosi puoi
   far leggere parti indipendenti in parallelo e poi riconciliare.
4. Ottieni: requisiti con ID e criteri di accettazione, perimetro (incluso,
   escluso, opzioni, futuri), conflitti offerta/specifiche, domande bloccanti,
   assunzioni reversibili, requisiti non funzionali.

## Fase 2 — Proposta tecnica (Technical Leader e Designer)

1. Affida al `tech-lead` `architecture.md` e `plan.md`: scelte tecniche
   motivate dalle specifiche, dominio e tenant, rapporto con Better-Auth, ruoli,
   contratti, Abstract Factory e Proxy previsti, dipendenze, API, job,
   compatibilità col target, milestone e incarichi parallelizzabili.
2. Il `tech-lead` può coinvolgere l'`ux-designer` per mappa delle pagine e
   flussi principali, se servono a stimare o a chiarire il perimetro.

## Fase 3 — Approvazione

Presenta all'utente, in un'unica risposta: quadro dei requisiti e perimetro,
conflitti, domande bloccanti con proposta, assunzioni, architettura, dipendenze
e piano a milestone. **Chiedi un'approvazione congiunta e attendi.** Il silenzio
non è approvazione. Nel frattempo sono ammesse solo analisi indipendenti.

## Fase 4 — Scheletro verificato

Dopo l'approvazione il `tech-lead` crea lo scheletro come descritto nel suo
file di agente e in `AGENTS.md` §5: Next.js creato nel container, script npm,
Docker con hot reload, debug, classi base, `tests/struttura.test.ts`,
`npm run verify` verde, SonarQube attivo, README del prodotto al posto della
guida del template. Riporta le
verifiche manuali ancora da completare.

## Fase 5 — Sviluppo per milestone

Per ogni milestone del piano:

1. `ux-designer` sui flussi con interfaccia nuova;
2. `backend-developer` e `frontend-developer` su incarichi con file e contratti
   assegnati dal `tech-lead` (massimo tre subagenti attivi);
3. integrazione e revisione del `tech-lead`, `verify` e Sonar;
4. collaudo del `product-owner` sulla versione integrata;
5. aggiornamento di `requirements.md`, `plan.md`, `verification.md`.

Prosegui tra le milestone senza chiedere conferme ordinarie; aggiorna l'utente
su risultati, decisioni rilevanti e blocchi. Chiedi una decisione solo se
cambiano perimetro o architettura, servono costi nuovi o manca un'informazione
indispensabile, continuando intanto le attività indipendenti.

## Fase 6 — Consegna

Verifica il prodotto integrato rispetto ai requisiti e al target. Consegna:

- requisiti inclusi tutti accettati, o rinviati esplicitamente dall'utente;
- README, `.env.example` senza segreti, istruzioni di avvio, migrazione e
  deploy riproducibili;
- istruzioni di backup, ripristino e operatività dei servizi usati;
- resoconto di evidenze, limiti e verifiche non eseguite.

Preparazione al deploy e deploy effettivo sono stati distinti: non pubblicare
nulla senza richiesta esplicita.

## Interruzioni

Se devi fermarti, lascia nei documenti vivi di `docs/` cosa è
integrato, cosa è verificato, cosa resta e il prossimo passo, così
`/riprendi-lavoro` può ripartire senza ripetere attività.

Inizia dalla Fase 1.
