import logging
from typing import Any

logger = logging.getLogger(__name__)

def start_main(args: dict[str, Any]) -> None:
    """
    Main entry point for GhostNet 
    """
    from ghostnet.ghostnet import GhostNet
    ghostnet = GhostNet()
    ghostnet.start()
