class _visitor:
    def __init__(self, match_first_n=None):
        self.slice_end = match_first_n
        self.cases = {}

    def case(self, *types):
        def call(fun):
            self.cases[types[: self.slice_end]] = fun

        return call

    def __call__(self, *args):
        fun = self.cases[tuple(type(x) for x in args[: self.slice_end])]
        return fun(*args)


def visitor(function=None, match_first_n=None):
    if function:
        return _visitor(match_first_n=match_first_n)
    else:

        def wrapper(_):
            return _visitor(match_first_n=match_first_n)

        return wrapper
