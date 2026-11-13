FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /html && chown ubuntu:ubuntu /html && chmod 755 /html

WORKDIR /app
COPY updater .
RUN chmod 755 updater

USER 1000:1000

CMD ["./updater"]
