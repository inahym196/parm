
from dataclasses import dataclass
from typing import Any

import yaml
from dacite.core import from_dict


@dataclass
class Permission:
    roleName: str
    principal: str
    propagate: bool = False
    isgroup: bool = False


@dataclass
class ConfigStore:
    vcenter: str
    entityName: str
    permissions: list[Permission]


def load_config(configfile: str) -> ConfigStore:
    with open(configfile, mode='r', encoding='utf-8') as f:
        config: dict[str, Any] = yaml.safe_load(f)
        configstore = from_dict(data_class=ConfigStore, data=config)
    return configstore
