"""Independent single-segment CCSDS OEM intake. States are km and km/s."""
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

def parse_utc(text):
    value = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    if value.utcoffset().total_seconds() != 0:
        raise ValueError("OEM epochs must be UTC, not a local offset")
    return value

@dataclass
class Ephemeris:
    epoch: datetime
    times: np.ndarray
    states: np.ndarray
    epochs: list
    metadata: dict

def read_oem(path, contract=None):
    metadata, epochs, states = {}, [], []
    in_metadata, segments = False, 0
    for raw in Path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("COMMENT"):
            continue
        if line == "META_START":
            segments += 1
            in_metadata = True
            continue
        if line == "META_STOP":
            in_metadata = False
            continue
        if line.startswith("COVARIANCE"):
            raise ValueError("Covariance blocks are not supported by this reader")
        if "=" in line:
            key, value = map(str.strip, line.split("=", 1))
            metadata[key] = value
            continue
        if not in_metadata:
            cells = line.split()
            if len(cells) != 7:
                raise ValueError(f"Unsupported OEM record: {line[:80]}")
            epochs.append(parse_utc(cells[0]))
            states.append([float(v) for v in cells[1:]])
    if segments != 1 or len(states) < 2:
        raise ValueError("Exactly one OEM segment and at least two states required")
    required = {"CENTER_NAME": "Earth", "REF_FRAME": "EME2000", "TIME_SYSTEM": "UTC"}
    for key, value in required.items():
        if metadata.get(key, "").upper() != value.upper():
            raise ValueError(f"Unsupported {key}: {metadata.get(key)}")
    if metadata.get("CCSDS_OEM_VERS") not in ("1.0", "2.0"):
        raise ValueError("Supported CCSDS OEM versions are 1.0 and 2.0")
    # CCSDS OEM Cartesian mandatory units are km and km/s even when omitted.
    for key, value in metadata.items():
        if "UNIT" in key and value.lower().replace(" ", "") not in ("km", "km/s", "km,km/s"):
            raise ValueError(f"Contrary explicit units: {key}={value}")
    epoch = epochs[0]
    times = np.array([(t-epoch).total_seconds() for t in epochs])
    state = np.asarray(states)
    if not np.isfinite(state).all() or not (np.diff(times) > 0).all():
        raise ValueError("States must be finite and epochs strictly increasing")
    if parse_utc(metadata["START_TIME"]) != epoch or parse_utc(metadata["STOP_TIME"]) != epochs[-1]:
        raise ValueError("OEM start/stop metadata do not match data; truncated export?")
    radii = np.linalg.norm(state[:, :3], axis=1)
    speeds = np.linalg.norm(state[:, 3:], axis=1)
    if not ((radii > 6300).all() and (radii < 100000).all() and (speeds < 20).all()):
        raise ValueError("State scale inconsistent with supported Earth-orbit km/km/s contract")
    if contract:
        if contract.get("expected_start_utc") and epoch != parse_utc(contract["expected_start_utc"]):
            raise ValueError("Epoch differs from explicit analysis configuration; update it intentionally")
        if abs(times[-1]-contract["expected_duration_s"]) > 1e-6:
            raise ValueError("Duration differs from configuration")
        if np.diff(times).max() > contract["max_sample_gap_s"]:
            raise ValueError("OEM cadence too coarse for configured interpolation validation")
    return Ephemeris(epoch, times, state, epochs, metadata)

