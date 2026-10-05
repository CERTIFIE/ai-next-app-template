# AGENTS.md — istruzioni di progetto per gli agenti

Questo file vale per ogni agente che lavora sul repository (Claude Code, Codex o
altri). Contiene le regole stabili; il processo di avvio di un progetto è nella
skill `/avvio-progetto` e lo stato del lavoro è nei documenti vivi di
`docs/` (§6).

## 1. Da dove vengono i requisiti

**Tutto ciò che serve per costruire il prodotto è nei documenti concordati con
il cliente**, in `.documents/`: offerta commerciale, specifiche funzionali e
tecniche, allegati, in formato **DOCX, XLSX o PDF**, senza sottocartelle.
Prima di proporre architettura o codice leggili integralmente.

| Percorso | Contenuto | Accesso agenti |
| --- | --- | --- |
| `.documents/*` | originali concordati con il cliente: **fanno fede** | sola lettura |
| `docs/sources/*.md` | estratti Markdown degli originali + `INDEX.md` (generati) | sola lettura |
| `docs/brief.md` | scheda progetto compilata dall'utente | sola lettura |
| `docs/*.md` (§6) | documenti vivi degli agenti | lettura e scrittura |

**Come si leggono i documenti del cliente**

1. Gli originali DOCX e XLSX non sono leggibili direttamente: prima di ogni
   analisi esegui la conversione con il servizio Docker `documents`
   (`npm run docs:convert` dopo lo scheletro, prima ancora
   `docker compose --env-file .env -f .docker/compose.app.yml --profile tools run --rm documents`).
2. Leggi `docs/sources/INDEX.md`: elenca ogni originale con checksum, stato
   (nuovo, aggiornato, invariato, errore, non supportato) e avvertenze.
3. Leggi gli estratti in `docs/sources/`. Dove l'indice segnala PDF
   scansionati, immagini o diagrammi non estratti, apri l'originale (i PDF si
   leggono anche come immagini, pagina per pagina).
4. Cita sempre come fonte **l'originale** (`.documents/<file>`, sezione, pagina
   o foglio e cella), non l'estratto.
5. Un documento con stato *aggiornato* è una nuova versione concordata:
   confronta l'estratto con la versione precedente (`git diff docs/sources/`)
   e segnala i requisiti da rivedere.

- I documenti sono la fonte dei requisiti; le regole operative sono quelle di
  questo file, della skill di avvio e delle decisioni successive dell'utente.
- Offerta e specifiche non hanno precedenza implicita l'una sull'altra: se
  confliggono, riporta i passaggi, l'impatto e la decisione richiesta.
- Non implementare opzioni citate ma non acquistate, e non inventare requisiti
  per colmare i vuoti: distingui domande bloccanti da assunzioni reversibili.
- Segnala documenti mancanti, illeggibili o incompleti invece di ignorarli.
- Non modificare, rinominare, spostare o aggiungere file in `.documents/`, né
  modificare a mano `docs/sources/` o `docs/brief.md`.

## 2. Il team

| Agente | File | Modello | Responsabilità |
| --- | --- | --- | --- |
| Coordinatore | sessione principale | — | rapporto con l'utente, approvazioni, integrazione finale |
| Product Owner | `.claude/agents/product-owner.md` | opus | requisiti, criteri di accettazione, collaudo funzionale |
| Technical Leader | `.claude/agents/tech-lead.md` | opus | architettura, piano tecnico, coordinamento sviluppo, revisione |
| Backend Developer | `.claude/agents/backend-developer.md` | sonnet | business, query, persistenza, API, auth, job |
| Frontend Developer | `.claude/agents/frontend-developer.md` | sonnet | pagine, componenti, form, i18n, accessibilità |
| UX/UI Designer | `.claude/agents/ux-designer.md` | sonnet | flussi, wireframe, design system DaisyUI, linee guida UI |

Flusso: Coordinatore → Product Owner (cosa e come si accetta) → Technical
Leader (come si costruisce) → sviluppatori e designer → Technical Leader
(integrazione e revisione) → Product Owner (collaudo) → Coordinatore (consegna).

