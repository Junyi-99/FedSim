import os

files = os.listdir('./')

ori_files = []
opt_files = []
for file in files:
    if file.startswith("log_ori"):
        ori_files.append(file)
    if file.startswith("log_opt"):
        opt_files.append(file)

print(ori_files)
print(opt_files)

ori_tainpart_time = []
ori_training_time = []
for file in ori_files:
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Data concat time"):
                ori_tainpart_time.append(float(line.split()[-1]))
            if line.startswith("Training time (sec)"):
                ori_training_time.append(float(line.split()[-1]))

opt_tainpart_time = []
opt_training_time = []
for file in opt_files:
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Data concat time"):
                opt_tainpart_time.append(float(line.split()[-1]))
            if line.startswith("Training time (sec)"):
                opt_training_time.append(float(line.split()[-1]))

import numpy as np

np.average(ori_tainpart_time)
np.average(ori_training_time)
np.std(ori_tainpart_time)
np.std(ori_training_time)

print("ori_tainpart_time: ", np.average(ori_tainpart_time), np.std(ori_tainpart_time))
print("ori_training_time: ", np.average(ori_training_time), np.std(ori_training_time))

print("opt_tainpart_time: ", np.average(opt_tainpart_time), np.std(opt_tainpart_time))
print("opt_training_time: ", np.average(opt_training_time), np.std(opt_training_time))