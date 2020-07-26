import argparse
import joblib

import torch
from torch.utils.data import DataLoader
from dataloading import FeatureExtractorDataset
from training import test


def test_model(modelpath, ifile, **kwargs):
    """ Loads a model and predicts each classes probability

Arguments:

        modelpath {str} : A path where the model was stored.

        ifile {str} : A path of a given wav file,
                      which will be tested.

Returns:

         y_pred {np.array} : An array with the probability of each class
                            that the model predicts.

    """

    # Restore model
    model = joblib.load(modelpath)
    max_seq_length = model.max_sequence_length

    # Move to device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Create test set
    test_set = FeatureExtractorDataset(X=[ifile],
                                       # Random class -- does not matter at all
                                       y=[0],
                                       feature_extraction_method="MEL_SPECTROGRAM",
                                       oversampling=False,
                                       max_sequence_length=max_seq_length)

    # Create test dataloader
    test_loader = DataLoader(dataset=test_set, batch_size=1,
                             num_workers=4, drop_last=False,
                             shuffle=False)

    # Predict some values
    y_pred = test(model=model, dataloader=test_loader,
                  cnn=True, probabilities=True).cpu().detach().numpy()[0]
    print(y_pred)


if __name__ == '__main__':

    # Read arguments -- model
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', required=True,
                        type=str, help='Model')

    parser.add_argument('-i', '--input', required=True,
                        type=str, help='Input file for testing')

    args = parser.parse_args()

    # Get arguments
    model = args.model
    ifile = args.input

    # Test the model
    test_model(modelpath=model, ifile=ifile)
