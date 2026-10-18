[![DOI](https://img.shields.io/badge/DOI-10.82901%2Fnemar.nm000424-blue)](https://doi.org/10.82901/nemar.nm000424)

# Human STN LFP during a stop-signal task (STN delta) - DERIVATIVE

Intraoperative local field potentials from the subthalamic nucleus (STN) of patients with Parkinson's disease
undergoing DBS surgery, recorded with microelectrodes while they performed a stop-signal reaction time task.

THIS IS A DERIVATIVE DATASET. The release provides the continuous STN LFP only as the authors' filtered 250 Hz EEGLAB
files. Each recording exists in a 0.5 Hz and a 2 Hz high-pass version; only the 0.5 Hz version is included here.

## Source
- Figshare: Johanna Petra Szabo, Panna Hegedüs, Tamás Laszlovszky, László Halász, Gabriella Miklós, Bálint Király, György Perczel, Virág Bokodi, László Entz, István Ulbert, Gertrúd Tamás, Dániel Fabó, Loránd Erőss, Balázs Hangya. "Dataset for "Neurons of the human subthalamic nucleus engage with local delta frequency processes during action cancellation"". doi:10.6084/m9.figshare.31359616 (CC BY 4.0).
  Both Figshare files matched their MD5 checksums.
- The original release (human-STN-delta_data.zip, 8.5 GB) also contains single-/multi-unit waveforms and spike times
  (MClust/CellBase), behavioural trial files, scalp EEG (intraoperative and postoperative) and epoched/CSD files. They are
  not repackaged here: BIDS-iEEG has no spike format, scalp EEG is not intracranial, and the epoched files duplicate the
  continuous data. Get them from the Figshare record. The release's session folder names are surgery dates, so they
  are not copied.

## Contents
- 13 patients (`sub-pd<NN>` = release patient id), 24 recordings, 5.13 h at 250 Hz.
- `ses-intraop<k>`: intraoperative session k of that patient (ordered by date; dates removed).
- `acq-<side>stim<off|on>`: hemisphere and the release's stimulation label (folder `stim<off|on>_<side>_LFP`).
- Channels Ch1..Ch5: the release's microelectrode tracks (type DBS, µV, values unchanged as float32).
- `events.tsv`: the EEGLAB annotations (StimulusOn, KeyPress1, Feedback, StopSignal, ...).
- No coordinates are released; electrodes.tsv lists the tracks with x, y, z = n/a and the stated target (STN).

## Privacy
Recording dates (in the release folder names) are dropped. No names were found.

## Ethics
Verbatim from the article of this Figshare dataset, Szabo JP et al. (2026) "Neurons of the human subthalamic nucleus engage with
local delta frequency processes during action cancellation", Nat Commun, doi:10.1038/s41467-026-71502-z (Europe PMC PMC13287684,
Methods, Patient selection):

> "Thirteen patients with Parkinson-disease (6 males; age, 60.92 ± 12.6 years; Supplementary Table S1) undergoing bilateral STN
> DBS implantation (Supplementary Table S2) were enrolled in this study, recruited from the Institute of Neurosurgery and
> Neurointervention (formerly National Institute of Clinical Neuroscience) of Semmelweis University (Budapest, Hungary). Informed
> consent was obtained from all subjects. Informed consent forms and all research protocols were approved by the Institutional
> Research Ethics Committee of NIMNN or its predecessors (OKITI IKEB1/2018; OMIII IKEB 21/2023) and the National Scientific and
> Ethical Committee of the Medical Research Council, Budapest, Hungary (OGYÉI/64814-6/2023)."

The 13 patients of the article are the 13 patients of this dataset.

## Units (added 2026-10-19, version 1.0.3)

The DBS channels (microelectrode LFP tracks Ch1-Ch5) now say `n/a` in channels.tsv and in the BrainVision headers (were `µV`). The values are the release's EEGLAB numbers, unchanged. EEGLAB files carry no unit; the conversion had assumed EEGLAB's µV convention, but the stored numbers are far too small for µV: robust SD after a 1 Hz high-pass 0.003-0.013 (median per run, one run per patient, 13 patients, 19 Oct 2026), i.e. 3-13 nV if they were µV. Read as mV they would be 3-13 µV, plausible for a microelectrode LFP, but this is not established: the intraoperative F4 scalp EEG channel recorded by the same ISIS MER system (release files `stimoff_*/EEG_*.set`, not repackaged) reads 0.0006-0.0007 in the same files, which would be an implausible 0.6 µV in mV, while the postoperative 60-channel Brain Products EEG in the release reads 6-11 (plausible µV). The release and the article (Szabo et al. 2026, Nat Commun, Methods) state no unit. So no unit is assigned.

Reading with MNE: a channel with unit `n/a` is read as volts with scale 1, so `raw.get_data()` returns the release numbers unchanged (before this change MNE multiplied them by 1e-6). Treat them as numbers in an unknown unit; relative measures (spectra shape, phase, event-related changes) are unaffected. Evidence files: fix1019 `out/pubamp/` (Voyager Jobs ieeg-f19-pa-*, 19 Oct 2026).
