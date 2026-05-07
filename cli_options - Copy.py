"""
Definition of cli arguments used in arguments.py
"""

from argparse import ArgumentTypeError


def check_int_positive(value: str) -> int:
    try:
        uint = int(value)
        if uint <= 0:
            raise ValueError
    except ValueError:
        raise ArgumentTypeError(
            f"{value} is invalid for this parameter, should be a positive integer value"
        )
    return uint


def check_int_nonzero(value: str) -> int:
    try:
        uint = int(value)
        if uint == 0:
            raise ValueError
    except ValueError:
        raise ArgumentTypeError(
            f"{value} is invalid for this parameter, should be a non-zero integer value"
        )
    return uint


class Arg:
    # Optional CLI arguments
    def __init__(self, *args, **kwargs):
        self.cli = args
        self.kwargs = kwargs


# List of available command line options
AVAILABLE_CLI_OPTIONS = {
    # Common options
    "verbosity": Arg(
        "-v",
        "--verbose",
        help="Verbose mode (-vv for more, -vvv to get all messages).",
        action="count",
    ),
    "version": Arg(
        "-V",
        "--version",
        help="show program's version number and exit",
        action="store_true",
    ),
     "print_colorized": Arg(
        "--no-color",
        help="Disable colorization of hyperopt results. May be useful if you are "
        "redirecting output to a file.",
        action="store_false",
        default=True,
    )
}
