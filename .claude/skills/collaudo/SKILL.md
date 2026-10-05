---
name: collaudo
description: Esegue il collaudo funzionale di una milestone o di un insieme di requisiti con il Product Owner, su una versione identificata del codice.
disable-model-invocation: true
argument-hint: "[milestone o ID requisiti, es. M2 oppure REQ-DDT-001..010]"
---

# Collaudo

Oggetto del collaudo: $ARGUMENTS (se vuoto, la milestone corrente di `plan.md`).

1. Identifica la versione da collaudare (commit corrente e `git status`
   pulito). Se ci sono modifiche non committate, chiedi all'utente se
   collaudare comunque e registra lo stato esatto.
2. Assicurati che l'ambiente sia avviato (`npm run docker:up`) e che
   `npm run verify` sia verde; se non lo è, il collaudo non parte e il problema
   va al `tech-lead`.
3. Affida al `product-owner` il collaudo dei requisiti indicati secondo i loro
   criteri di accettazione: flussi positivi, errori, permessi, isolamento tra
   tenant, API `/api/v1`, lingue supportate.
4. Il `product-owner` aggiorna stato ed evidenze in `requirements.md` e
   `verification.md`.
5. Riporta all'utente: requisiti accettati, respinti (con passi di
   riproduzione), verifiche non eseguibili e perché, e il prossimo passo.

Non dichiarare accettato nulla senza evidenza reale.
