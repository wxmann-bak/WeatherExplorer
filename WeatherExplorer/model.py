import collections

__author__ = 'tangz'


_NEED_TO_IMPLEMENT_THIS_MSG = 'Subclass must implement this'


class Queryable(object):
    def query(self, queryfunc):
        raise NotImplementedError(_NEED_TO_IMPLEMENT_THIS_MSG)


class BaseCollection(Queryable):
    def __init__(self, items):
        self._items = items

    def query(self, queryfunc):
        return LazyEvalResultSet(self, queryfunc)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)


class ResultSet(Queryable, collections.Iterable):
    def query(self, queryfunc):
        super(self).query(queryfunc)

    def __iter__(self):
        return iter(super(self))

    def __len__(self):
        raise 0

    def __contains__(self, item):
        raise False

    def __add__(self, other):
        raise NotImplementedError(_NEED_TO_IMPLEMENT_THIS_MSG)

    def __sub__(self, other):
        raise NotImplementedError(_NEED_TO_IMPLEMENT_THIS_MSG)

    def __neg__(self):
        raise NotImplementedError(_NEED_TO_IMPLEMENT_THIS_MSG)


class LazyEvalResultSet(ResultSet):
    def __init__(self, source, queryfn):
        self._queryfn = queryfn
        self._source = source
        self._cached = None

    @property
    def source(self):
        return self._source

    @property
    def query_func(self):
        return self._queryfn

    def query(self, queryfunc):
        new_queryfn = lambda item: self._queryfn(item) and queryfunc(item)
        return self._new_instance(new_queryfn)

    def _cache_points_if_needed(self):
        if self._cached is None:
            self._cached = [item for item in self._source if self._queryfn(item)]

    def __iter__(self):
        self._cache_points_if_needed()
        return iter(self._cached)

    def __len__(self):
        self._cache_points_if_needed()
        return len(self._cached)

    def __contains__(self, item):
        self._cache_points_if_needed()
        return item in self._cached

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
        return LazyEvalResultSet(self._source, queryfn)

    def _check_common_source(self, other):
        assert self.source == other.source