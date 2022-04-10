from parm.cli import Parser, SubParsers
from parm.service_instance import connect


def main():
    parser = Parser()
    parser.add_subparsers(SubParsers.ROLE)
    parser.add_subparsers(SubParsers.MO)
    args = parser.args
    si = connect(args)
    # content = si.RetrieveContent()
    # authorizationManager = content.authorizationManager
    # print(authorizationManager.roleList[0].privilege)
    # for role in authorizationManager.roleList:


if __name__ == '__main__':
    main()
