import os
import struct
from typing import Optional


class FeatureDB:
    ext = 'fdb'

    def __init__(self, name: str, key_length: int = 1):
        self.path = os.path.join('storage', 'output', name + '.' + self.ext)
        self.index_path = self.path + '-index'
        self.key_length: int = key_length
        self.key_type = {1: '>B', 2: '>H', 4: '>I', 8: '>Q'}[key_length]
        self.define_structure()
        self.index: dict[int, tuple[int, int]] = {}

        if os.path.isfile(self.path):
            if not os.path.isfile(self.index_path):
                raise Exception('Index file of the database is missing!')
            with open(self.index_path, 'rb') as idx:
                raw_index = idx.read()
            self.key_length = raw_index[0]
            for b in range(1, len(raw_index), self.key_length + 16):
                val2 = b + self.key_length
                self.index[struct.unpack(self.key_type, raw_index[b:val2])[0]] = (
                    struct.unpack('>Q', raw_index[val2:val2 + 8])[0],
                    struct.unpack('>Q', raw_index[val2 + 8:val2 + 16])[0]
                )

    # noinspection PyAttributeOutsideInit
    def define_structure(self):
        self.data: dict[int, set[int]] = {}

    def read(self, key: int) -> Optional[set[int]]:
        if key not in self.index: return None
        with open(self.path, 'rb') as fdb:
            fdb.seek(self.index[key][0])
            data = fdb.read(self.index[key][1] * 8)
        ret = set()
        for b in range(0, len(data), 8):
            ret.add(struct.unpack('>Q', data[b:b + 8])[0])
        return ret

    def write(self):
        with open(self.path, 'wb') as fdb:
            for k, ids in self.data.items():
                offset = fdb.tell()
                self.index[k] = (offset, len(ids))
                for sid in ids: fdb.write(struct.pack('>Q', sid))
        self.write_index()

    def write_index(self):
        with open(self.index_path, 'wb') as idx:
            idx.write(struct.pack('>B', self.key_length))
            for k, v in self.index.items():
                idx.write(struct.pack(self.key_type, k))
                idx.write(struct.pack('>Q', v[0]))
                idx.write(struct.pack('>Q', v[1]))

    def delete(self):
        os.remove(self.path)
        os.remove(self.index_path)

# FIXME FUUUUUUUUUUCK self.data is empty; BECAUSE IT'S NEVER READ! WE SHOULD WRITE IN A WAY THAT...


class FractionalFeatureDB(FeatureDB):
    ext = 'ffdb'

    def __init__(self, name: str, key_length: int = 2):
        super().__init__(name, key_length)

    # noinspection PyAttributeOutsideInit
    def define_structure(self):
        self.data: dict[int, list[tuple[int, float]]] = {}

    def read(self, key: int) -> Optional[list[tuple[int, float]]]:
        if key not in self.index: return None
        with open(self.path, 'rb') as fdb:
            fdb.seek(self.index[key][0])
            data = fdb.read(self.index[key][1] * 12)
        ret = list()
        for b in range(0, len(data), 12):
            ret.append((
                struct.unpack('>Q', data[b:b + 8])[0],
                struct.unpack('>f', data[b + 8:b + 12])[0]
            ))
        return ret

    def write(self):
        with open(self.path, 'wb') as fdb:
            for k, ids_and_values in self.data.items():
                offset = fdb.tell()
                self.index[k] = (offset, len(ids_and_values))
                for sid, val in ids_and_values:
                    fdb.write(struct.pack('>Q', sid))
                    fdb.write(struct.pack('>f', val))
        self.write_index()

    def sort(self, key: int):
        """ DO THIS ON EVERY INSERT OR UPDATE! """
        self.data[key].sort(key=lambda t: t[1])


# write tests here.
if __name__ == '__main__':
    my_fdb = FeatureDB('test', 2)
    my_fdb.data = {1: {1001, 1002, 1003}, 2: {1004, 1005, 1006}}
    my_fdb.write()
    print(my_fdb.read(1))

    my_ffdb = FractionalFeatureDB('test', 2)
    my_ffdb.data = {
        1: [(1001, 1.1), (1002, 1.2), (1003, 1.3)],
        2: [(1005, 1.5), (1004, 1.4), (1006, 1.6)],
    }
    my_ffdb.sort(2)
    my_ffdb.write()
    print(my_ffdb.read(2))
