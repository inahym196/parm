from parm.cli import Parser, SubParsers


def main():
    parser = Parser()
    parser.add_subparsers(SubParsers.ROLE)
    parser.add_subparsers(SubParsers.MO)

    print(parser.args)


if __name__ == '__main__':
    main()