## 3. Regole di coordinamento

- Al massimo **tre subagenti attivi contemporaneamente**, oltre al
  coordinatore. Per attività piccole o sequenziali usa meno agenti.
- Un'attività non è conclusa perché un agente lo dichiara: va integrata,
  verificata e, per il codice, revisionata da un agente diverso dall'autore.
- **Un solo responsabile di scrittura per file** in ogni momento. Non presumere
  checkout isolati. Se usi worktree, registra il riferimento di partenza e
  integra esplicitamente.
- Sono **file condivisi del Technical Leader** (o di un unico delegato
  esplicito): schema dati e migrazioni, `src/business/core`, contratti in
  `src/interfaces`, `package.json` e lockfile, configurazioni di TypeScript,
  ESLint, Prettier, Vitest, Next.js, tutto `.docker/` e `.vscode/`.
- Le interfacce condivise si concordano prima; una variazione si propone al
  Technical Leader, che ne valuta l'impatto e lo comunica agli altri.
- Nessun agente aggiunge dipendenze in autonomia: le propone motivandole.
- Ogni incarico contiene: obiettivo e ID requisiti; contesto e decisioni
  approvate; file assegnati e file da non toccare; contratti e dipendenze;
  verifiche richieste e condizione di completamento; formato del resoconto.
- Ogni resoconto contiene: modifiche, file toccati, verifiche **realmente
  eseguite** con esito, limiti, decisioni pendenti, rischi. Un blocco o una
  necessità di cambiare contratto si segnala subito.
- Test e revisione si fanno su una versione identificabile (commit o diff).
  Non sommare esiti verdi ottenuti su versioni diverse.

## 4. Stack

- **Next.js (App Router) + React + TypeScript** in un'unica applicazione che fa
  da frontend e backend (route handler e server action). Niente backend separato.
- **TailwindCSS + DaisyUI** per la UI.
- **PostgreSQL** come database. ORM o query builder da proporre e motivare
  nell'architettura (preferenza per soluzioni leggere e tipizzate).
- **Better-Auth** per l'autenticazione, ruoli gestiti dall'applicazione. Una
  sola fonte di verità per tenant e appartenenze; le tabelle di Better-Auth si
  usano tramite la sua API o un adapter dedicato, mai con query sparse.
- **MailDev** per la posta in sviluppo e test; provider reale dietro
  un'interfaccia (Abstract Factory) in produzione.
- **Vitest** per unit e integration test; **Playwright** solo per i flussi end
  to end del collaudo, se approvato.
- **Prettier + ESLint** (flat config). **SonarQube** per l'analisi statica.
- Versioni compatibili tra loro, verificate sulla documentazione ufficiale e
  registrate in `architecture.md`. Non mescolare esempi di versioni diverse.

## 5. Ambiente: tutto in Docker

L'host non esegue `next dev`, build, test o `npm install`: solo Docker.

| File | Scopo |
| --- | --- |
| `.docker/compose.app.yml` | app (hot reload + debug), cron, postgres, maildev, sonarqube, scanner |
| `.docker/compose.test.yml` | unit, integration, e2e (profilo), con risorse isolate per esecuzione |
| `.docker/app/Dockerfile` | stadi `dev`, `build`, `runner` (standalone) |
| `.docker/cron/` | scheduler che chiama le rotte `/api/cron/*` come Vercel Cron |
| `.docker/documents/` | conversione di `.documents/` (DOCX, XLSX, PDF) in `docs/sources/` |

- Sorgenti montati in bind su `/app`; `node_modules` e `.next` in volumi del
  container. Se l'hot reload non scatta, abilita il polling e verificalo.
- Debug: `next dev --inspect=0.0.0.0:9229`, porta pubblicata solo su
  `127.0.0.1`. Configurazione *attach* in `.vscode/launch.json`.
- **I dati persistenti stanno in `.data/<servizio>/`** sull'host, esclusi da
  Git. Sono dati da preservare: cancellarli non è una procedura di reset.
