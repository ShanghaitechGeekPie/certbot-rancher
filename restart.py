# -*- coding:utf-8 -*-

import os, urllib, urllib2, json, base64

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
RANCHER_API_HOST = os.getenv('RANCHER_API_HOST')
RANCHER_METADATA_HOST = os.getenv('RANCHER_METADATA_HOST')
HOOK_LABEL_KEY = os.getenv('HOOK_LABEL_KEY')
HOOK_LABEL_VALUE = os.getenv('HOOK_LABEL_VALUE')

def get(url, body = {}, headers = {}):
	req = urllib2.Request(url=url, headers=headers)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	return res

def post(url, body = {}, headers = {}):
	body_encoded = urllib.urlencode(body)
	req = urllib2.Request(url=url, data=body_encoded, headers=headers)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	return res

def get_txt(url, body = {}, headers = {}):
	return get(url, {}, dict(headers, **{'Accept': 'application/txt'}))

def get_json(url, body = {}, headers = {}):
	return get(url, {}, dict(headers, **{'Accept': 'application/json'}))

def post_json(url, body = {}, headers = {}):
	return post(url, {}, dict(headers, **{'Accept': 'application/json'}))

def get_json_auth(url, body = {}, headers = {}):
	base64string = base64.encodestring('%s:%s' % (ACCESS_KEY, SECRET_KEY)).replace('\n', '')
	return get_json(url, {}, dict(headers, **{'Authorization': "Basic {}".format(base64string)}))

def post_json_auth(url, body = {}, headers = {}):
	base64string = base64.encodestring('%s:%s' % (ACCESS_KEY, SECRET_KEY)).replace('\n', '')
	return post_json(url, {}, dict(headers, **{'Authorization': "Basic {}".format(base64string)}))

def get_host_uuid():
	res = get_txt('{}/latest/self/host/uuid/'.format(RANCHER_METADATA_HOST))
	return res

def get_instance_list():
	res = get_json('{}/latest/containers/'.format(RANCHER_METADATA_HOST))
	instance_list = json.loads(res)
	return instance_list

def filter_instance_list(instance_list, host_uuid):
	instance_uuid_list = [instance.get('uuid')
		for instance in instance_list
		if (instance.get('host_uuid') == host_uuid)
			and (instance.get('labels', []).get(HOOK_LABEL_KEY) == HOOK_LABEL_VALUE)
			and instance.get('uuid', False)]
	return instance_uuid_list

def exchange_container_id(instance_uuid_list):
	instance_id_list = []
	for instance_uuid in instance_uuid_list:
		res = get_json_auth('{}/v1/containers/?uuid={}'.format(RANCHER_API_HOST, instance_uuid))
		data = json.loads(res).get('data', [])
		if len(data) == 1:
			instance_id = data[0].get('id', None)
			if instance_id:
				instance_id_list.append(instance_id)
	return instance_id_list

def triger_restart(instance_id_list):
	for instance_id in instance_id_list:
		print('	{}'.format(instance_id))
		res = post_json_auth('{}/v1/containers/{}/?action=restart'.format(RANCHER_API_HOST, instance_id))
	return

def main():
	print('Hook fired')
	host_uuid = get_host_uuid()
	print('Get host uuid: {}'.format(host_uuid))
	instance_list = get_instance_list()
	print('Get {} instance over all'.format(len(instance_list)))
	instance_uuid_list = filter_instance_list(instance_list, host_uuid)
	print('Get {} instance uuid after filtered by {} = {} on the same host'.format(len(instance_uuid_list), HOOK_LABEL_KEY, HOOK_LABEL_VALUE))
	print('	{}'.format(instance_uuid_list))
	instance_id_list = exchange_container_id(instance_uuid_list)
	print('Exchange into {} instance id'.format(len(instance_id_list)))
	print('	{}'.format(instance_id_list))
	print('Restart them...')
	triger_restart(instance_id_list)
	return

if __name__ == "__main__":
	main()
