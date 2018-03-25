#!/bin/bash

# if command starts with an option, prepend mysqld
if [ "${1:0:1}" = '-' ]; then
	set -- certbot "$@"
fi

# usage: file_env VAR [DEFAULT]
#    ie: file_env 'XYZ_DB_PASSWORD' 'example'
# (will allow for "$XYZ_DB_PASSWORD_FILE" to fill in the value of
#  "$XYZ_DB_PASSWORD" from a file, especially for Docker's secrets feature)
file_env() {
	local var="$1"
	local fileVar="${var}_FILE"
	local def="${2:-}"
	if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
		echo >&2 "error: both $var and $fileVar are set (but are exclusive)"
		exit 1
	fi
	local val="$def"
	if [ "${!var:-}" ]; then
		val="${!var}"
	elif [ "${!fileVar:-}" ]; then
		val="$(< "${!fileVar}")"
	fi
	export "$var"="$val"
	unset "$fileVar"
}

file_env 'ACCESS_KEY'
file_env 'SECRET_KEY'
file_env 'RANCHER_API_HOST'
file_env 'RANCHER_METADATA_HOST'
file_env 'HOOK_LABEL_KEY'
file_env 'HOOK_LABEL_VALUE'
file_env 'CLOUDXNS_API_KEY'
file_env 'CLOUDXNS_SECRET_KEY'

echo \# CloudXNS API credentials used by Certbot > /opt/certbot/cloudxns.ini
echo dns_cloudxns_api_key = $CLOUDXNS_API_KEY >> /opt/certbot/cloudxns.ini
echo dns_cloudxns_secret_key = $CLOUDXNS_SECRET_KEY >> /opt/certbot/cloudxns.ini

exec "$@"
