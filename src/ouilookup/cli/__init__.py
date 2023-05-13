import argparse

from ouilookup import OuiLookup

from .. import __data_filename__, __data_path_defaults__, __data_source_url__, __logger_name__, __title__, __version__
from ..utils import logger_setlevel, output


def cli():
    parser = cli_argparser()
    args = parser.parse_args()

    if args.debug:
        logger_setlevel(name=__logger_name__, loglevel="debug")

    ouilookup = OuiLookup(data_file=args.data_file)

    if args.update is True:
        output(ouilookup.update(), sort_keys=True)

    elif args.update_local:
        output(ouilookup.update(source_data_file=args.update_local), sort_keys=True)

    elif args.status is True:
        output(ouilookup.status(), sort_keys=True)

    elif args.query is not False:
        output(ouilookup.query(expression=args.query))

    else:
        parser.print_help()
        exit(1)


def cli_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="{} v{}".format(__title__, __version__),
        add_help=True,
        epilog="""
            A CLI tool for interfacing with the OuiLookup module that provides CLI access the query(), 
            update() and status() functions.  Outputs at the CLI are JSON formatted allowing for easy chaining with 
            other toolchains. The update() function updates directly from "standards-oui.ieee.org".
        """,
    )

    parser_group0 = parser.add_mutually_exclusive_group()
    parser_group0.add_argument(
        "-q",
        "--query",
        required=False,
        default=False,
        type=str,
        nargs="*",
        metavar="<hwaddr>",
        help=f"Query to locate matching MAC hardware address(es) from the oui {__data_filename__} data file.  "
        f"Addresses may be expressed in formats with or without ':' or '-' separators.  Use a space or comma "
        f"between addresses to query for more than one item in a single query.",
    )
    parser_group0.add_argument(
        "-s",
        "--status",
        required=False,
        default=False,
        action="store_true",
        help=f"Return status metadata about the {__data_filename__} data file.",
    )
    parser_group0.add_argument(
        "-u",
        "--update",
        required=False,
        default=False,
        action="store_true",
        help=f"Download the latest from {__data_source_url__} then parse and save as a {__data_filename__} data file.",
    )
    parser_group0.add_argument(
        "-ul",
        "--update-local",
        metavar="<filename>",
        required=False,
        help=f"Supply a local oui.txt then parse and save as a {__data_filename__} data file.",
    )

    parser_group1 = parser.add_argument_group()
    parser_group1.add_argument(
        "-d", "--debug", required=False, default=False, action="store_true", help="Enable debug logging"
    )
    parser_group1.add_argument(
        "-df",
        "--data-file",
        metavar="<data-file>",
        required=False,
        help=f"Use a data file that is not in the default data file search paths: {', '.join(__data_path_defaults__)}",
    )

    return parser
