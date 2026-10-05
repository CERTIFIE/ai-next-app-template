# docs — documenti di lavoro del progetto

Qui vivono i documenti **prodotti durante lo sviluppo**. I documenti
concordati con il cliente stanno invece in `.documents/` e fanno fede.

| File | Chi lo scrive | Contenuto |
| --- | --- | --- |
| `brief.md` | tu, prima dell'avvio | scheda progetto: nome, obiettivo, tenant, target, lingue, elenco dei documenti |
| `sources/` | servizio Docker `documents` | estratti Markdown dei documenti del cliente + `INDEX.md` (non modificare a mano) |
| `requirements.md` | Product Owner | requisiti, criteri di accettazione, stato ed evidenze di collaudo |
| `architecture.md` | Technical Leader | dominio, architettura, contratti, decisioni, versioni |
| `plan.md` | Technical Leader | milestone, incarichi, responsabili dei file, blocchi |
| `verification.md` | chi verifica | comandi, esiti, verifiche manuali, integrazioni non verificate |
| `ux.md` | UX Designer | flussi, mappa delle pagine, wireframe, design system |

`sources/` va in Git insieme agli altri file: quando il cliente manda una
nuova versione di un documento, il diff dell'estratto mostra cosa è cambiato.
