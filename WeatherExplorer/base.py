__author__ = 'tangz'


_NEED_TO_IMPLEMENT_THIS_MSG = 'Subclass must implement this'


class BaseColl(object):
    def __init__(self, items):
        self._items = items

    def __getitem__(self, q):
        return QueryResult(self, q)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)


class QueryResult(object):
    def __init__(self, source, queryfn):
        self._queryfn = queryfn
        self._source = source
        self._cached = None
        self._len = None

    @property
    def source(self):
        return self._source

    @property
    def query_func(self):
        return self._queryfn

    def __getitem__(self, q):
        new_queryfn = lambda item: self._queryfn(item) and q(item)
        return self._new_instance(new_queryfn)

    def __iter__(self):
        for elem in self._source:
            if self._queryfn(elem):
                yield elem

    def __len__(self):
        if self._len is None:
            self._len = len([item for item in self._source if self._queryfn(item)])
        return self._len

    def __contains__(self, item):
        return item in self._source and self._queryfn(item)

    def __add__(self, other):
        self._check_common_source(other)
        new_queryfn = lambda item: self._queryfn(item) or other.query_func(item)
        return self._new_instance(new_queryfn)

    def __sub__(self, other):
        self._check_common_source(other)
        new_queryfn = lambda item: self._queryfn(item) and not other.query_func(item)
        return self._new_instance(new_queryfn)

    def __neg__(self):
        new_queryfn = lambda item: not self._queryfn(item)
        return self._new_instance(new_queryfn)

    def _new_instance(self, queryfn):
        return QueryResult(self._source, queryfn)

    def _check_common_source(self, other):
        assert self.source == other.source


# LatLon = collections.namedtuple('LatLon', 'lat lon')