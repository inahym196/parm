from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Argument:
    name_or_flags: tuple[str, ...]
    options: dict[str, Any]

    def __post_init__(self):
        for name_or_flag in self.name_or_flags:
            assert name_or_flag.startswith('-')


@dataclass
class SubParser:
    name: str
    arguments: Optional[tuple[Argument]] = None
    help: str = ''


class SubParsers:
    ROLE = SubParser(
        name='role',
        arguments=(
            Argument(
                name_or_flags=('-t', '--type',),
                options={'required': True}
            ),
        ),
        help='see `role -h`'
    )
    MO = SubParser(
        name='mo',
        arguments=None,
        help='see `mo -h`'
    )


class Parser:
    def __init__(self) -> None:
        self._parser = ArgumentParser(
            description='Arguments for talking to vCenter')
        self._standard_args_group = self._parser.add_argument_group('standard arguments')
        self._specific_args_group = self._parser.add_argument_group('specific arguments')

        self._standard_args_group.add_argument(
            '-s', '--host', help='vSphere service address to connect to')
        self._standard_args_group.add_argument(
            '-o', '--port', type=int, default=443, help='Port to connect to host')
        self._standard_args_group.add_argument(
            '-u', '--user', required=False, help='User name to use when connecting to host')
        self._standard_args_group.add_argument(
            '-p', '--password', required=False, help='Password to use when connecting to host')
        self._standard_args_group.add_argument(
            '-f', '--config', default='.cred.yml', help='Config to use when connecting to host')
        self._standard_args_group.add_argument(
            '--nossl', default=False, action='store_true', help='Disable ssl host certificate verification')

    def _add_subparser(self, subparser: SubParser):
        _parser = self._subparsers.add_parser(name=subparser.name, help=subparser.help)
        if isinstance(subparser.arguments, tuple):
            for argument in subparser.arguments:
                _parser.add_argument(*argument.name_or_flags, **argument.options)

    def add_subparsers(self, *subparsers: SubParser):
        if not hasattr(self, '_subparsers'):
            self._subparsers = self._parser.add_subparsers()
        for subparser in subparsers:
            self._add_subparser(subparser)

    @property
    def args(self) -> Namespace:
        return self._parser.parse_args()