- **Test isolati**: ogni esecuzione ha un `TEST_RUN_ID` univoco, un progetto
  Compose proprio (`<app>_test_<run>`) e database per worker
  (`<app>_test_<run>_<worker>`). Una suite pulisce solo ciò che ha creato.
  Vietate pulizie globali (`docker system prune`, `docker volume prune`).
- Job pianificati: rotte `/api/cron/<job>` protette da
  `Authorization: Bearer $CRON_SECRET`, eseguite in locale dal servizio `cron`
  e in produzione dallo scheduler del target (es. `vercel.json`).
- Contratto degli script npm (da creare nello scheletro):
  - **sull'host**, unico punto d'ingresso documentato, richiamano Docker e non
    richiedono `node_modules` locali: `docker:up`, `docker:down`, `docker:logs`,
    `test`, `test:unit`, `test:integration`, `test:coverage`, `test:e2e`,
    `test:watch`, `format`, `format:check`, `lint`, `lint:fix`, `typecheck`,
    `build`, `verify`, `sonar`, `docs:convert` (i `test*` passano da
    `.docker/test.sh`);
  - **nel container**, usati da Dockerfile e Compose: `dev`, `start`,
    `build:next`, `vitest:unit`, `vitest:integration`, `vitest:coverage`
    (report in `$REPORTS_DIR`). Nomi distinti evitano che uno script
    dell'host richiami se stesso dentro il container.

## 6. Documenti vivi (`docs/`)

Aggiornali senza duplicare informazioni; servono a riprendere il lavoro.
Non vanno mai in `.documents/`, che contiene solo i documenti del cliente.

- `requirements.md` — Product Owner: requisiti con ID stabile, fonte, ruoli,
  criteri di accettazione, milestone, stato ed evidenze di collaudo.
- `architecture.md` — Technical Leader: dominio, architettura, contratti,
  decisioni approvate con motivazione, versioni.
- `plan.md` — Technical Leader: milestone, incarichi, responsabili dei file,
  dipendenze, assunzioni, blocchi.
- `verification.md` — chi verifica: comandi, ambienti, esiti, verifiche manuali,
  integrazioni non ancora verificate dal vivo.
- `ux.md` — UX Designer: flussi, mappa delle pagine, componenti, linee guida.

## 7. Architettura applicativa

Usa i pattern dove risolvono un problema concreto; niente astrazioni senza uso.

**Responsabilità.** Ogni classe di `src/business` nomina al massimo un
repository. Per attraversare più tabelle si compongono getter e comandi che le
possiedono; una vista composta senza fonte propria è un `ServiceGetter`. Non
caricare intere tabelle per filtrare, ordinare o paginare in memoria: serve una
query dedicata in `src/query`. Per operazioni su più entità definisci confini
transazionali, idempotenza e gestione dei fallimenti parziali.

**Command.** Cinque classi base in `src/business/core`:

| Classe | Accesso diretto al DB | Serve a |
| --- | --- | --- |
| `ServiceDataGetter` | sì, un repository | leggere: `load`, `list` paginata, `count` |
| `ServiceDataCommand` | sì, un repository | modificare lo stato persistito |
| `ServiceGetter` | no | calcolare o comporre altri getter |
| `ServiceCommand` | no | eseguire un'azione o coordinare comandi |
| `ServiceQuestionGetter` | no | rispondere sì/no con `answer` |

I getter implementano `load`, `list`, `count`; dove non hanno senso sollevano
`NotImplemented`. `list` è sempre paginata.

**Abstract Factory** solo per famiglie che variano insieme (infrastruttura reale
o di prova: repository, posta, storage, provider esterni). Dove basta `new`,
niente factory.

**Proxy** davanti a repository e servizi esterni per controlli trasversali:
isolamento tenant, autorizzazioni, audit, cache, rate limit. Il contesto
autenticato (identità, tenant, permessi) si costruisce sul server: un
`tenantId` dal client non prova nulla. Vale per pagine, server action, API,
worker e cron. Le regole di dominio restano nei servizi.

