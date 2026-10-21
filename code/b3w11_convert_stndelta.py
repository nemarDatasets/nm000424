"""d3-fig-stn-delta (Figshare 10.6084/m9.figshare.31359616, CC BY 4.0) -> iEEG-BIDS DERIVATIVE dataset (STN LFP only).

Release (measured, Job ieeg-b3w11-sdprobe-1008000623): patients/pd<NN>/<YYMMDD><l|r>/ session folders. Continuous intracranial
signals exist only as EEGLAB files in stim{off,on}_{left,right}_LFP/ subfolders: 5 channels Ch1..Ch5 (STN microelectrode
LFP), 250 Hz, filtered by the authors (two variants: high-pass 0.5 Hz or 2 Hz; notch-filtered 'filtnotch' or cleaned
'filtCLN'), with task annotations (StimulusOn, KeyPress1, Feedback, StopSignal, ...). The 0.5 Hz high-pass variant is
converted (least filtered); the 2 Hz variant is the same recording with a stronger filter and is not duplicated.
Not converted: single-/multi-unit waveforms and spike times (no BIDS-iEEG format), scalp EEG (not intracranial), epoched files.
Session folder names are surgery dates: they are NOT carried over (sessions are labelled by order; no dates anywhere).
Usage: python b3w11_convert_stndelta.py <work_dir> <bids_root>
"""
import glob
import json
import os
import re
import shutil
import sys
from collections import defaultdict

import mne
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b3w3_common import wjson, write_vhdr, wtsv  # noqa: E402

mne.set_log_level("ERROR")
W, OUT = sys.argv[1], sys.argv[2]
X = os.path.join(W, "extracted", "human-STN-delta_data", "human-STN-delta_data", "patients")
files = sorted(glob.glob(os.path.join(X, "pd*", "*", "stim*_*_LFP", "EEG_filt*_05HP.set")))
rep = {"recordings": [], "skipped": []}
# session order per patient from the (dated) folder names; dates themselves are discarded
sess_dirs = defaultdict(set)
for f in files:
    pt, sd = f.split(os.sep)[-4], f.split(os.sep)[-3]
    sess_dirs[pt].add(sd[:6])
SES = {pt: {d: i + 1 for i, d in enumerate(sorted(ds))} for pt, ds in sess_dirs.items()}
scans = defaultdict(list)
runs = defaultdict(int)
for f in files:
    pt, sd, cond = f.split(os.sep)[-4], f.split(os.sep)[-3], f.split(os.sep)[-2]
    m = re.match(r"stim(off|on)_(left|right)_LFP$", cond)
    variant = os.path.basename(f).split("_")[1]  # filtnotch / filtCLN
    stim, side = m.group(1), m.group(2)
    raw = mne.io.read_raw_eeglab(f, preload=True)
    X_ = raw.get_data() * 1e6  # MNE reads EEGLAB data as µV -> V; back to the file's µV
    fs = raw.info["sfreq"]
    sub = "sub-" + pt
    ses = f"ses-intraop{SES[pt][sd[:6]]}"
    key = (sub, ses, side, stim)
    runs[key] += 1
    stem = f"{sub}_{ses}_task-stopsignal_acq-{side}stim{stim}_run-{runs[key]}"
    D = os.path.join(OUT, sub, ses, "ieeg")
    os.makedirs(D, exist_ok=True)
    X32 = np.ascontiguousarray(X_.T.astype("<f4"))
    X32.tofile(os.path.join(D, stem + "_ieeg.eeg"))
    names = raw.ch_names
    write_vhdr(os.path.join(D, stem + "_ieeg"), len(names), fs, names, ["µV"] * len(names),
               comment="b3w11_convert_stndelta.py: EEGLAB %s (%s) values unchanged as float32 µV" % (os.path.basename(f), variant))
    back = np.fromfile(os.path.join(D, stem + "_ieeg.eeg"), dtype="<f4").reshape(-1, len(names)).T.astype(np.float64)
    err = float(np.max(np.abs(back - X_))) if X_.size else 0.0
    scale = float(np.max(np.abs(X_))) or 1.0
    rt = back.shape == X_.shape and err / scale < 1e-6
    ann = raw.annotations
    wtsv(os.path.join(D, stem + "_events.tsv"), ["onset", "duration", "trial_type", "sample"],
         [[round(float(a["onset"]), 6), round(float(a["duration"]), 6), a["description"], int(round(float(a["onset"]) * fs))] for a in ann])
    hp = "0.5" if "05HP" in f else "2"
    wtsv(os.path.join(D, stem + "_channels.tsv"), ["name", "type", "units", "low_cutoff", "high_cutoff", "sampling_frequency", "group", "status", "status_description", "description"],
         [[c, "DBS", "n/a", hp, "n/a", fs, side, "good", "n/a", "intraoperative STN microelectrode LFP, track %s of the %s hemisphere (release channel name)" % (c, side)] for c in names])
    wjson(os.path.join(D, stem + "_ieeg.json"), {
        "TaskName": "stopsignal",
        "TaskDescription": "Stop-signal reaction time task performed intraoperatively (record; Szabo et al.)",
        "SamplingFrequency": fs, "PowerLineFrequency": 50,
        "SoftwareFilters": {"HighPass": {"CutoffHz": float(hp), "Description": "authors' high-pass (file EEG_%s_05HP.set)" % variant},
                            "Cleaning": {"Description": "authors' 'filtnotch' (notch-filtered) or 'filtCLN' (cleaned) processing; this file: %s" % variant},
                            "Resampling": {"Description": "released at 250 Hz"}},
        "HardwareFilters": "n/a",
        "iEEGReference": "n/a (not stated in the release)",
        "Manufacturer": "n/a",
        "RecordingType": "continuous", "RecordingDuration": round(raw.n_times / fs, 6),
        "DBSChannelCount": len(names), "ECOGChannelCount": 0, "SEEGChannelCount": 0,
        "ElectricalStimulation": stim == "on",
        "ElectricalStimulationParameters": "release folder label 'stim%s' (meaning as in the source; not further described in the record)" % stim,
    })
    scans[(sub, ses)].append([f"ieeg/{stem}_ieeg.vhdr", "n/a"])
    rep["recordings"].append(dict(src=os.path.relpath(f, X).replace(sd, "<session>"), sub=sub, ses=ses, stem=stem, sfreq=fs, n_ch=len(names),
                                  n_samples=int(raw.n_times), n_events=len(ann), variant=variant, max_abs_err_uV=err, roundtrip_ok=bool(rt)))
    print(stem, len(names), raw.n_times, fs, "ev", len(ann), "rt", rt, flush=True)

