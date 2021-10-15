import os,sys,glob,shutil,numpy as np, pandas as pd
import requests, zipfile,gdown
from datetime import datetime
#from eegnb import DATA_DIR

# dictionary format : kftools -> type -> experiments -> site -> subjects
# the nifti dictionaries include 3 dictionaries each: hbo nifti, hbr nifti, and events.tsv (in this order)

kftools_files_dict = {
    'snirf-mom': {
        'kf-ft':{
            'kcni':{
                0:{'kcni_000_0909-1523_ft_mom.snirf': '11Ji3X72pyQRTMGRQ_9Mt8NS646P6oR4e', 'kcni_000_0917-1313_ft_mom.snirf':'11DEWnSOhEjv3GDRE7d_XKCFtI-7Q2KCc'}}}},
    'snirf-hb': {
            'kf-ft':{
            '   kcni': {0:{'kcni_000_0909-1523_ft_hbm.snirf':'11Lcv-dczig_SLGHcyl8hstE3IS5R8oXO', 'kcni_000_0917-1313_ft_hbm.snirf':'1IOB4DZFDIkWzj9AtxygV8mQE1Ee2mtHt'}}}},
    'nifti': {
           'kf-ft':{
           'kcni':{ 0:{'hbo':{'kcni_000_0909-1523_ft_hbo.nii.gz': '16F2jq5QT-gzbOMyzUU15bD6Uqd3qbh43', 
                             'kcni_000_0917-1313_ft_hbo.nii.gz': '16MM3BKeSTZUeYt9UuKLP43OwdQQ9X2KE'}},
                       'hbr':{'kcni_000_0909-1523_ft_hbr.nii.gz':'16HYwInXlIWpqezHpASP68IxNk3Wme9nI', 
                             'kcni_000_0917-1313_ft_hbr.nii.gz':'16MZ4jDVhC34RnWj4DRwsL4HC0pjKVAfF'}},
                       'events':{'kcni_000_0909-1523_ft_events.tsv':'1DXUIQcbVJg3dc4WAiC7xStbweF9v_4V1',
                               'kcni_000_0917-1313_ft_events.tsv':'1CDrWzSNVIPCRDvQ541T2QLTo0-KmltDY'}}}}