**Query.** Filtri, ordinamenti, proiezioni e join stanno solo in
`src/query/<ambito>/`. Ogni DataGetter/DataCommand ha una query e ogni query un
solo proprietario. Ogni query su dati di tenant pretende il contesto tenant nel
costruttore. Niente costrutti o import dell'ORM in `src/business`. Nessun
tenant fittizio, opzionale o filtro vuoto come scorciatoia.

**Cartelle**

```
src/business/core/       classi base
src/business/<ambito>/   getter e comandi: decidono COSA fare
src/query/<ambito>/      query: COME interrogare il database
src/interfaces/dto/      record persistiti e sotto-oggetti
src/interfaces/          contratti di ingresso (I*), uno per file
src/types/               alias e vocabolari, uno per file
src/i18n/                dizionari, lingua, formattazione
src/lib/                 dominio e utilità
src/app/                 pagine e rotte (api/v1 per le integrazioni)
tests/                   test con percorsi speculari a src
tests/fixtures/          costruttori di dati di test
tests/e2e/               flussi di collaudo (se approvati)
```

La posizione di repository, adapter e Proxy si fissa in `architecture.md` prima
che più agenti li implementino.

## 8. API per terze parti

- Sotto `/api/v1/`, autenticate con **chiavi API per tenant** salvate come
  hash, revocabili, con permessi, rate limit e idempotenza dove un ritentativo
  duplica effetti.
- Documentazione **OpenAPI generata dai contratti** del codice, con Swagger UI.
- Passano per gli stessi getter e comandi dell'interfaccia: nessuna logica
  nelle rotte. Esponi solo gli endpoint del perimetro approvato.

## 9. Regole che diventano test

`tests/struttura.test.ts`, incluso in `verify`, controlla tramite AST
TypeScript (non ricerche testuali) che:

- ogni getter, comando o query concreto abbia il test speculare
  (`src/business/x/Y.ts` → `tests/business/x/Y.test.ts`);
- i file di `src/business` e `src/query` contengano una sola classe con lo
  stesso nome del file, senza funzioni, costanti o interfacce libere;
- i file di `src/interfaces` e `src/types` contengano un solo contratto;
- nessuna classe di `src/business` nomini più di un repository o violi i limiti
  della propria classe base;
- in `src/business` non compaiano costrutti di query.

Le regole non si applicano a componenti React, route handler, fixtures e
configurazioni.

## 10. Come si scrive

- **Codice, commenti, nomi di tabelle e chiavi i18n in inglese**; testi utente
  solo nei dizionari di `src/i18n`, nella lingua del dizionario.
- Lingua dei messaggi: preferenza del profilo → lingua salvata del destinatario
  → default del brief. Cron e code usano la lingua salvata.
- I commenti spiegano il perché, non il cosa.
- Istanti come `Date` in UTC, timestamp generati dal server; date di calendario
  rappresentate in modo che non si spostino col fuso. Formattazione centralizzata.
- Formattazione e lint con `npm run format` e `npm run lint:fix`, mai a mano.

## 11. Qualità e completamento

`npm run verify` esegue in Docker: formattazione, lint, tipi, test (incluso
struttura) e build di produzione; la stessa verifica gira in CI. SonarQube
(`npm run sonar`) non deve introdurre nuovi problemi bloccanti o critici.

Una milestone è completa quando i contributi sono integrati, la revisione è
chiusa, `verify` passa e il Product Owner ha collaudato i criteri previsti.
Mock e fixtures non dimostrano che un servizio esterno funzioni: registra
separatamente integrazioni verificate dal vivo e simulate.

## 12. Cosa non fare

- Non cancellare dati di sviluppo. I dati creati da script o verifiche si
  marcano con un campo `_test<Scopo>` e si puliscono filtrando solo su quello.
- Non aggirare regole con test disattivati, asserzioni vuote, soglie abbassate
  o deroghe al lint: proponi una modifica motivata della regola.
- Non introdurre credenziali nel repository o nei resoconti; `.env` non si legge.
- Non presentare placeholder o dati demo come funzionalità implementate.
- Non dichiarare eseguito un comando, test, revisione o collaudo non svolto.
- Non pubblicare, acquistare servizi o migrare dati reali senza richiesta
  esplicita dell'utente.
