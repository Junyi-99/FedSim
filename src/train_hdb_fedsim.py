import os
import sys
from datetime import datetime
import argparse
import numpy as np

from model.vertical_fl.FedSimModel import FedSimModel
from preprocess.hdb import load_both

now_string = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
os.chdir(sys.path[0] + "/../")  # change working directory
root = "data/hdb/"
hdb_dataset = root + "hdb_clean.csv"
school_dataset = root + "school_clean.csv"

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--leak-p', type=float, default=1.0)
parser.add_argument('-g', '--gpu', type=int, default=0)
parser.add_argument('-k', '--top-k', type=int, default=None)
parser.add_argument('--mlp-merge', action='store_true')
parser.add_argument('-ds', '--disable-sort', action='store_true')
parser.add_argument('-dw', '--disable-weight', action='store_true')
args = parser.parse_args()

num_common_features = 2
[X1, X2], y = load_both(hdb_path=hdb_dataset, airbnb_path=school_dataset, active_party='hdb')
name = "hdb_fedsim"

model = FedSimModel(num_common_features=num_common_features,
                    raw_output_dim=10,
                    feature_wise_sim=False,
                    task='regression',
                    metrics=['r2_score', 'rmse'],
                    dataset_type='real',
                    blocking_method='knn',
                    n_classes=2,
                    grid_min=-10.0,
                    grid_max=10.0,
                    grid_width=1.5,
                    knn_k=50,
                    filter_top_k=args.top_k,
                    kd_tree_radius=1e-2,
                    tree_leaf_size=1000,
                    model_name=name + "_" + now_string,
                    val_rate=0.1,
                    test_rate=0.2,
                    drop_key=True,
                    device='cuda:{}'.format(args.gpu),
                    hidden_sizes=[200, 100],
                    train_batch_size=128,
                    test_batch_size=1024 * 4,
                    num_epochs=100,
                    learning_rate=1e-3,
                    weight_decay=1e-4,
                    update_sim_freq=1,
                    num_workers=4 if sys.gettrace() is None else 0,
                    use_scheduler=False, sche_factor=0.1, sche_patience=10, sche_threshold=0.0001,
                    writer_path="runs/{}_{}".format(name, now_string),
                    model_save_path="ckp/{}_{}.pth".format(name, now_string),
                    sim_model_save_path="ckp/{}_{}_sim.pth".format(name, now_string),
                    log_dir="log/{}_{}/".format(name, now_string),
                    # SplitNN parameters
                    local_hidden_sizes=[[200], [200]],
                    agg_hidden_sizes=[100],
                    cut_dims=[100, 100],

                    # fedsim parameters
                    use_conv=True,
                    merge_hidden_sizes=[400],
                    sim_hidden_sizes=[10],
                    merge_model_save_path="ckp/{}_{}_merge.pth".format(name, now_string),
                    merge_dropout_p=0.2,
                    conv_n_channels=8,
                    conv_kernel_v_size=7,
                    mlp_merge=[1600, 1000, 400] if args.mlp_merge else None,
                    disable_sort=args.disable_sort,
                    disable_weight=args.disable_weight,

                    # private link parameters
                    link_epsilon=5e-3,
                    link_delta=5e-3,
                    link_threshold_t=1e-2,
                    sim_leak_p=args.leak_p,
                    link_n_jobs=-1,
                    )
model.train_splitnn(X1, X2, y, scale=True)
# model.train_splitnn(X1, X2, y, scale=True)
