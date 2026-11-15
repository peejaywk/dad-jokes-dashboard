FROM alpine:3.24

RUN apk add --no-cache bash curl ca-certificates && \
    adduser -D -u 1000 updater && \
    mkdir /html && chown updater:updater /html && chmod 755 /html

WORKDIR /app
COPY updater .
RUN chmod 755 updater

USER 1000:1000

CMD ["./updater"]
