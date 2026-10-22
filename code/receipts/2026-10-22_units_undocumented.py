"""Units receipt: channels.tsv units, BrainVision header labels and unit fields of the source EEGLAB files.

Usage: python 2026-10-22_units_undocumented.py <head_root> <main_root> <source_root>
"""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.io

UNIT_PATTERN = re.compile(r"unit|volt|µv|\buv\b|\bmv\b|gain|scal|calib", re.IGNORECASE)


def unit_hits(x) -> int:
    if isinstance(x, scipy.io.matlab.mat_struct):
        return sum(bool(UNIT_PATTERN.search(f)) + unit_hits(getattr(x, f)) for f in x._fieldnames)
    if isinstance(x, np.ndarray) and x.dtype == object:
        return sum(unit_hits(e) for e in x.flat)
    if isinstance(x, str):
        return len(UNIT_PATTERN.findall(x))
    return 0


def set_unit_hits(path: Path) -> int:
    names = [n for n, _, _ in scipy.io.whosmat(path) if n != "data"]
    mat = scipy.io.loadmat(path, variable_names=names, struct_as_record=False, squeeze_me=True)
    return sum(bool(UNIT_PATTERN.search(n)) + unit_hits(mat[n]) for n in names)


def header_units(vhdr: Path) -> set[str]:
    section = vhdr.read_text(encoding="utf-8").split("[Channel Infos]")[1].split("\n[")[0]
    return {line.split(",")[-1] for line in section.splitlines() if re.match(r"[^;].*=", line)}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)


head_root, main_root, source_root = (Path(p) for p in sys.argv[1:4])
sources = {}
for path in source_root.glob("**/stimoff_*_LFP/EEG_*_05HP.set"):
    patient = next(p for p in path.parts if re.fullmatch(r"pd\d+", p))
    sources[(patient, path.parent.name.split("_")[1])] = path

print("| recording | rows | units main -> head | other columns identical | header units | source unit fields/text |")
print("|---|---:|---|---|---|---:|")
totals = dict(tables=0, rows=0, sources=0, hits=0)
for tsv in sorted(head_root.glob("sub-*/ses-*/ieeg/*_channels.tsv")):
    rel = tsv.relative_to(head_root)
    stem = tsv.name.removesuffix("_channels.tsv")
    head, main = read_tsv(tsv), read_tsv(main_root / rel)
    same = head.drop(columns="units").equals(main.drop(columns="units"))
    vhdr = main_root / rel.parent / f"{stem}_ieeg.vhdr"
    patient, side = re.search(r"sub-(pd\d+)_.*acq-(left|right)stim", stem).groups()
    source = sources.get((patient, side))
    hits = "missing" if source is None else set_unit_hits(source)
    print(f"| {stem} | {len(head)} | {'/'.join(sorted(set(main['units'])))} -> {'/'.join(sorted(set(head['units'])))} "
          f"| {same} | {'/'.join(sorted(header_units(vhdr)))} | {hits} |")
    totals["tables"] += 1
    totals["rows"] += len(head)
    totals["sources"] += source is not None
    totals["hits"] += 0 if source is None else hits
print(f"\nTotals: {totals}; source files found: {len(sources)}")
