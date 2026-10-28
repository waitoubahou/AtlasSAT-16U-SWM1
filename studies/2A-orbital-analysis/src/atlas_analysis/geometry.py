"""WGS84 surface points and terrestrial Hermite state interpolation; km, s."""
import csv
import numpy as np
from scipy.interpolate import CubicHermiteSpline
A = 6378.137
F = 1/298.257223563
B = A*(1-F)

def unit(vector):
    return vector/np.linalg.norm(vector, axis=-1, keepdims=True)

def geodetic(lat, lon):
    lat, lon = np.radians(lat), np.radians(lon)
    n = A/np.sqrt(1-F*(2-F)*np.sin(lat)**2)
    return np.stack([n*np.cos(lat)*np.cos(lon), n*np.cos(lat)*np.sin(lon),
                     n*(1-F*(2-F))*np.sin(lat)], axis=-1)

def normal_at(lat, lon):
    lat, lon = np.radians([lat, lon])
    return np.array([np.cos(lat)*np.cos(lon), np.cos(lat)*np.sin(lon), np.sin(lat)])

def surface_normal(point):
    return unit(np.asarray(point)/np.array([A*A, A*A, B*B]))

def read_targets(path, optical):
    with open(path, encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    ids = set()
    for row in rows:
        if row["id"] in ids or row["id"] == "REF":
            raise ValueError("Unique agricultural targets required; historical REF is excluded")
        ids.add(row["id"])
        for key in ("latitude_deg", "longitude_deg", "weight_km2"):
            row[key] = float(row[key])
        lat, lon = row["latitude_deg"], row["longitude_deg"]
        if not (-90 <= lat <= 90 and -180 <= lon <= 180 and row["weight_km2"] > 0):
            raise ValueError("Invalid target coordinate or nonpositive area weight")
        row["q"] = geodetic(lat, lon)
        row["normal"] = normal_at(lat, lon)
        row["is_reference"] = False
        center = geodetic(*optical["regional_center_lat_lon_deg"])
        if np.linalg.norm(row["q"]-center) > optical["supported_target_radius_km"]:
            raise ValueError("Target outside validated regional prefilter domain")
    if not rows:
        raise ValueError("No targets")
    return rows

class Orbit:
    def __init__(self, times, state, optical):
        self.t = times
        self.state = state
        self.optical = optical
        self.spline = CubicHermiteSpline(times, state[:, :3], state[:, 3:], extrapolate=False)
    def rv(self, time):
        if np.any(np.asarray(time) < self.t[0]) or np.any(np.asarray(time) > self.t[-1]):
            raise ValueError("Ephemeris extrapolation is forbidden")
        return self.spline(time), self.spline(time, 1)
    def axes(self, time):
        r, v = self.rv(time)
        nadir = -unit(r)
        along = unit(v-(v*nadir).sum(axis=-1, keepdims=True)*nadir)
        cross = np.cross(along, nadir)
        return r, nadir, along, cross

