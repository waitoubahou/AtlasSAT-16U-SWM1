"""EME2000 -> GCRS/J2000 bias -> ITRF93, with state rotation derivative."""
from pathlib import Path
import numpy as np
import erfa
import spiceypy as sp
from .provenance import sha256

def transform_ephemeris(ephemeris, config, root):
    sp.kclear()
    for kernel in config["kernels"]:
        path = Path(kernel["path"])
        if not path.is_absolute():
            path = root/path
        if sha256(path) != kernel["sha256"]:
            raise ValueError(f"Kernel fingerprint changed: {path}")
        sp.furnsh(str(path))
    et0 = sp.str2et(ephemeris.epoch.replace(tzinfo=None).isoformat())
    tt0 = sp.unitim(et0, "ET", "TDT")
    # UTC calendar elapsed seconds equal TT elapsed only if no leap second intervenes.
    for timestamp, elapsed in zip(ephemeris.epochs[::1000]+[ephemeris.epochs[-1]],
                                  list(ephemeris.times[::1000])+[ephemeris.times[-1]]):
        tt = sp.unitim(sp.str2et(timestamp.replace(tzinfo=None).isoformat()), "ET", "TDT")
        if abs((tt-tt0)-elapsed) > 2e-6:
            raise ValueError("UTC leap-second interval is unsupported; do not use UTC timedelta as SI elapsed")
    epochs = [sp.unitim(tt0+float(t), "TDT", "ET") for t in ephemeris.times]
    rb = erfa.bp00(2451545., 0.)[0]
    bias = np.zeros((6, 6))
    bias[:3, :3] = rb.T
    bias[3:, 3:] = rb.T
    fixed = np.array([sp.sxform("J2000", "ITRF93", et)@bias@state
                      for et, state in zip(epochs, ephemeris.states)])
    sun = np.array([sp.spkpos("SUN", et, "ITRF93", "NONE", "EARTH")[0] for et in epochs])
    return fixed, sun


