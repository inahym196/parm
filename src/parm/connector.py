import atexit
from argparse import Namespace
from typing import Any, Optional

import yaml
from pyvim.connect import Disconnect, SmartConnect


def get_roleId_by_name(content: Any, name: str):
    authmgr = content.authorizationManager
    for role in authmgr.roleList:
        if role.name == name:
            return role.roleId


def get_mo_by_name(content: Any, name: str) -> Any:
    containerview = content.viewManager.CreateContainerView(
        container=content.rootFolder, type=[], recursive=True)
    for child in containerview.view:
        if child.name == name:
            return child


def get_connect_info(configfile: str) -> tuple[str, str, str]:
    with open(configfile, encoding='utf-8') as f:
        config: dict[str, Any] = yaml.safe_load(f)
        host = config.get('hostname', '')
        user = config.get('username', '')
        password = config.get('password', '')
    return (host, user, password)


def connect(args: Namespace, config: str = '.cred.yml'):
    service_instance: Optional[Any] = None
    host = ''
    user = ''
    password = ''
    nossl = False
    port = args.port

    host, user, password = get_connect_info(config)

    if args.user:
        user = args.user
    if args.password:
        password = args.password
    if args.nossl:
        nossl = args.nossl

    service_instance = SmartConnect(host=host,
                                    user=user,
                                    pwd=password,
                                    port=port,
                                    disableSslCertValidation=nossl
                                    )
    atexit.register(Disconnect, service_instance)

    if not service_instance:
        raise SystemError('Unable to connect to host with supplied credentials.')

    return service_instance
