"""
__main__.py for GhostNet
To launch GhostNet as a module

> python -m ghostnet (with Python >= 3.11)
"""


import logging
import platform
import sys
from typing import Any

from ghostnet import __version__
from ghostnet.commands.arguments import Arguments
from ghostnet.loggers import setup_logging_pre, setup_logging


logger = logging.getLogger(__name__)


def run(sysargv: list[str] | None = None) -> None:
    """
    This function will initiate the bot and start the trading loop.
    :return: None
    """

    return_code: Any = 1
    try:
        setup_logging_pre()
        setup_logging()
        arguments = Arguments(sysargv)
        args = arguments.get_parsed_arg()

        # Call subcommand.
        if args.get("version") or args.get("version_main"):
            """
            Print version information for GhostNet and its key dependencies.
            """
            print(f"Operating System:\t{platform.platform()}")
            print(f"Python Version:\t\tPython {sys.version.split(' ')[0]}")
            print()
            print(f"GhostNet Version:\tGhostNet {__version__}")

            return_code = 0

        elif "func" in args:
            logger.info(f"GhostNet {__version__}")
            return_code = args["func"](args)
        
    except SystemExit as e:  # pragma: no cover
        return_code = e
    except KeyboardInterrupt:
        logger.info("SIGINT received, aborting ...")
        return_code = 0
   
    except Exception:
        logger.exception("Fatal exception!")
    finally:
        sys.exit(return_code)


if __name__ == "__main__":
    run()
