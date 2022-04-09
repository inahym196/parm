from argparse import ArgumentParser, Namespace

from parm.exporter import ExportFactor


def parser() -> Namespace:
    print('hello')
    parser = ArgumentParser(description='cli-tool to manage vsphere authority')
    parser.add_argument('-s', '--host', required=True, help='connect host')
    parser.add_argument('-au', '--auth-user', required=True, help='authenticated user')
    parser.add_argument('-ap', '--auth-pass', required=True, help='authenticated password')

    subparsers = parser.add_subparsers()
    parser_export = subparsers.add_parser('export', help='exporter')
    parser_export.add_argument(
        '-t', '--type', choices=['role', 'mo'], required=True, help='export object Type')
    parser_export.add_argument('-n', '--name', required=False, help='managed-object name')
    parser_export.set_defaults(exportfactor=ExportFactor)

    return parser.parse_args()


def exec():
    args = parser()
    if hasattr(args, 'export'):
        exporter = args.exportfactor()
        exporter.export(args)


if __name__ == '__main__':
    exec()
