import argparse
import torch
from torch.utils.data import DataLoader
from dataloading.dataloading import FeatureExtractorDataset
from lib.training import test
from utils.model_editing import drop_layers
import config
import os
import glob
import numpy as np
import pickle

import deep_retrieval_build_db


def search_deep_database(database_path, query_wav):
    with open(database_path, 'rb') as f:
        all_features = pickle.load(f)
        f_names = pickle.load(f)
        audio_files = pickle.load(f)
        models_folder = pickle.load(f)

    models = deep_retrieval_build_db.load_models(models_folder)
    f, f_names = deep_retrieval_build_db.get_meta_features(query_wav, models)

    import scipy.spatial.distance
    print(f.reshape(-1,1).shape)
    print(all_features.shape)
    d = scipy.spatial.distance.cdist(f.reshape(-1,1).T, all_features)[0]
    print([x for _, x in sorted(zip(d, audio_files))])
    print(d)


if __name__ == '__main__':
    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', required=True,
                        type=str, help='Dir of models')
    parser.add_argument('-i', '--input', required=True,
                        type=str, help='Input file for testing')
    args = parser.parse_args()

    search_deep_database(args.db, args.input)