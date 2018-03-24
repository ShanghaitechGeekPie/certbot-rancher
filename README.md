# certbot-rancher
Rancher compatible docker image of EFF's Certbot tool for obtaining TLS/SSL certificates from Let's Encrypt.

This image is built over official certbot-cloudxns plugin support (certbot/dns-cloudxns:latest).

We provide a script which can triger a container restart action through rancher API endpoint automatically. This script will only restart these containsers that with the specific label on the same host. It can be used as a hook of certbot (see [the document](https://certbot.eff.org/docs/using.html#renewing-certificates))

# Configuration

Configuration are given by environment variables:

```
ACCESS_KEY
	default:""
	Access key of rancher API. See API - Keys on your rancher dashboard.

SECRET_KEY
	default:""
	Secret key of rancher API.

RANCHER_API_HOST
	default:"http://localhost"
	Host of the rancher api server.

RANCHER_METADATA_HOST
	default:"http://rancher-metadata"
	Host of the rancher meta-data server using internal DNS. You are not supposed to change it.

HOOK_LABEL_KEY
	default:"certbot-hook"
	Key of the specific label to be trigered.

HOOK_LABEL_VALUE
	default:"true"
	Value of the specific label to be trigered.

CLOUDXNS_API_KEY
	default:""
	API key of cloudxns API.

CLOUDXNS_SECRET_KEY
	default:""
	Secret key of cloudxns API.

```

# Usage

See [Official Certbot Repository](https://github.com/certbot/certbot)
