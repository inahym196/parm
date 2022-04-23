import sys
from argparse import ArgumentParser
from typing import Optional

from parm.replacer import replace_permission


def run(parser: ArgumentParser):
    args = parser.parse_args()
    print(args)
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
    return sys.exit(0)


class ConnectParser:
    def __init__(self, description: Optional[str]) -> None:
        self._parser = ArgumentParser(description=description)
        self._standard_args_group = self._parser.add_argument_group('Arguments for talking to vCenter')

        self._standard_args_group.add_argument('-s', '--host', help='vSphere service address to connect to')
        self._standard_args_group.add_argument('-o', '--port', type=int, default=443, help='Port to connect to host')
        self._standard_args_group.add_argument('-u', '--user', required=False,
                                               help='User name to use when connecting to host')
        self._standard_args_group.add_argument('-p', '--password', required=False,
                                               help='Password to use when connecting to host')
        self._standard_args_group.add_argument(
            '--nossl', default=False, action='store_true', help='Disable ssl host certificate verification')

    @property
    def parser(self) -> ArgumentParser:
        return self._parser


def replace():
    replace_parser = ConnectParser(description='replace vcenter SSO authority').parser
    replace_file_replace_parser = replace_parser.add_mutually_exclusive_group(required=True)
    replace_file_replace_parser.add_argument('-f', '--filepaths', nargs='+')
    replace_file_replace_parser.add_argument('-a', '--all', action='store_true')
    replace_file_replace_parser.add_argument('-d', '--dir')
    replace_parser.set_defaults(handler=replace_permission)
    run(replace_parser)
