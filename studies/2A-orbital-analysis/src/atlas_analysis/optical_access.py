"""Continuous pushbroom rectangular angular-footprint access, adapted from frozen v0.4.
No sampled hit test: solve fan-plane crossings, then along/cross angular boundaries.
Ideal roll is independent per target; these windows are not a feasible pointing schedule.
"""
from datetime import timedelta
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, minimize_scalar
from .geometry import geodetic, surface_normal, unit

def utc(epoch, seconds):
    return (epoch + timedelta(seconds=float(seconds))).isoformat(timespec='microseconds').replace('+00:00', 'Z')

def angles(orbit, t, q, roll_limit):
    """Inverse look angles: cross-track alpha, along-track beta after clipped ideal roll. Radians."""
    r, n, a, c = orbit.axes(t)
    los = q - r
    down = np.dot(los, n)
    cross = np.dot(los, c)
    along = np.dot(los, a)
    alpha = np.arctan2(cross, down)
    roll = np.clip(alpha, -roll_limit, roll_limit)
    d = down * np.cos(roll) + cross * np.sin(roll)
    return (alpha, np.arctan2(along, d), roll)

def along_crossings(orbit, q, max_roll=np.radians(23)):
    """Find continuous fan-plane crossings between OEM knots, including interval endpoints. The regional and range filters are valid only within the explicitly bounded configuration domain."""
    if not hasattr(orbit, '_regional_axes'):
        r, n, a, c = orbit.axes(orbit.t)
        keep = np.linalg.norm(r - geodetic(*orbit.optical['regional_center_lat_lon_deg']), axis=1) < orbit.optical['regional_prefilter_km']
        orbit._regional_axes = (r, a, np.flatnonzero(keep))
    r, a, idx = orbit._regional_axes
    signed = np.einsum('ij,j->i', a[idx], q)
    indexes = idx[:-1][(signed[:-1] * signed[1:] <= 0) & (np.diff(idx) == 1)]
    roots = []
    for i in indexes:
        if min(np.linalg.norm(r[i] - q), np.linalg.norm(r[i + 1] - q)) > orbit.optical['candidate_slant_filter_km']:
            continue
        f = lambda t: float(np.dot(q - orbit.rv(t)[0], orbit.axes(t)[2]))
        tc = brentq(f, float(orbit.t[i]), float(orbit.t[i + 1]), xtol=orbit.optical['crossing_xtol_s'])
        rr = orbit.rv(tc)[0]
        if np.dot(surface_normal(q), rr - q) <= 0:
            continue
        alpha = angles(orbit, tc, q, 0.0)[0]
        if abs(alpha) < max_roll and (not roots or tc - roots[-1] > 0.0001):
            roots.append(tc)
    ahalf = np.arctan(orbit.optical['along_track_sample_m'] / 2000 / orbit.optical['reference_altitude_km'])
    for endpoint in [float(orbit.t[0]), float(orbit.t[-1])]:
        rr, nn, aa, cc = orbit.axes(endpoint)
        los = q - rr
        if np.dot(surface_normal(q), rr - q) <= 0:
            continue
        alpha = np.arctan2(np.dot(los, cc), np.dot(los, nn))
        if abs(alpha) < max_roll and abs(np.dot(los, aa)) <= np.tan(ahalf) * np.linalg.norm(los) and (not any((abs(tc - endpoint) < 0.1 for tc in roots))):
            roots.append(endpoint)
    return sorted(roots)

