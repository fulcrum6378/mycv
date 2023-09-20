import os


class FeatureDB:
    def __init__(self, name: str, key_length: int = 2):
        self.path = os.path.join('storage', 'output', name + '.fdb')
        self.index_path = self.path + '-index'
        self.key_length = key_length
        self.data: dict[int, set[str]]
        self.index: dict[int, int]

        if not os.path.isfile(self.path):
            self.data = {}
        else:
            if not os.path.isfile(self.index_path):
                raise Exception('Index file of the database is missing!')
            with open(self.index_path, 'rb') as idx:
                self.key_length = idx.read(1)[0]
            self.data = {1: {'a', 'b', 'c'}, 2: {'d', 'e', 'f'}}
            self.index = {}
            # with open(self.path, 'rb') as fdb:
            #    print(fdb.read())

    def write(self):
        self.index = {}
        with open(self.path, 'wb') as fdb:
            for k, v in self.data.items():
                self.index[k] = fdb.tell()
                fdb.write(k.to_bytes(self.key_length))


        with open(self.index_path, 'wb') as idx:
            idx.write(self.key_length.to_bytes(1))

    def delete(self):
        os.remove(self.path)
        os.remove(self.index_path)


FeatureDB('test', 2).write()
