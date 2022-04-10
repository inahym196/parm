from parm.parser import Parser, SubParsers
from parm.service_instance import connect, get_mo_by_name


def main():
    parser = Parser()
    parser.add_subparsers(SubParsers.ROLE)
    parser.add_subparsers(SubParsers.MO)
    args = parser.args
    si = connect(args)
    content = si.RetrieveContent()
    authmgr = content.authorizationManager

    if args.subcmd == 'role':
        for role in authmgr.roleList:
            print(role.name, role.roleId)
    elif args.subcmd == 'mo':
        mo = get_mo_by_name(content, args.name)
        entity_permissions = authmgr.RetrieveEntityPermissions(
            entity=mo, inherited=False)
        print(entity_permissions)


if __name__ == '__main__':
    main()
