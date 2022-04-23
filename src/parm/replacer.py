from argparse import Namespace

from pyVmomi import vim

from parm.connector import connect
from parm.loader import load_config


def _replace_permission(content: vim.ServiceInstanceContent, filepath: str):
    configstore = load_config(filepath)
    return configstore


def retrieveGlobalContent(content: vim.ServiceInstanceContent) -> tuple[vim.view.ContainerView, list[vim.AuthorizationManager.Permission]]:
    container: vim.Folder = content.rootFolder
    containerview: vim.view.ContainerView = content.viewManager.CreateContainerView(container, [], recursive=True)
    roleList: list[vim.AuthorizationManager.Permission] = content.authorizationManager.roleList
    return (containerview, roleList)


def replace_permission(args: Namespace):

    filepaths: list[str] = []
    if args.filepaths:
        filepaths = args.filepaths

    si = connect(args)
    content = si.RetrieveContent()
    global_content = retrieveGlobalContent(content)

    for filepath in filepaths:
        _replace_permission(content, filepath)

    # authmgr = content.authorizationManager
