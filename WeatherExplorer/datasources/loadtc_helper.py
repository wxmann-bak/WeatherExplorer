from WeatherExplorer.tcdata import StormHistory, BasinHistory

__author__ = 'tangz'


class BasinBuilder(object):
    def __init__(self, basin_name):
        self._basin = basin_name
        self._storm_pts = {}

    def __add__(self, pt):
        if pt.storm not in self._storm_pts:
            self._storm_pts[pt.storm] = []
        self._storm_pts[pt.storm].append(pt)
        return self

    def build(self):
        storms = []
        for stormid in self._storm_pts:
            pts_for_storm = self._storm_pts[stormid]
            stormhist = StormHistory.from_hurdat_points(pts_for_storm)
            storms.append(stormhist)
        return BasinHistory(self._basin, storms)