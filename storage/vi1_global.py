import pickle


class VolatileIndex:
    def __init__(self):
        # first item of the tuple is beginning and the latter is "last item + 1".
        self.fi: dict[int, tuple[int, int]] = {}
        self.yi: dict[int, set[int]] = {}
        self.ui: dict[int, set[int]] = {}
        self.vi: dict[int, set[int]] = {}
        self.ri: dict[int, set[int]] = {}
        # "Position [of a shape] In Frame"
        self.pifi: dict[int, list[tuple[int, int]]] = {}

    def vi_write(self, path: str) -> None:
        pickle.dump(self, open(path, 'wb'))


def vi_read(path: str) -> VolatileIndex:
    return pickle.load(open(path, 'rb'))