def event_window(orbit, q, normal, tc, swath, roll_deg, along_m=None):
    """Refine millisecond along-track slit entry/exit, then clip cross-track boundaries. A bounded maximum preserves grazing rectangular-footprint corner cases."""
    half = np.arctan(swath / 2 / orbit.optical['reference_altitude_km'])
    ahalf = np.arctan((along_m or orbit.optical['along_track_sample_m']) / 2000 / orbit.optical['reference_altitude_km'])
    roll_limit = np.radians(roll_deg)

    def amargin(t):
        return ahalf - abs(angles(orbit, t, q, roll_limit)[1])
    left = max(float(orbit.t[0]), tc - orbit.optical['window_bracket_halfwidth_s'])
    right = min(float(orbit.t[-1]), tc + orbit.optical['window_bracket_halfwidth_s'])
    ls, rs = (amargin(left), amargin(right))
    if ls >= 0 and left > orbit.t[0] or (rs >= 0 and right < orbit.t[-1]):
        raise ValueError('Increase along-window bracket')
    start = left if ls >= 0 else brentq(amargin, left, tc, xtol=orbit.optical['boundary_xtol_s'])
    end = right if rs >= 0 else brentq(amargin, tc, right, xtol=orbit.optical['boundary_xtol_s'])

    def cmargin(t):
        return half + roll_limit - abs(angles(orbit, t, q, roll_limit)[0])
    cs, ce = (cmargin(start), cmargin(end))
    if cs < 0 and ce < 0:
        fit = minimize_scalar(lambda t: -cmargin(t), bounds=(start, end), method='bounded', options={'xatol': 1e-08})
        if -fit.fun <= 0:
            return None
        peak = fit.x
    else:
        peak = tc
    if cs < 0:
        anchor = end if ce >= 0 else peak
        start = brentq(cmargin, start, anchor, xtol=orbit.optical['boundary_xtol_s'])
    if ce < 0:
        anchor = start if cs >= 0 else peak
        end = brentq(cmargin, anchor, end, xtol=orbit.optical['boundary_xtol_s'])
    if end - start <= 1e-07:
        return None
    mid = (start + end) / 2
    rr = orbit.rv(mid)[0]
    if np.dot(normal, rr - q) <= 0:
        return None
    alpha, beta, roll = angles(orbit, mid, q, roll_limit)
    return (start, end, mid, float(np.degrees(alpha)), float(np.degrees(roll)))

def scenario(swath, roll):
    """Stable scenario name: swath in km and ideal roll limit in degrees."""
    return f'S{swath:02d}_R{roll:02d}'

def solar_elevation(sun_spline, t, q, normal):
    """Geometric topocentric Sun elevation over the WGS84 normal; no refraction."""
    s = sun_spline(t) - q
    return float(np.degrees(np.arcsin(np.clip(np.dot(unit(s), normal), -1, 1))))

def compute(orbit, sun, targets, swaths, rolls, epoch, progress=True):
    """Calculate independent per-target ideal geometric windows and minimum sampled solar elevation at entry/midpoint/exit. No shared pointing or flight schedule is inferred."""
    solar = CubicSpline(orbit.t, sun)
    result = []
    for k, p in enumerate(targets):
        roots = along_crossings(orbit, p['q'], max_roll=np.arctan(max(swaths) / (2 * orbit.optical['reference_altitude_km'])) + np.radians(max(rolls)) + 1e-05)
        for tc in roots:
            alpha = abs(angles(orbit, tc, p['q'], 0.0)[0])
            for sw in swaths:
                half = np.arctan(sw / (2 * orbit.optical['reference_altitude_km']))
                for roll in rolls:
                    if alpha > half + np.radians(roll) + 1e-05:
                        continue
                    win = event_window(orbit, p['q'], p['normal'], tc, sw, roll)
                    if win is None:
                        continue
                    st, en, mid, angle, actual_roll = win
                    sunlo = min((solar_elevation(solar, t, p['q'], p['normal']) for t in (st, en, mid)))
                    result.append({'scenario': scenario(sw, roll), 'target_id': p['id'], 'swath_km': sw, 'roll_limit_deg': roll, 'entry_s': st, 'exit_s': en, 'mid_s': mid, 'entry_utc': utc(epoch, st), 'exit_utc': utc(epoch, en), 'duration_ms': (en - st) * 1000, 'cross_track_angle_deg': angle, 'required_roll_deg': actual_roll, 'min_solar_elevation_deg': sunlo, 'daylight': sunlo >= orbit.optical['solar_elevation_min_deg'], 'daylight_10deg': sunlo >= orbit.optical['solar_elevation_sensitivity_deg']})
        if progress and (k + 1) % 50 == 0:
            print(f'{k + 1}/{len(targets)} targets, {len(result)} windows', flush=True)
    return result
