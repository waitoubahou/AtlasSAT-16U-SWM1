"""Midpoint revisit, exact end-to-next-start gaps and area-weighted rolling coverage."""
import numpy as np

MODES = ("geometric", "daylight", "daylight_10deg")

def interval_statistics(values):
    values = np.asarray(values, dtype=float)
    if not len(values):
        return dict.fromkeys(("min", "mean", "median", "max", "p90", "p95"))
    return dict(zip(("min", "mean", "median", "max", "p90", "p95"),
                    map(float, (values.min(), values.mean(), np.median(values),
                                values.max(), np.percentile(values,90), np.percentile(values,95)))))

def exact_gap_statistics(windows, duration):
    windows = sorted(windows, key=lambda w:w["entry_s"])
    if not windows:
        return dict(access_count=0, maximum_complete_gap_h=None,
                    left_censored_h=duration/3600, right_censored_h=duration/3600,
                    no_access_span_h=duration/3600, observed_72h_failure=duration>72*3600)
    # Merge overlapping intervals before computing true no-access gaps.
    merged = []
    for w in windows:
        if merged and w["entry_s"] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], w["exit_s"])
        else:
            merged.append([w["entry_s"], w["exit_s"]])
    gaps = [(b[0]-a[1])/3600 for a,b in zip(merged, merged[1:])]
    left, right = merged[0][0]/3600, (duration-merged[-1][1])/3600
    return dict(access_count=len(windows), maximum_complete_gap_h=max(gaps) if gaps else None,
                left_censored_h=left, right_censored_h=right, no_access_span_h=0.,
                observed_72h_failure=max([left,right]+gaps)>72+1e-6)

def rolling_fractions(time_lists, weights, duration, hours):
    horizon = hours*3600
    starts = np.arange(0, duration-horizon+1, 3600)
    if not len(starts):
        return None
    fractions = np.zeros(len(starts))
    for weight,times in zip(weights, time_lists):
        fractions += weight*(np.searchsorted(times,starts+horizon,side="right") >
                             np.searchsorted(times,starts,side="left"))
    return np.clip(fractions, 0, 1)

def summarize(windows, targets, duration, scenarios):
    indexed = {}
    for window in windows:
        indexed.setdefault((window["scenario"],window["target_id"]),[]).append(window)
    per_target, summaries, subregions = [], [], []
    weights = np.array([p["weight_km2"] for p in targets])
    weights /= weights.sum()
    for scenario in scenarios:
        for mode in MODES:
            lists, pooled, local = [], [], []
            for p in targets:
                selected = [w for w in indexed.get((scenario,p["id"]),[])
                            if mode=="geometric" or w[mode]]
                times = np.array(sorted(w["mid_s"] for w in selected))
                lists.append(times)
                pooled.extend(np.diff(times)/3600)
                row = dict(scenario=scenario, mode=mode,target_id=p["id"],
                           latitude_deg=p["latitude_deg"],longitude_deg=p["longitude_deg"],
                           commune=p.get("subregion",""),weight_km2=p["weight_km2"],
                           **exact_gap_statistics(selected,duration))
                row.update({"midpoint_revisit_"+k+"_h":v for k,v in interval_statistics(np.diff(times)/3600).items()})
                per_target.append(row)
                local.append(row)
            summary = dict(scenario=scenario,mode=mode,grid_points=len(targets),
                           area_km2=float(sum(p["weight_km2"] for p in targets)),
                           targets_with_no_access=sum(r["access_count"]==0 for r in local),
                           targets_with_observed_72h_failure=sum(r["observed_72h_failure"] for r in local),
                           pooled_complete_revisit_h=interval_statistics(pooled),
                           rolling_hourly_coverage={},initial_coverage_fraction={})
            for hours in (24,48,72):
                fractions = rolling_fractions(lists,weights,duration,hours)
                summary["rolling_hourly_coverage"][str(hours)] = None if fractions is None else dict(
                    min=float(fractions.min()),mean=float(fractions.mean()),median=float(np.median(fractions)),
                    max=float(fractions.max()),p05=float(np.percentile(fractions,5)),windows=len(fractions))
                summary["initial_coverage_fraction"][str(hours)] = float(np.dot(weights,[np.any(ts<=hours*3600) for ts in lists]))
            complete = [r["maximum_complete_gap_h"] for r in local if r["maximum_complete_gap_h"] is not None]
            summary["maximum_complete_gap_h"] = max(complete) if complete else None
            summaries.append(summary)
            for commune in sorted({r["commune"] for r in local}):
                group = [r for r in local if r["commune"]==commune]
                gaps = [r["maximum_complete_gap_h"] for r in group if r["maximum_complete_gap_h"] is not None]
                subregions.append(dict(scenario=scenario,mode=mode,commune=commune,targets=len(group),
                                       maximum_complete_gap_h=max(gaps) if gaps else None,
                                       targets_with_no_access=sum(r["access_count"]==0 for r in group),
                                       targets_with_observed_72h_failure=sum(r["observed_72h_failure"] for r in group)))
    return per_target, summaries, subregions


