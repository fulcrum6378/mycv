import os


def read_database(name: str) -> dict[int, str]:
    path = get_path(name)
    if not os.path.isfile(path):
        create_database(path)
        return {}
    else:
        pass  # TODO


def get_path(name: str, index: bool = False) -> str:
    return os.path.join('storage', 'output', name + '.fdb' + ('-index' if index else ''))


def create_database(path: str):
    write_database(path, {})


def write_database(path: str, data: dict[int, str]):
    pass  # TODO


def update_database(name: str, data: dict[int, str]):
    write_database(get_path(name), data)


def delete_database(name: str):
    os.remove(get_path(name, True))
    os.remove(get_path(name))
