import os


class FeatureDB:
    def __init__(self, name: str, key_length: int = 2):
        self.path = os.path.join('storage', 'output', name + '.fdb')
        self.index_path = self.path + '-index'
        self.key_length = key_length
        self.data: dict[int, set[int]] = {}
        self.index: dict[int, tuple[int, int]] = {}
        if os.path.isfile(self.path):
            if not os.path.isfile(self.index_path):
                raise Exception('Index file of the database is missing!')
            with open(self.index_path, 'rb') as idx:
                raw_index = idx.read()
            self.key_length = raw_index[0]
            for b in range(1, len(raw_index), self.key_length + 16):
                val2 = b + self.key_length
                self.index[int.from_bytes(raw_index[b:val2])] = (
                    int.from_bytes(raw_index[val2:val2 + 8]),
                    int.from_bytes(raw_index[val2 + 8:val2 + 16])
                )

    def read(self, key: int) -> set[int]:
        with open(self.path, 'rb') as fdb:
            fdb.seek(self.index[key][0])
            data = fdb.read(self.index[key][1] * 8)
        ret = set()
        for b in range(0, len(data), 8):
            ret.add(int.from_bytes(data[b:b + 8]))
        return ret

    def write(self):
        with open(self.path, 'wb') as fdb:
            for k, ids in self.data.items():
                offset = fdb.tell()
                self.index[k] = (offset, len(ids))
                for sid in ids: fdb.write(sid.to_bytes(8))
        with open(self.index_path, 'wb') as idx:
            idx.write(self.key_length.to_bytes(1))
            for sid, v in self.index.items():
                idx.write(sid.to_bytes(self.key_length))
                idx.write(v[0].to_bytes(8))
                idx.write(v[1].to_bytes(8))

    def delete(self):
        os.remove(self.path)
        os.remove(self.index_path)


if __name__ == '__main__':
    my_fdb = FeatureDB('test', 1)
    my_fdb.data = {1: {1001, 1002, 1003}, 2: {1004, 1005, 1006}}
    my_fdb.write()
    print(my_fdb.read(1))
