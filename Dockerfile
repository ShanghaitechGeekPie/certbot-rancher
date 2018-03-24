FROM certbot/dns-cloudxns:latest

MAINTAINER eastpiger

ENTRYPOINT [ "/bin/sh -c '(/opt/certbot/makecfg.sh)& certbot'" ]
EXPOSE 80 443
VOLUME /etc/letsencrypt /var/lib/letsencrypt
WORKDIR /opt/certbot

ENV ACCESS_KEY=""
ENV SECRET_KEY=""
ENV RANCHER_API_HOST="http://localhost"
ENV RANCHER_METADATA_HOST="http://rancher-metadata"
ENV HOOK_LABEL_KEY="certbot-hook"
ENV HOOK_LABEL_VALUE="true"
ENV CLOUDXNS_API_KEY=""
ENV CLOUDXNS_SECRET_KEY=""

COPY makecfg.sh ./
COPY entry.sh restart.py hook/

RUN chmod +x makecfg.sh hook/entry.sh
