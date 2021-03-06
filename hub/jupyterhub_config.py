import os
import hmac
import hashlib


c.Application.log_level = 'DEBUG'

c.JupyterHub.authenticator_class = 'oauthenticator.mediawiki.MWOAuthenticator'
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.db_url = os.environ['JPY_DB_URL']
c.JupyterHub.db_kwargs = {
    'pool_recycle': 60  # Do not keep connections for more than one minute
}

c.JupyterHub.statsd_host = os.environ.get('STATSD_HOST', 'labmon1001.eqiad.wmnet')
c.JupyterHub.statsd_prefix = os.environ.get('STATSD_PREFIX', 'tools.paws')

c.MWOAuthenticator.client_id = '0a73e346a40b07262b6e36bdba01cba4'
c.MWOAuthenticator.client_secret = '99b284730a79dd30e2c35988be42708ef7e57122'
c.MWOAuthenticator.pass_secrets = True

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.KubeSpawner.kube_namespace = 'paws'

c.Authenticator.admin_users = {'YuviPanda'}
c.JupyterHub.admin_access = True

def generate_mysql_password(spawner):
    h = hmac.new(
        os.environ['MYSQL_HMAC_KEY'].encode('utf-8'),
        spawner.user.name.encode('utf-8'),
        hashlib.sha256
    )
    return h.hexdigest()


def generate_mysql_username(spawner):
    return spawner.user.name


c.KubeSpawner.environment = {
    'MYSQL_HOST': os.environ['MYSQL_SERVICE_HOST'],
    'MYSQL_USERNAME': generate_mysql_username,
    'MYSQL_PASSWORD': generate_mysql_password
}

c.KubeSpawner.kube_api_endpoint = 'https://%s' % os.environ['KUBERNETES_SERVICE_HOST']
c.KubeSpawner.hub_ip_connect = '%s:%s' % (os.environ['HUB_SERVICE_HOST'], os.environ['HUB_SERVICE_PORT'])
c.JupyterHub.ip =  os.environ['PAWS_SERVICE_HOST']
c.JupyterHub.proxy_api_ip =  os.environ['PROXYAPI_SERVICE_HOST']
c.JupyterHub.proxy_api_port = 8001
c.KubeSpawner.kube_ca_path = False
c.KubeSpawner.kube_token = os.environ['INSECURE_KUBE_TOKEN']
c.KubeSpawner.singleuser_image_spec = 'docker-registry.tools.wmflabs.org/pawsuser:latest'
c.KubeSpawner.volumes = [
    {
        'name': 'home',
        'hostPath': {
            'path': '/data/project/paws/userhomes/{userid}'
        }
    },
    {
        'name': 'dumps',
        'hostPath': {
            'path': '/public/dumps/',
        }
    }
]
c.KubeSpawner.volume_mounts = [
    {
        'mountPath': '/home/paws',
        'name': 'home'
    },
    {
        'mountPath': '/public/dumps/',
        'name': 'dumps',
        }
]
c.KubeSpawner.start_timeout = 60 * 5  # First pulls can be really slow


c.JupyterHub.base_url = '/paws/'
