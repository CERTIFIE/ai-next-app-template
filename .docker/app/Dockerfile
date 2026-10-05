# syntax=docker/dockerfile:1.7
# Immagine unica a stadi:
#   dev    -> sviluppo con hot reload e debug (usata da compose.app.yml e compose.test.yml)
#   build  -> build di produzione
#   runner -> esecuzione in produzione su target container (output "standalone" di Next.js)
# Su Vercel gli stadi build/runner non servono: la build la fa la piattaforma.

ARG NODE_VERSION=24

FROM node:${NODE_VERSION}-bookworm-slim AS base
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------- dev
FROM base AS dev
ENV NODE_ENV=development
COPY .docker/app/entrypoint.dev.sh /usr/local/bin/entrypoint.dev.sh
# Le cartelle dei volumi esistono già con proprietario "node": un volume nuovo
# eredita i permessi e l'utente non-root può installare e compilare.
RUN chmod +x /usr/local/bin/entrypoint.dev.sh \
 && mkdir -p /app/node_modules /app/.next /home/node/.npm \
 && chown -R node:node /app /home/node/.npm
USER node
EXPOSE 3000 9229
ENTRYPOINT ["entrypoint.dev.sh"]
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--inspect=0.0.0.0:9229"]

# ---------------------------------------------------------------- deps
FROM base AS deps
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci

# ---------------------------------------------------------------- build
FROM deps AS build
COPY . .
# next.config deve avere output: "standalone" per lo stadio runner.
RUN npm run build:next

# ---------------------------------------------------------------- runner
FROM node:${NODE_VERSION}-bookworm-slim AS runner
WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOSTNAME=0.0.0.0
COPY --from=build --chown=node:node /app/public ./public
COPY --from=build --chown=node:node /app/.next/standalone ./
COPY --from=build --chown=node:node /app/.next/static ./.next/static
USER node
EXPOSE 3000
CMD ["node", "server.js"]
