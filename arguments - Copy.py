"""
This module contains the argument manager class
"""

from argparse import ArgumentParser, Namespace, _ArgumentGroup
from typing import Any

from ghostnet.commands.cli_options import AVAILABLE_CLI_OPTIONS


ARGS_MAIN = ["version"]

ARGS_COMMON = [
    "verbosity",
    "print_colorized",
    "version",
]

ARGS_WEBSERVER: list[str] = []
ARGS_SSHSERVER: list[str] = []
ARGS_START: list[str] = []


class Arguments:
    """
    Arguments Class. Manage the arguments received by the cli
    """

    def __init__(self, args: list[str] | None) -> None:
        self.args = args
        self._parsed_arg: Namespace | None = None

    def get_parsed_arg(self) -> dict[str, Any]:
        """
        Return the list of arguments
        :return: List[str] List of arguments
        """
        if self._parsed_arg is None:
            self._build_subcommands()
            self._parsed_arg = self._parse_args()

        return vars(self._parsed_arg)

    def _parse_args(self) -> Namespace:
        """
        Parses given arguments and returns an argparse Namespace instance.
        """
        parsed_arg = self.parser.parse_args(self.args)
        return parsed_arg

    def _build_args(
        self, optionlist: list[str], parser: ArgumentParser | _ArgumentGroup
    ) -> None:
        for val in optionlist:
            opt = AVAILABLE_CLI_OPTIONS[val]
            parser.add_argument(*opt.cli, dest=val, **opt.kwargs)

    def _build_subcommands(self) -> None:
        """
        Builds and attaches all subcommands.
        :return: None
        """
        # Build shared arguments (as group Common Options)
        # Build main command
        self.parser = ArgumentParser(
            prog="ghostnet", description="Honeypot-Based Attack Monitoring System"
        )
        self._build_args(optionlist=ARGS_COMMON, parser=self.parser)

        from ghostnet.commands import start_webserver
        from ghostnet.commands import start_sshserver
        from ghostnet.commands import start_main

        
        subparsers = self.parser.add_subparsers(
            dest="command",
        )

        # Add webserver subcommand
        webserver_cmd = subparsers.add_parser(
            "webserver",
            help="Webserver module.",
        )
        webserver_cmd.set_defaults(func=start_webserver)
        self._build_args(optionlist=ARGS_WEBSERVER, parser=webserver_cmd)

        # Add SSH server subcommand
        sshserver_cmd = subparsers.add_parser(
            "sshserver",
            help="SSH server module.",
        )
        sshserver_cmd.set_defaults(func=start_sshserver)
        self._build_args(optionlist=ARGS_SSHSERVER, parser=sshserver_cmd)

        # Add main command
        main_cmd = subparsers.add_parser(
            "start",
            help="Main module.",
        )
        main_cmd.set_defaults(func=start_main)
        self._build_args(optionlist=ARGS_START, parser=main_cmd)
