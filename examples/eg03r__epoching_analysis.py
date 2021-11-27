# -*- coding: utf-8 -*-
r"""
=================================
Epoching-based analysis
=================================

"""


# sphinx_gallery_thumbnail_number = 1

# %%
# Importage
# --------------------------------------------------

# KF Tools and related imports
from kftools.data import load_info,fetch_file
from kftools.snirf.eeg import load_snirf_eeg
from mne.io import read_raw_snirf

# Some generic things
from matplotlib import pyplot as plt
import os
import pandas as pd


# %%
# Specify data download location
# --------------------------------------------------

# Give a specific location 
# `data_dir = '/external/rprshnas01/netdata_kcni/jglab/Data/kftools_data'``
# or maybe
# `data_dir = '.'``

# If data_dir=None the default location is used, which is '~/.kftools' 
#data_dir=None

data_dir = '.'



# %%
# List available files
# --------------------------------------------------
info = load_info()
info[['fname', 'site','subid', 'task', 'sesid', 'datetime', 'filetype']]


# %%
# HB Moments file
# ---------------------------------------------------

# The kernel portal gives two .snirf file options: 
# 1. The 'raw' moments file
# 2. A 'Hb moments' file

# The Hb moments file has some initial preprocessing applied to it, 
# including optical density and modified beer lambert law calculations.
 
fetch_file(data_dir=data_dir, filetype='kp-snf-hbm',
           site='snic', task='ft', subid='sub001', sesid='ses01')

f = 'snic_sub001_ft_ses01_0909-1523_kp-snf-hbm.snirf'

raw = read_raw_snirf(f)

fig, ax = plt.subplots(figsize=(12,3))
df_raw[raw.ch_names[0:5]].loc[3000:].plot(ax=ax, title="Hb Moment Time series", xlabel='timepoints')


# %%
# Importing and epoching the EEG
# ---------------------------------------------------
#

# Loading the EEG without epoching:
# The [`load_snirf_eeg()`]() function imports the EEG from the `.snirf` file. 
# If `epoch=True``, it will also epoch the data based on the event descriptions. But for now, we will just import and plot the continuous EEG data 
f = "/nethome/kcni/tmor/scratch/data/kf/test-004_fb46b0d_5.snirf"
raw_eeg=load_snirf_eeg(f, sfreq=1000, epochs=False)
# Transform the eeg file into a dataframe
eeg_df = raw_eeg.to_data_frame()
eeg_df

# Plot the continuous EEG data:
eeg_df.plot(y='Fz', x='time')

# As observed, the EEG data includes drops and peaks. In some periods of time, 

# %%
# Importing the epoched EEG
# ---------------------------------------------------
#

# Loading the EEG with epoching:
## 
f = "/nethome/kcni/tmor/scratch/data/kf/test-004_fb46b0d_5.snirf"
raw_eeg=load_snirf_eeg(f, sfreq=1000, epochs=False)
# Transform the eeg file into a dataframe
eeg_df = raw_eeg.to_data_frame()
eeg_df