def fetch_dataset(data_dir=None,
    file_type=None,
    experiment=None,
    site="kcni",
    subjects="all",
    download_method="gdown",
    f_ids = [0]):
    """
    Return a long-form filenames list and a table saying what
    subject and session, and run each entry corresponds to
    Usage:
            data_dir = '/my_folder'
            file_type = 'snirf-mom'
            experiment = 'kf-ft'
            subjects = [1]
            # sessions = 'all'
            snirf-mom_kf-ft_fnames = fetch_dataset(data_dir=data_dir, file_type = 'snirf-mom', subjects='all', experiment='kf-ft',
            site='kcni')
            snirf-mom_rec_fnames = fetch_dataset(data_dir=data_dir, file_type = 'snirf-mom', subjects=[1], experiment='rec',
            site='kcni')
    """
    # List of file types available
    file_type_list = [
        "snirf-mom",
        "snirf-hb",
        "nifti"
    ]

    # List of experiments available
    experiments_list = [
        "kf-ft",
        "kf-fl",
        "kf-bh",
        "rec",
        "reo",
        "mmn",
    ]
  
    # List of sub available
    experiments_list = [
        "kf-ft",
        "kf-fl",
        "kf-bh",
        "rec",
        "reo",
        "mmn",
    ]

        

    # If no non-default top-level data path specified, use default
    if data_dir == None:
        data_dir = os.getcwd() #?

    # check parameter entries
    if experiment not in experiments_list:
        raise ValueError("experiment not in database")

    if file_type not in file_type_list:
        raise ValueError("file type not in database")

    if subjects == "all":
        subjects = [0,1,2,3,4,5,6,7,8]

    # selecting the files to download #   
    if file_type == 'nifti':
      hbo_ids = []
      hbr_ids = []
      events_ids = []

      hbo_names = []
      hbr_names = []
      events_names = []
        
      for subject in subjects:
        for i in range(len(kftools_files_dict[file_type[experiment[site[subject['hbo']]]]])):
          hbo_ids.append(kftools_files_dict[file_type[experiment[site[subject[list('hbo'.keys())]]]]])[i]
          hbo_names.append(kftools_files_dict[file_type[experiment[site[subject[list('hbo'.values())]]]]])[i]      
        
          hbr_ids.append(kftools_files_dict[file_type[experiment[site[subject[list('hbr'.keys())]]]]])[i]
          hbr_names.append(kftools_files_dict[file_type[experiment[site[subject[list('hbr'.values())]]]]])[i]
        
          events_ids.append(kftools_files_dict[file_type[experiment[site[subject[list('events'.keys())]]]]])[i]
          events_names.append(kftools_files_dict[file_type[experiment[site[subject[list('events'.values())]]]]])[i]  
    

    else:
        
      files_id = []
      files_name = []

      for subject in subjects:
        for i in range(len(kftools_files_dict[file_type[experiment[site[subject]]]])):
          files_id.append(kftools_files_dict[file_type[experiment[site[list(subject.keys())]]]])[i]
          files_name.append(kftools_files_dict[file_type[experiment[site[list(subject.values())]]]])[i]

        
    # check if data has been previously downloaded
    download_it = False
    exp_dir = os.path.join(data_dir, '/kftools_datasets')
    if not os.path.isdir(exp_dir):
        download_it = True

    if download_it:
        # check if data directory exits. If not, create it
        if os.path.exists(data_dir) is not True:
            os.makedirs(data_dir)

        destination = os.path.join(data_dir, "/kftools_datasets") 

        if download_method == "gdown":
            if file_type == 'nifti':
             for each_file in hbo_ids:
                  URL = "https://drive.google.com/uc?id=" + each_file
                  gdown.download(URL, destination, quiet=False)
        
             for each_file in hbr_ids:
                  URL = "https://drive.google.com/uc?id=" + each_file
                  gdown.download(URL, destination, quiet=False)
        
             for each_file in events_ids:
                  URL = "https://drive.google.com/uc?id=" + each_file
                  gdown.download(URL, destination, quiet=False)        
        
            else:
             for each_file in files_id:
                  URL = "https://drive.google.com/uc?id=" + each_file
                  gdown.download(URL, destination, quiet=False)

        elif download_method == "requests":

            URL = "https://docs.google.com/uc?export=download"

            session = requests.Session()
            response = session.get(
                URL, params={"id": gdrive_locs[experiment]}, stream=True #%????
            )

            # get the confirmation token to download large files
            token = None
            for key, value in response.cookies.items():
                if key.startswith("download_warning"):
                    token = value

            if token:
                params = {"id": id, "confirm": token}
                response = session.get(URL, params=params, stream=True)

            # save content to the zip-file  
            CHUNK_SIZE = 32768
            with open(destination, "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

        # unzip the file
        with zipfile.ZipFile(destination, "r") as zip_ref:
            zip_ref.extractall(data_dir)


    # returning the file directories as a list:
    if file_type == 'nifti':
      hbo_dirs = []
      hbr_dirs = []
      events_dirs = []

      for i in hbo_names:
        file_dir = glob.glob(destination + i)[0]
        hbo_dirs.append(file_dir)        

      for i in hbr_names:
        file_dir = glob.glob(destination + i)[0]
        hbr_dirs.append(file_dir)        

      for i in events_names:
        file_dir = glob.glob(destination + i)[0]
        events_dirs.append(file_dir)        

    else:
      f_dirs = []
      for i in files_name:
        file_dir = glob.glob(destination + i)[0]
        f_dirs.append(file_dir)
        
      return f_dirs

