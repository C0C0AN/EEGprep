import os
import warnings
import re

import numpy as np


def validate_sourcedata(path, source_type, pattern='sub-\\d+'):
    """
    This function validates the "sourcedata/" directory provided by user to
    see if it's contents are consistent with BIDS.
    """

    if not path:
        path = './'

    if not source_type:
        source_type = ['eeg']

    # construct relative sourcedata path
    sourcedata_dir = os.path.join(path, 'sourcedata')

    source_name = None

    sub_dirs = []
    n_subs = 0
    subject_names = None

    data_dirs = []
    data_files = []

    # browse through directories in parent_dir
    for root, directories, files in os.walk(path):
        if root == path:
            if 'sourcedata' not in directories:
                raise ValueError('The provided directory does not contain "sourcedata/".')  # noqa: E501
            else:
                source_name = 'OK'

        if root == sourcedata_dir:
            sub_dirs.extend([os.path.join(root, sub) for sub in directories])
            n_subs = len(sub_dirs)

            valid_names = []
            for sub in sub_dirs:
                if re.findall(pattern=pattern,
                              string=os.path.basename(sub)):
                    valid_names.append(True)
                else:
                    valid_names.append(False)

            if len(set(valid_names)) > 1:
                bad_names = np.where(np.logical_not(valid_names))[0]
                bad_names = [sub_dirs[bn] for bn in bad_names]

                warnings.warn('The directory names in "sourcedata/" are not BIDS conform.')  # noqa: E501
                subject_names = 'error in %s' \
                                % (', '.join([str(bn) for bn in bad_names]))
            else:
                subject_names = 'OK'

        elif root in sub_dirs:
            data_dirs.append([data_dir for data_dir in directories
                              if data_dir in source_type])
            n_dirs = [len(d) for d in data_dirs]
            if len(set(n_dirs)) > 1:
                warnings.warn('Subject directories contain different number of subdirectories.')  # noqa: E501
                modal = max(set(n_dirs), key=n_dirs.count)

                inconscistent = [i for i, n in enumerate(n_dirs)
                                 if not n == modal]
                bads = [sub_dirs[i] for i in inconscistent]

        elif root in [os.path.join(s_dir, source)
                      for s_dir in sub_dirs for source in source_type]:
            data_files.extend([os.path.join(root, file) for file in files])

            valid_file_names = []
            file_patterns = [pattern + '_\\w+_' + source + '.*'
                             for source in source_type]

            for file in data_files:
                for file_pattern in file_patterns:
                    if re.findall(pattern=file_pattern,
                                  string=os.path.basename(file)):
                        valid_file_names.append(True)
                    else:
                        valid_file_names.append(False)

            if len(set(valid_file_names)) > 1:
                bad_files = np.where(np.logical_not(valid_file_names))[0]
                bad_files = [data_files[bf] for bf in bad_files]

                warnings.warn('Some file names are not BIDS conform.')
                file_names = 'error in %s' % (', '.join([str(bn)
                                                         for bn in bad_files]))
            else:
                file_names = 'OK'

    data_val = {
        'source_data_path':
            {
                'path': sourcedata_dir,
                'naming': source_name,
                'dirs_in_sourcedata': n_subs
            },
        'subject_directories':
            {
                'name_pattern': pattern,
                'naming': subject_names
            },
        'data_files':
            {
                'file_pattern': (', '.join([f_pat for f_pat in file_patterns])),  # noqa
                'naming': file_names  # noqa
            }
    }

    return data_val



def check_fif(input, output, keep_fif=False):


    if keep_if = True:
      save_file(opj(input_dir, derivatives, filename)

    return data_fif