for (sub, ses), r in scans.items():
    wtsv(os.path.join(OUT, sub, ses, f"{sub}_{ses}_scans.tsv"), ["filename", "acq_time"], sorted(r))
    D = os.path.join(OUT, sub, ses, "ieeg")
    names = sorted({c for rr in rep["recordings"] if rr["sub"] == sub and rr["ses"] == ses for c in ["Ch%d" % k for k in range(1, rr["n_ch"] + 1)]})
    pref = f"{sub}_{ses}"
    wtsv(os.path.join(D, f"{pref}_space-Other_electrodes.tsv"), ["name", "x", "y", "z", "size", "group", "region_stated"],
         [[c, "n/a", "n/a", "n/a", "n/a", "n/a", "subthalamic nucleus (stated in the record; not localised)"] for c in names])
    wjson(os.path.join(D, f"{pref}_space-Other_electrodes.json"), {"region_stated": {"Description": "Target stated in the Figshare record"}, "SpatialReference": "none: no coordinates released"})
    wjson(os.path.join(D, f"{pref}_space-Other_coordsystem.json"), {"iEEGCoordinateSystem": "Other", "iEEGCoordinateUnits": "n/a",
                                                                    "iEEGCoordinateSystemDescription": "No microelectrode coordinates are released; tracks listed with x, y, z = n/a."})
subs = sorted({r["sub"] for r in rep["recordings"]})
wtsv(os.path.join(OUT, "participants.tsv"), ["participant_id", "diagnosis"], [[s, "Parkinson's disease"] for s in subs])
wjson(os.path.join(OUT, "participants.json"), {"diagnosis": {"Description": "Record: patients with Parkinson's disease undergoing DBS surgery"}})
wjson(os.path.join(OUT, "task-stopsignal_events.json"), {"trial_type": {"Description": "EEGLAB event type of the release (e.g. StimulusOn, KeyPress1, Feedback, StopSignal)"},
                                                         "sample": {"Description": "onset x 250 (0-based)"}})
os.makedirs(os.path.join(OUT, "code"), exist_ok=True)
for fn in (os.path.abspath(__file__), os.path.join(os.path.dirname(os.path.abspath(__file__)), "b3w3_common.py")):
    shutil.copy(fn, os.path.join(OUT, "code", os.path.basename(fn)))
