import torch.nn as nn


class CNN1(nn.Module):
    def __init__(self, output_dim=7):
        super(CNN1, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=2),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))

        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=5, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.linear_layer1 = nn.Sequential(
            nn.Dropout2d(0.75),
            nn.Linear(1792, 1024),
            nn.LeakyReLU()
        )

        self.linear_layer2 = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(1024, 256),
            nn.LeakyReLU()
        )

        self.linear_layer3 = nn.Sequential(
            # nn.Dropout(0.2),
            nn.Linear(256, output_dim),
            nn.LeakyReLU()
        )

    def forward(self, x):
        # input: (batch_size,1,max_seq,features)
        # Each layer applies the following matrix tranformation
        # recursively: (batch_size,conv_output,max_seq/2 -1,features/2 -1)
        # CNN
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = out.view(len(out), -1)

        # DNN -- pass through linear layers
        out = self.linear_layer1(out)
        out = self.linear_layer2(out)
        out = self.linear_layer3(out)

        return out
