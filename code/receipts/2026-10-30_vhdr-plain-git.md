# Receipt: BrainVision headers say n/a, committed as plain git text files

**Claim**: the 24 `.vhdr` headers, annexed with unit µV at `origin/main`, are plain git text files at the PR head whose
channel units are n/a, as in channels.tsv. Only the unit fields and the converter comment line differ from the annexed
files; no `.eeg` or `.vmrk` file changes.

**PR**: nemarDatasets/nm000424#3, header commit `e336e62df8292ebfc65ad21aac25618debb89767` (the receipt commit adds
only this receipt's two files).

## Source
- NEMAR nm000424 `origin/main` `92f9c770e49343043f94cde181cf55d070ec768f`: the 24 annexed `*_ieeg.vhdr`, fetched from the
  NEMAR annex (public S3 prefix `nemar/nm000424/objects/`); the sha256 of each equals its git-annex key (column 2).
- PR head: the 24 headers (git blobs) and the channels.tsv and `_ieeg.json` of the 24 recordings, read with `git show`.
- Mechanism as in nemarDatasets/nm000509 `432a7a42`: the annex pointer of the `.vhdr` is replaced by the header text, a
  plain git blob (mode 100644); no `.gitattributes` change. Here the files were added with
  `git -c annex.largefiles=nothing add`.

## Method
- Header text: the annexed file with the two edits that `code/b3w11_convert_stndelta.py` makes at this head: the unit
  field of every `Ch<n>=` record `µV` -> `n/a`, and the comment `... values unchanged as float32 µV` ->
  `... values unchanged as float32 (unit not stated in the release)`.
- `2026-10-30_vhdr-plain-git.py <clone> <PR head> <dir with the origin/main headers>` (Python 3.12.15, pandas 3.1.0),
  per header: annexed at `origin/main` with sha256 = key; plain git blob with mode 100644 at the head; changed lines
  (difflib, classed as unit field, comment, SamplingInterval or other); header units vs channels.tsv units per channel
  (same names in the same order); header rate (1e6 / SamplingInterval) vs `_ieeg.json` SamplingFrequency and
  channels.tsv sampling_frequency; `.eeg` (annex pointer) and `.vmrk` (git text) blobs at the head equal to those at
  `origin/main`.

## Result (script output)

| recording | origin/main: annexed, sha256 = key | head | lines changed | channels | units header / channels.tsv | units agree | rate header / ieeg.json / channels.tsv (Hz) | rate agrees | .eeg and .vmrk as on origin/main |
|---|---|---|---|---:|---|---:|---|---|---|
| sub-pd01_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd02_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd02_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd03_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 3 | 3 | n/a / n/a | 3/3 | 250 / 250 / 250 | True | True |
| sub-pd04_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd04_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd05_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd05_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd07_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 3 | 3 | n/a / n/a | 3/3 | 250 / 250 / 250 | True | True |
| sub-pd07_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 3 | 3 | n/a / n/a | 3/3 | 250 / 250 / 250 | True | True |
| sub-pd08_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd08_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd10_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd10_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd12_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd12_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd13_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd13_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd14_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 3 | 3 | n/a / n/a | 3/3 | 250 / 250 / 250 | True | True |
| sub-pd14_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 3 | 3 | n/a / n/a | 3/3 | 250 / 250 / 250 | True | True |
| sub-pd15_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd15_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd16_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | True True | plain git | comment 1, unit 5 | 5 | n/a / n/a | 5/5 | 250 / 250 / 250 | True | True |
| sub-pd16_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | True True | plain git | comment 1, unit 4 | 4 | n/a / n/a | 4/4 | 250 / 250 / 250 | True | True |

Totals: {'headers': 24, 'plain': 24, 'key_ok': 24, 'names_ok': 24, 'rate_ok': 24, 'data_same': 24, 'channels': 109, 'units_ok': 109, 'changed': 24, 'comment': 24, 'unit': 109}

Files changed by the PR (origin/main...head): 54; by suffix: {'CHANGES': 1, '.md': 2, '.py': 2, '.json': 1, '.tsv': 24, '.vhdr': 24} (at the header commit; no `.eeg` or `.vmrk` among them.)

All 24 headers are plain git text at the head with n/a in all 109 channel records, matching the 109 channels.tsv rows;
the only changed lines are the 109 unit fields and the 24 comment lines; the rates are unchanged (250 Hz, as in
`_ieeg.json` and channels.tsv); the 24 `.eeg` (same annex keys) and 24 `.vmrk` are unchanged from `origin/main`.

## Coverage
24 of 24 headers (109 of 109 channel records), 24 of 24 channels.tsv and `_ieeg.json`, 24 of 24 `.eeg` and `.vmrk`.

## Reproduce
```
uv run --no-project --python 3.12 --with pandas python code/receipts/2026-10-30_vhdr-plain-git.py \
  <nm000424 git clone> e336e62df8292ebfc65ad21aac25618debb89767 <dir with the 24 origin/main headers>
```
Run on 2026-10-30 (header text only, no signal data read); the table is verbatim from its output.
