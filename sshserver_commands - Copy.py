import logging
from typing import Any

logger = logging.getLogger(__name__)

def start_sshserver(args: dict[str, Any]) -> None:
    """
    Main entry point for SSH server mode
    """
    from ghostnet.ghostnet import GhostNet
    ghostnet = GhostNet()
    ghostnet.start_ssh_honeypot()
