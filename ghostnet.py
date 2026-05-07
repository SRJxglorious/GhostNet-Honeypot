import logging

from twisted.internet import reactor, endpoints
from twisted.cred import portal

from ghostnet.config import CONFIG
from ghostnet.data.manager import Manager
from ghostnet.data.handler import MongoHandler

from ghostnet.data.handler import MongoHandler
from ghostnet.loggers import LoggingMixin
from ghostnet.ssh.ssh import LoggingPasswordChecker, SimpleSSHFactory, SimpleSSHRealm

logger = logging.getLogger(__name__)

class GhostNet:
    def __init__(self):
        LoggingMixin.__init__(self, logger)

        self.client = Manager().get_client()

    
    def start_ssh_honeypot(self):

        logger.info("Starting SSH honeypot mode...")
        
        db = self.client["ssh_logs"]
        collection = db["events"]
        
        log = logging.getLogger("ssh")
        log.addHandler(MongoHandler(collection))
        
        ssh_config = CONFIG["ssh_config"]
        ssh_factory = SimpleSSHFactory(ssh_config["version"])
        ssh_realm = SimpleSSHRealm()
        ssh_portal = portal.Portal(ssh_realm)
        ssh_portal.registerChecker(LoggingPasswordChecker())
        ssh_factory.portal = ssh_portal

        endpoint = endpoints.TCP4ServerEndpoint(reactor, ssh_config["port"], interface=ssh_config["hostname"])
        endpoint.listen(ssh_factory)

        reactor.run()

    def start_api_server(self):
        if not CONFIG["enable_api_server"]:
            logger.info("API server is disabled in configuration.")
            return

        from backend.app.app import start_app
        start_app(CONFIG,standalone=True)
    
    def start(self):
        from backend.app.app import start_app
        
        start_app(CONFIG)
        self.start_ssh_honeypot()


