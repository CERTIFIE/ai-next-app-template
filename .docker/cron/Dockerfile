# Scheduler di sviluppo: chiama le rotte /api/cron/<job> dell'app come fa
# Vercel Cron in produzione (GET con Authorization: Bearer $CRON_SECRET).
FROM alpine:3
RUN apk add --no-cache curl tzdata
COPY .docker/cron/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY .docker/cron/run-job.sh /usr/local/bin/run-job
RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/run-job
ENTRYPOINT ["entrypoint.sh"]
