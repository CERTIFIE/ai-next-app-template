# Template — piattaforma full-stack Next.js con sviluppo multiagente

Template aziendale per sviluppare prodotti full-stack con un team di agenti AI
(Claude Code, compatibile anche con Codex), partendo dai **documenti concordati
con il cliente**: offerta commerciale e specifiche tecnico-funzionali in DOCX,
XLSX o PDF.

Il template non contiene il prodotto: definisce **agenti, regole, tecnologie e
ambiente**. Il codice lo scrive il team di agenti leggendo i documenti che
inserisci in `.documents/`.

**Stack:** Next.js (App Router) · React · TypeScript · TailwindCSS + DaisyUI ·
PostgreSQL · Better-Auth · MailDev · Vitest · Playwright · SonarQube · Docker.

> Questo README è la guida del template. In ogni nuovo progetto il Technical
> Leader lo sostituisce con il README del prodotto: la guida resta qui.

## Indice

- [Prerequisiti](#prerequisiti)
- [Guida: dal contratto al prodotto in 9 passi](#guida-dal-contratto-al-prodotto-in-9-passi)
- [Situazioni ricorrenti](#situazioni-ricorrenti)
- [Consigli pratici](#consigli-pratici)
- [Domande frequenti](#domande-frequenti)
- [Riferimento](#riferimento): team, struttura, documenti, servizi, comandi, personalizzazione

---

## Prerequisiti

- **Docker Desktop** (o Docker Engine con Compose v2.24+), con almeno **6 GB di
  RAM** assegnati: SonarQube da solo ne usa circa 2.
- **Claude Code** aggiornato, da terminale o con l'estensione di VS Code.
- **VS Code** con le estensioni consigliate (le propone da solo all'apertura
  del progetto, da `.vscode/extensions.json`).
- **Git**.

Sul computer non servono Node né npm: tutto gira in Docker.

---

## Guida: dal contratto al prodotto in 9 passi

### 1. Crea il progetto dal template

Copia il template in una nuova cartella e fai il primo commit, così hai un
punto di partenza pulito a cui tornare:

```sh
cp -R <percorso-template>/nextjs-fullstack ~/workspace/nome-progetto
cd ~/workspace/nome-progetto
git init && git add -A && git commit -m "Avvio da template"
```

Non lavorare mai dentro la cartella del template: copiala sempre.

### 2. Inserisci i documenti del cliente in `.documents/`

Copia in `.documents/` l'offerta e le specifiche **concordate con il cliente**,
in formato **DOCX, XLSX o PDF**, senza sottocartelle.

- **Usa nomi chiari:** `offerta-v2.pdf`, `specifiche-funzionali.docx`,
  `tracciati-record.xlsx`. Gli agenti riconoscono il tipo di documento anche
  dal nome.
- **Mockup e diagrammi:** se un DOCX ne contiene di importanti, aggiungi anche
  la sua esportazione in PDF. Gli agenti non vedono le immagini dentro un DOCX,
  ma possono guardare le pagine di un PDF.
- I vecchi `.doc` non sono supportati: salvali come DOCX o PDF.

Gli agenti leggono questi file ma non possono modificarli.

### 3. Compila la scheda `docs/brief.md`

È l'unica parte del prompt che cambia da un progetto all'altro. Indica:

- nome e obiettivo del prodotto, con le **esclusioni** esplicite
  (es. "solo DDT e CMR, esclusa la parte doganale");
- l'elenco dei documenti messi in `.documents/`, con versione e data;
- chi è il tenant, quali ruoli esistono, il target di produzione (Vercel o
  container), le lingue;
- integrazioni con terze parti e job pianificati già noti;
- le **decisioni già prese**, che gli agenti non devono rimettere in discussione.

Dedicaci dieci minuti: un brief preciso evita interi giri di domande.

### 4. Configura l'ambiente

```sh
cp .env.example .env
```

In `.env`:

- imposta `APP_NAME` (minuscolo, es. `login-app`);
- genera `BETTER_AUTH_SECRET` con `openssl rand -base64 32`;
- genera `CRON_SECRET` con `openssl rand -hex 32`;
- cambia le password di PostgreSQL.

In `.vscode/settings.json` sostituisci `CHANGE_ME_APP_NAME` con lo stesso nome.

Avvia i servizi:

```sh
docker compose --env-file .env -f .docker/compose.app.yml up -d --build
```

Il container `app` resta in attesa: è normale, il progetto Next.js lo crea il
Technical Leader più avanti.

**SonarQube (una volta per progetto):**

1. apri http://localhost:9000 ed entra con admin/admin;
2. cambia la password;
3. crea un token di analisi e salvalo in `SONAR_TOKEN` dentro `.env`.

### 5. Avvia il team

Apri Claude Code nella cartella del progetto (`claude` da terminale, oppure
l'estensione di VS Code) e scrivi:

```
/avvio-progetto
```

Puoi aggiungere note per questo avvio, ad esempio:
`/avvio-progetto il cliente vuole la prima demo entro novembre`.

Cosa succede:

1. **Conversione:** i documenti diventano Markdown in `docs/sources/`. PDF
   scansionati, file illeggibili o formati non supportati vengono segnalati
   subito.
2. **Product Owner:** legge tutto e scrive `docs/requirements.md` (requisiti,
   perimetro, conflitti tra offerta e specifiche, domande).
3. **Technical Leader:** scrive `docs/architecture.md` e `docs/plan.md` (scelte
   tecniche, dipendenze, milestone).
4. **Stop:** il coordinatore presenta tutto e **aspetta la tua approvazione**.
   Prima di allora non viene scritto codice.

### 6. Approva perimetro, architettura e piano

È il passo più importante. Prima di rispondere, apri i tre documenti in
`docs/` e controlla:

- **perimetro:** c'è tutto quello che è in offerta e niente di più? Le opzioni
  non acquistate sono escluse?
- **conflitti e domande bloccanti:** rispondi a tutte in un unico messaggio;
- **assunzioni:** se una è sbagliata, correggila adesso;
- **dipendenze e scelte tecniche:** sono quelle che l'azienda vuole mantenere
  nel tempo?

Poi rispondi in modo esplicito: *"Approvato"* oppure *"Approvato con queste
modifiche: …"*. Il silenzio non vale come approvazione. Correggere qui costa
poco, correggere dopo tre milestone costa molto.

### 7. Segui lo sviluppo

Dopo l'approvazione il team procede da solo per milestone: prima lo scheletro
tecnico (Docker, struttura, test, debug), poi i flussi funzionali. Per ogni
milestone il Technical Leader integra e revisiona il codice e il Product Owner
lo collauda.

A te restano tre compiti:

- **rispondere quando il coordinatore ti interpella:** succede solo se cambia
  il perimetro, servono costi nuovi o manca un'informazione;
- **approvare i permessi** che Claude Code ti chiede, ad esempio i comandi Docker;
- **fare un commit a fine milestone,** per avere un punto a cui tornare. Puoi
  chiederlo direttamente: *"fai il commit della milestone M1"*.

Per vedere a che punto è il lavoro, apri la sezione *Stato corrente* di
`docs/plan.md`.

Mentre gli agenti lavorano, non modificare a mano i file condivisi
(`package.json`, configurazioni, Docker): chiedi al coordinatore.

### 8. Collauda

A fine milestone, o quando vuoi verificare un gruppo di requisiti:

```
/collaudo M2
```

Il Product Owner verifica i criteri di accettazione (casi positivi, errori,
permessi, isolamento tra tenant, API) e aggiorna stato ed evidenze in
`docs/requirements.md` e `docs/verification.md`. Un requisito è accettato solo
con un'evidenza reale.

### 9. Consegna

A fine progetto il coordinatore verifica che ogni requisito sia accettato o
rinviato da te. Prepara poi README del prodotto, istruzioni di avvio,
migrazione e deploy, backup e ripristino, e l'elenco delle verifiche non
eseguite dal vivo (ad esempio integrazioni senza credenziali reali).

**Il deploy non parte da solo:** va richiesto esplicitamente.

---

## Situazioni ricorrenti

| Situazione | Cosa fare |
| --- | --- |
| Hai chiuso la sessione e vuoi ripartire | `/riprendi-lavoro` |
| Il cliente manda una nuova versione di un documento | sostituisci il file in `.documents/` (togli la versione vecchia) e lancia `/riprendi-lavoro`: il documento risulta *aggiornato* e il Product Owner mostra l'impatto sui requisiti |
| Il cliente aggiunge un documento | copialo in `.documents/`, aggiornane l'elenco in `docs/brief.md`, poi `/riprendi-lavoro` |
| Vuoi collaudare una milestone o dei requisiti | `/collaudo M2` oppure `/collaudo REQ-DDT-001..010` |
| Vuoi lanciare i test | `sh .docker/test.sh all` (dopo lo scheletro: `npm run test`) |
| Vuoi l'analisi di qualità | `npm run sonar` (dopo lo scheletro) |
| Vuoi fare debug del server | VS Code → Run and Debug → *Docker: attach Next.js server* |
| Vuoi vedere le email inviate in sviluppo | http://localhost:1080 |
| Vuoi convertire i documenti a mano | `docker compose --env-file .env -f .docker/compose.app.yml --profile tools run --rm documents` |

---

## Consigli pratici

- **Al primo progetto resta presente** durante analisi, approvazione e
  scheletro: capirai se il template va ritoccato (regole in `AGENTS.md`,
  modelli degli agenti).
- **Costi:** Product Owner e Technical Leader usano Opus, il modello più
  capace e più costoso. Per progetti semplici puoi passarli a Sonnet cambiando
  il campo `model` nei loro file in `.claude/agents/`.
- **Rispondi alle domande tutte insieme:** il coordinatore le raggruppa
  apposta, e una risposta completa sblocca tutto il team.
- **Migliora il template, non solo il progetto:** se correggi una regola o un
  agente in un progetto e la correzione vale in generale, riportala nel
  template, così ne beneficiano tutti i progetti futuri.

---

## Domande frequenti

**Il container `app` non risponde su http://localhost:3000.**
Prima dello scheletro è normale: il container aspetta che il progetto Next.js
venga creato. Verifica con
`docker compose --env-file .env -f .docker/compose.app.yml logs app`.

**L'indice dei documenti segnala un "probabile PDF scansionato".**
Il PDF contiene immagini e non testo. Gli agenti lo leggono pagina per pagina,
ma se il cliente ha la versione testuale (DOCX o PDF esportato) è meglio usare
quella.

**Claude Code non vede gli agenti o i comandi `/avvio-progetto`.**
Avvia Claude Code dalla **radice** del progetto (dove c'è `CLAUDE.md`) e
verifica che `.claude/agents/` e `.claude/skills/` siano stati copiati: in
Finder i file che iniziano con il punto sono nascosti (`Cmd+Shift+.` per
mostrarli).

**Posso usare Codex o un altro strumento?**
Sì: `AGENTS.md` è letto anche da Codex. Le skill in `.claude/skills/` sono
prompt in Markdown che puoi incollare in qualsiasi strumento.

**Devo cancellare `.data/` per ripartire da zero?**
No, contiene dati da preservare. Fai prima un backup (istruzioni in
`.data/README.md`) e chiedi al coordinatore come procedere.

---

## Riferimento

### Il team di agenti

```
                      Utente
                        │  approvazioni, decisioni
                  ┌─────▼──────┐
                  │Coordinatore│  sessione principale di Claude Code
                  └──┬──────┬──┘
        cosa e quando│      │come
        si accetta   │      │si costruisce
          ┌──────────▼─┐  ┌─▼────────────┐
          │Product     │  │Technical     │
          │Owner (opus)│  │Leader (opus) │
          └────────────┘  └─┬─────┬─────┬┘
                ┌───────────┘     │     └────────────┐
         ┌──────▼──────┐  ┌───────▼──────┐  ┌────────▼─────┐
         │UX Designer  │  │Backend Dev   │  │Frontend Dev  │
         │(sonnet)     │  │(sonnet)      │  │(sonnet)      │
         └─────────────┘  └──────────────┘  └──────────────┘
```

| Agente | Scrive in | Ruolo |
| --- | --- | --- |
| `product-owner` | `docs/requirements.md`, `verification.md`, `tests/e2e/` | requisiti, criteri di accettazione, collaudo |
| `tech-lead` | `docs/architecture.md`, `plan.md`, file condivisi | architettura, coordinamento, integrazione, revisione |
| `backend-developer` | `src/business`, `src/query`, API, test | logica, persistenza, API `/api/v1`, cron |
| `frontend-developer` | `src/app`, componenti, `src/i18n` | interfaccia, i18n, accessibilità |
| `ux-designer` | `docs/ux.md` | flussi, wireframe, design system DaisyUI |

Le definizioni sono in `.claude/agents/`; modelli, strumenti e permessi sono
nel frontmatter di ciascun file. Le regole comuni sono in `AGENTS.md`.

### Struttura

```
.claude/
  agents/            definizioni dei subagenti
  skills/            prompt riutilizzabili: /avvio-progetto, /riprendi-lavoro, /collaudo
  settings.json      permessi condivisi (blocca lettura .env, pulizie Docker, modifica dei documenti cliente)
.data/               dati persistenti dei servizi Docker (esclusi da Git)
.docker/
  app/               Dockerfile multi-stadio (dev, build, runner) ed entrypoint
  cron/              scheduler che chiama /api/cron/* come Vercel Cron
  documents/         conversione di .documents/ in Markdown per gli agenti
  postgres/init/     script di prima inizializzazione (database SonarQube)
  compose.app.yml    app, cron, postgres, maildev, sonarqube, sonar-scanner, documents
  compose.test.yml   unit, integration, coverage, e2e isolati per esecuzione
  test.sh            esecuzione dei test con pulizia mirata
.documents/          documenti concordati con il cliente (DOCX, XLSX, PDF): fanno fede
docs/                brief, estratti dei documenti (sources/) e documenti vivi degli agenti
.vscode/             settings, debug in Docker, estensioni consigliate, task
src/                 codice (creato dagli agenti)
tests/               test speculari a src e fixtures
AGENTS.md            regole per tutti gli agenti (letto da Claude Code e Codex)
CLAUDE.md            importa AGENTS.md e aggiunge note specifiche per Claude Code
```

### Come gli agenti leggono i documenti del cliente

Gli agenti leggono bene Markdown e PDF, ma non i file Office. Per questo il
servizio Docker `documents` (basato su MarkItDown, tutto in locale) converte
ogni file di `.documents/` in `docs/sources/<file>.md` e scrive
`docs/sources/INDEX.md` con checksum, stato e avvertenze.

- **DOCX** → testo, titoli e tabelle (le immagini no: vanno viste sull'originale o sul PDF).
- **XLSX/XLS** → una tabella per foglio.
- **PDF** → testo; se è scansionato l'indice lo segnala e gli agenti leggono le pagine come immagini.
- I file invariati non vengono riconvertiti; un file **aggiornato** viene
  marcato nell'indice, così il Product Owner rivede i requisiti collegati.
- Gli originali restano la fonte ufficiale: nei requisiti gli agenti citano
  `.documents/<file>`, sezione, pagina o foglio.

Gli agenti non possono modificare `.documents/` né gli estratti
(`.claude/settings.json`). `/avvio-progetto` e `/riprendi-lavoro` eseguono la
conversione da soli.

### Servizi e porte

Tutte le porte sono pubblicate solo su `127.0.0.1`.

| Servizio | URL / porta | Note |
| --- | --- | --- |
| app | http://localhost:3000 | Next.js con hot reload |
| debug Node | 127.0.0.1:9229 | VS Code → *Docker: attach Next.js server* |
| postgres | localhost:5432 | dati in `.data/postgres` |
| maildev | http://localhost:1080 (SMTP 1025) | email di sviluppo |
| sonarqube | http://localhost:9000 | primo accesso admin/admin |
| cron | — | job in `.docker/cron/crontab` |

### Comandi

Prima dello scheletro (nessun `package.json`):

```sh
docker compose --env-file .env -f .docker/compose.app.yml up -d --build    # avvia i servizi
docker compose --env-file .env -f .docker/compose.app.yml down             # li ferma (i dati restano)
```

Dopo lo scheletro gli agenti creano gli script npm del contratto in
`AGENTS.md` §5 (`docker:up`, `docker:down`, `test`, `verify`, `sonar`,
`docs:convert`, …), che diventano l'unico punto d'ingresso. I test si possono
lanciare anche direttamente:

```sh
sh .docker/test.sh unit        # unit | integration | coverage | e2e | all
```

Ogni esecuzione dei test usa database, rete e volumi propri e li elimina alla
fine: più persone o agenti possono lanciarli insieme.

**Analisi SonarQube manuale:**

```sh
sh .docker/test.sh coverage
docker compose --env-file .env -f .docker/compose.app.yml --profile scan run --rm sonar-scanner
```

### Personalizzare il template

- **Altri stack** (es. .NET con Razor, React o Angular): duplica il template,
  aggiorna `AGENTS.md` §4–§5 e §7, il Dockerfile, i compose e gli agenti di
  sviluppo; agenti funzionali, skill, `.documents/` e `docs/` restano invariati.
- **Modelli:** cambia il campo `model` nei file di `.claude/agents/`
  (`opus`, `sonnet`, `haiku` o un ID completo).
- **Regole del team:** sono in `AGENTS.md`; tienilo conciso, perché ogni
  agente lo legge a ogni sessione.
