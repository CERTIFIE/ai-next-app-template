# Scheda progetto

> Compila questa scheda prima di lanciare `/avvio-progetto`. È l'unica parte
> che cambia da un progetto all'altro; il resto delle regole è in `AGENTS.md`.
> I documenti del cliente vanno in `.documents/`, non qui.

## Identità

- **Nome del prodotto:** <!-- es. Login -->
- **Nome tecnico (APP_NAME):** <!-- minuscolo, senza spazi, es. login-app -->
- **Cliente:** <!-- ragione sociale -->

## Obiettivo

<!-- Due o tre frasi: cosa deve fare il prodotto e per chi.
     Indica esplicitamente cosa è escluso, es.:
     "Riscrittura del prodotto X limitata a DDT e CMR; esclusi cassetto e
     dichiarazione doganale." -->

## Fonti

<!-- Elenca i documenti concordati con il cliente messi in .documents/
     (DOCX, XLSX, PDF), con versione e data. -->

- **Offerta commerciale:** <!-- es. .documents/offerta-v2.pdf (v2, 12/09/2026) -->
- **Specifiche funzionali:** <!-- es. .documents/specifiche-funzionali.docx -->
- **Specifiche tecniche:** <!-- es. .documents/integrazioni-api.pdf -->
- **Altri allegati:** <!-- es. .documents/tracciati-record.xlsx -->
- **Codice o prodotto esistente da analizzare:** <!-- percorso o URL repository, oppure "nessuno" -->

## Parametri

- **Tenant:** <!-- chi è il tenant, es. "azienda cliente che inserisce i documenti" -->
- **Ruoli noti:** <!-- es. amministratore piattaforma, amministratore tenant, operatore -->
- **Target di produzione:** <!-- Vercel | container (Docker/Kubernetes) | on-premise -->
- **Lingue supportate:** <!-- es. it, en, fr, es, de -->
- **Lingua di default:** it
- **Database:** PostgreSQL
- **Integrazioni con terze parti:** <!-- API da esporre e servizi esterni da consumare -->
- **Job pianificati noti:** <!-- es. invio riepiloghi notturni -->

## Vincoli e scadenze

<!-- milestone contrattuali, date, vincoli di budget, requisiti di
     conservazione dati, accessibilità, SLA -->

## Decisioni già prese

<!-- tutto ciò che gli agenti non devono rimettere in discussione -->