json.dump(rep, open(os.path.join(OUT, "code", "conversion_report.json"), "w"), indent=1)
rec = json.load(open(os.path.join(W, "source_record", "figshare_article.json")))
AUTH = [a["full_name"] for a in rec["authors"]]
hrs = sum(r["n_samples"] / r["sfreq"] for r in rep["recordings"]) / 3600
wjson(os.path.join(OUT, "dataset_description.json"), {
    "Name": "Human subthalamic nucleus LFP during a stop-signal task (STN delta; Szabo et al.; derivative, 250 Hz)",
    "BIDSVersion": "1.10.0", "DatasetType": "derivative", "License": "CC-BY-4.0", "Authors": AUTH,
    "HowToAcknowledge": "Cite the Figshare dataset doi:10.6084/m9.figshare.31359616 and the associated article 'Neurons of the human subthalamic nucleus engage with local delta frequency processes during action cancellation'.",
    "ReferencesAndLinks": ["https://doi.org/10.6084/m9.figshare.31359616"],
    "Keywords": ["subthalamic nucleus", "local field potential", "stop-signal task", "response inhibition", "Parkinson's disease", "deep brain stimulation"],
    "SourceDatasets": [{"DOI": "doi:10.6084/m9.figshare.31359616", "URL": "https://figshare.com/articles/dataset/31359616", "Version": "Figshare version %s" % rec.get("version")}],
    "GeneratedBy": [{"Name": "Authors' processing", "Description": "Intraoperative STN microelectrode LFP released as EEGLAB files at 250 Hz, high-pass filtered (0.5 or 2 Hz) and notch-filtered or cleaned."},
                    {"Name": "b3w11_convert_stndelta.py", "Description": "Repackaging of the 0.5 Hz high-pass LFP files to BrainVision float32 µV with unchanged values; annotations to events.tsv; dated folder names dropped. Code in code/."}],
})
open(os.path.join(OUT, "README"), "w").write(f"""# Human STN LFP during a stop-signal task (STN delta) - DERIVATIVE

Intraoperative local field potentials from the subthalamic nucleus (STN) of patients with Parkinson's disease
undergoing DBS surgery, recorded with microelectrodes while they performed a stop-signal reaction time task.

THIS IS A DERIVATIVE DATASET. The release provides the continuous STN LFP only as the authors' filtered 250 Hz EEGLAB
files. Each recording exists in a 0.5 Hz and a 2 Hz high-pass version; only the 0.5 Hz version is included here.

## Source
- Figshare: {', '.join(AUTH)}. "{re.sub('<[^>]+>', '', rec.get('title', ''))}". doi:10.6084/m9.figshare.31359616 (CC BY 4.0).
  Both Figshare files matched their MD5 checksums.
- The original release (human-STN-delta_data.zip, 8.5 GB) also contains single-/multi-unit waveforms and spike times
  (MClust/CellBase), behavioural trial files, scalp EEG (intraoperative and postoperative) and epoched/CSD files. They are
  not repackaged here: BIDS-iEEG has no spike format, scalp EEG is not intracranial, and the epoched files duplicate the
  continuous data. Get them from the Figshare record. The release's session folder names are surgery dates, so they
  are not copied.

## Contents
- {len(subs)} patients (`sub-pd<NN>` = release patient id), {len(rep['recordings'])} recordings, {hrs:.2f} h at 250 Hz.
- `ses-intraop<k>`: intraoperative session k of that patient (ordered by date; dates removed).
- `acq-<side>stim<off|on>`: hemisphere and the release's stimulation label (folder `stim<off|on>_<side>_LFP`).
- Channels Ch1..Ch5: the release's microelectrode tracks (type DBS, values unchanged as float32). Units are `n/a`: the values
  are Inomed ISIS ADC steps of 0.4/65535 (the release's 20 kHz MER data, e.g. pd03 `Ch1_data.mat`, equal the LFP before
  resampling), which the authors' spike code treats as volts (`read_inomed.m`); the amplifier gain is not released.
- `events.tsv`: the EEGLAB annotations (StimulusOn, KeyPress1, Feedback, StopSignal, ...).
- No coordinates are released; electrodes.tsv lists the tracks with x, y, z = n/a and the stated target (STN).

## Privacy
Recording dates (in the release folder names) are dropped. No names were found.
""")
open(os.path.join(OUT, "CHANGES"), "w").write("1.0.0 2026-10-08\n  - Repackaging of the STN LFP of Figshare doi:10.6084/m9.figshare.31359616 (derivative) for NEMAR.\n")
open(os.path.join(OUT, ".bidsignore"), "w").write("code/\n")
print(json.dumps({"recordings": len(rep["recordings"]), "subjects": subs, "hours": hrs, "rt_all": all(r["roundtrip_ok"] for r in rep["recordings"])}))
print("CONVERT_DONE")
