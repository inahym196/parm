import atexit
from argparse import Namespace
from typing import Any, Optional

import yaml
from pyvim.connect import Disconnect, SmartConnect


def _get_connect_info_from_file(config_file: str) -> tuple[str, str, str, bool]:
    host = ''
    user = ''
    password = ''
    nossl = False

    with open(config_file, 'r', encoding='UTF-8') as f:
        config: dict[str, Any] = yaml.safe_load(f)
        host = config.get('hostname', '')
        user = config.get('username', '')
        password = config.get('password', '')
        nossl = config.get('nossl', '')
    return (host, user, password, nossl)


def connect(args: Namespace):
    service_instance: Optional[Any] = None
    host = ''
    user = ''
    password = ''
    nossl = False
    port = args.port

    if args.config:
        host, user, password, nossl = _get_connect_info_from_file(args.config)

    if args.host:
        host = args.host
    if args.user:
        user = args.user
    if args.password:
        password = args.password
    if args.nossl:
        nossl = args.nossl

    print(host, user, password, port, nossl)
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
