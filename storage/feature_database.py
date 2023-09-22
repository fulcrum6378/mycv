import os
import struct
from typing import Optional


class FeatureDB:
    ext = 'fdb'

    def __init__(self, name: str, key_length: int = 1):
        self._path = os.path.join('storage', 'output', name + '.' + self.ext)
        self._index_path = self._path + '-index'
        self._key_length: int = key_length
        self._key_type = {1: '>B', 2: '>H', 4: '>I', 8: '>Q'}[key_length]
        self._define_structure()
        self._index: dict[int, tuple[int, int]] = {}

        if os.path.isfile(self._path):
            if not os.path.isfile(self._index_path):
                raise Exception('Index file of the database is missing!')
            with open(self._index_path, 'rb') as idx:
                raw_index = idx.read()
            self._key_length = raw_index[0]
            for b in range(1, len(raw_index), self._key_length + 16):
                val2 = b + self._key_length
                self._index[struct.unpack(self._key_type, raw_index[b:val2])[0]] = (
                    struct.unpack('>Q', raw_index[val2:val2 + 8])[0],
                    struct.unpack('>Q', raw_index[val2 + 8:val2 + 16])[0]
                )

    def _define_structure(self):
        self._data: dict[int, set[int]] = {}

    def read(self, key: int) -> Optional[set[int]]:
        # if key not in self._index: return None  # could make it heavy!
        with open(self._path, 'rb') as fdb:
            fdb.seek(self._index[key][0])
            data = fdb.read(self._index[key][1] * 8)
        ret = set()
        for b in range(0, len(data), 8):
            ret.add(struct.unpack('>Q', data[b:b + 8])[0])
        return ret

    def begin_transaction(self):
        pass

    def insert(self):
        pass

    def delete(self):
        pass

    def end_transaction(self):
        pass

    # items are never going to be UPDATED, except while sorting.
    def edit(self, key: int, value: set[int]) -> bool:
        """ Returns True if calling save_index() is necessary. """
        this_offset = None
        for k in self._index:
            if k < key:  # before this
                continue
            elif k == key:  # on this (which may not exist!)
                this_offset = self._index[k][0]
                dif_items = len(value) - self._index[k][1]
                if dif_items == 0: break
            else:  # after this
                if this_offset is None:
                    this_offset = self._index[k][0]
                    dif_items = len(value)
                else:
                    # noinspection PyUnboundLocalVariable
                    self._index[k] = (self._index[k][0] + (dif_items * 8), self._index[k][1])
        if this_offset is None:
            this_offset = os.path.getsize(self._path) if os.path.isfile(self._path) else 0
            dif_items = len(value)
        self._index[key] = (this_offset, len(value))
        with open(self._path, 'ab') as fdb:  # sometimes it needs to bs `ab`, sometimes `wb` and sometimes THE BOTH!!!
            fdb.seek(this_offset)
            for sid in value: fdb.write(struct.pack('>Q', sid))
        return dif_items != 0

    def save_index(self):
        with open(self._index_path, 'wb') as idx:
            idx.write(struct.pack('>B', self._key_length))
            for k, v in self._index.items():
                idx.write(struct.pack(self._key_type, k))
                idx.write(struct.pack('>Q', v[0]))
                idx.write(struct.pack('>Q', v[1]))


# WE MIGHT NOT NEED `SORTING` THOUGH!

class FractionalFeatureDB(FeatureDB):
    ext = 'ffdb'

    def __init__(self, name: str, key_length: int = 2):
        super().__init__(name, key_length)

    def _define_structure(self):
        self._data: dict[int, list[tuple[int, float]]] = {}

    def read(self, key: int) -> Optional[list[tuple[int, float]]]:
        if key not in self._index: return None
        with open(self._path, 'rb') as fdb:
            fdb.seek(self._index[key][0])
            data = fdb.read(self._index[key][1] * 12)
        ret = list()
        for b in range(0, len(data), 12):
            ret.append((
                struct.unpack('>Q', data[b:b + 8])[0],
                struct.unpack('>f', data[b + 8:b + 12])[0]
            ))
        return ret

    def edit(self, key: int, value: list[tuple[int, float]]):
        # FIX-ME
        self._data[key].sort(key=lambda t: t[1])
        with open(self._path, 'wb') as fdb:
            for k, ids_and_values in self._data.items():
                offset = fdb.tell()
                self._index[k] = (offset, len(ids_and_values))
                for sid, val in ids_and_values:
                    fdb.write(struct.pack('>Q', sid))
                    fdb.write(struct.pack('>f', val))


# open().truncate() MIGHT BE USEFUL TOO, but it just resizes the whole file not a specific portion of it!.

# write tests here.
if __name__ == '__main__':
    my_fdb = FeatureDB('test', 2)
    my_fdb.edit(1, {1001, 1002, 1003})
    my_fdb.edit(2, {1004, 1005, 1006})
    my_fdb.save_index()
    print(my_fdb.read(1))

    # my_ffdb = FractionalFeatureDB('test', 2)
    # my_ffdb.edit(1, [(1001, 1.1), (1002, 1.2), (1003, 1.3)])
    # my_ffdb.edit(2, [(1005, 1.5), (1004, 1.4), (1006, 1.6)])
    # my_ffdb.save_index()
    # print(my_ffdb.read(2))
