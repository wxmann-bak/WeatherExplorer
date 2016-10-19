
__author__ = 'tangz'


_SSHS_CATEGORIES = {1: 65, 2: 85, 3: 100, 4: 115, 5: 140}


def sshs_category(windspeed):
    if windspeed < _SSHS_CATEGORIES[1]:
        return -1
    for cat in range(1, 5):
        if _SSHS_CATEGORIES[cat] <= windspeed < _SSHS_CATEGORIES[cat + 1]:
            return cat
    return 5


def bucket_history(storm, statuses):
    bucketed = {}
    for status in statuses:
        if isinstance(status, int):
            slice_fn = lambda pt: sshs_category(pt.windspd) == status
        else:
            slice_fn = lambda pt: pt.status == status
        bucketed[status] = storm.slice(slice_fn)
    return bucketed

