
from pyVmomi import vim

from parm.parser import Parser, SubParsers
from parm.service_instance import connect, get_mo_by_name, get_roleId_by_name


def main():
    parser = Parser()
    parser.add_subparsers(SubParsers.MO)
    args = parser.args
    si = connect(args)
    content = si.RetrieveContent()
    authmgr = content.authorizationManager
    entity = get_mo_by_name(content, 'Datacenter1')
    roleId = get_roleId_by_name(content, 'ReadOnly')
    principal = 'VSPHERE.LOCAL\\hoge01'
    permission = vim.AuthorizationManager.Permission(principal=principal, roleId=roleId)
    authmgr.SetEntityPermissions(entity=entity, permission=[permission])


if __name__ == '__main__':
    main()
