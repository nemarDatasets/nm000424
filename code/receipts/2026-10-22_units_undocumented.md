# Receipt: channels.tsv units µV -> n/a (physical units undocumented)

**Claim**: channels.tsv units µV -> n/a (physical units undocumented).

**Source**
- PR head `2639bc3b` (tables unchanged in all later PR commits): the 24 `sub-*/ses-*/ieeg/*_channels.tsv`.
- NEMAR `origin/main` `92f9c770e49343043f94cde181cf55d070ec768f`, read from a copy refreshed on 2026-10-22: the same
  24 tables and the 24 `*_ieeg.vhdr` (tables byte-equal to `origin/main`, header sha256 equal to their git-annex keys).
- Figshare doi:10.6084/m9.figshare.31359616.v2: record description (API v2), file lists of `human-STN-delta_data.zip`
  (2137 entries) and `human-STN-delta_tables.zip` (9 entries), and the 24 converted source files
  `patients/pd<NN>/<session>/stimoff_<side>_LFP/EEG_<filtCLN|filtnotch>_05HP.set`, extracted from Figshare file
  61964647 with Python `zipfile` (member CRC-32 checked).
- Author code: github.com/hangyabalazs/human-STN-delta at `f27fdd64f861e0958d55d6a09ac43d420ea7e4e1` (2024-11-04, the
  commit of the review link; resolves through the GitHub API, 110 files), read from its tarball. It is an ancestor of
  `main` `8a7f480cb9c894a7a2f3fafcf90800f641f3dab2` (120 files); `unit_preprocess/` (6 files) and
  `EEG_LFP_preprocess/load_intraoplfp.m` are the same git blobs in both.

**Method**
- `2026-10-22_units_undocumented.py <head_root> <main_root> <source_root>` (pandas, scipy): per table, row count,
  units in main and head, whether all other columns are identical (string compare), and the unit labels in the main
  header's `[Channel Infos]`; per source `.set` (scipy `loadmat`, all variables except `data`), the number of field
  names and text values matching `unit|volt|µv|uv|mv|gain|scal|calib` (case-insensitive, recursive).
- By hand: the Figshare description states no unit, and neither archive holds a documentation file (extensions .mat,
  .fd, .set, .t, .clusters, .dat, .cfg, .xlsx). In the author code at `f27fdd64`, both `load_intraoplfp.m` files (root
  and `EEG_LFP_preprocess/`) build the LFP from `*MER*.mat` files whose writer (`MER_bigFile`, called by
  `read_inomed.m`) is not in the tree; the only unit wording is the spike threshold comment of `read_inomed.m` and the
  mV plot label of `saveDATasMER.m` (`*EMG*.dat` files). No source states the unit or gain of the released 250 Hz LFP,
  so `units` is `n/a`.

**Result**

| recording | rows | units main -> head | other columns identical | header units | source unit fields/text |
|---|---:|---|---|---|---:|
| sub-pd01_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd02_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd02_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd03_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 3 | µV -> n/a | True | µV | 0 |
| sub-pd04_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd04_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd05_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd05_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd07_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 3 | µV -> n/a | True | µV | 0 |
| sub-pd07_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 3 | µV -> n/a | True | µV | 0 |
| sub-pd08_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd08_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd10_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd10_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd12_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd12_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd13_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd13_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd14_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 3 | µV -> n/a | True | µV | 0 |
| sub-pd14_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 3 | µV -> n/a | True | µV | 0 |
| sub-pd15_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd15_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd16_ses-intraop1_task-stopsignal_acq-leftstimoff_run-1 | 5 | µV -> n/a | True | µV | 0 |
| sub-pd16_ses-intraop1_task-stopsignal_acq-rightstimoff_run-1 | 4 | µV -> n/a | True | µV | 0 |

All 109 rows change µV -> n/a with the other columns unchanged; the current headers keep the µV label written by the
repackaging (the converter in `code/` writes `n/a`); no unit field or text in the source files.

**Coverage**: 24 of 24 channels.tsv, 24 of 24 headers, 24 of 24 converted source files.
