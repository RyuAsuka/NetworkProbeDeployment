import torch
import torch.nn as nn
import torch.utils.data as datautils
from torch.autograd import Variable as V
import torchvision
import numpy as np
from alive_progress import alive_bar
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.covariance import MinCovDet
from AnomalyRate import get_anomaly, get_anomaly_rate, get_max_min_anomaly_rate
import random


class AutoEncoder(nn.Module):
    """
    自动编码机
    """
    def __init__(self):
        super(AutoEncoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(11, 4),
            nn.Tanh(),
            nn.Linear(4, 3),
            nn.Tanh(),
            nn.Linear(3, 1)
        )

        self.decoder = nn.Sequential(
            nn.Linear(1, 3),
            nn.Tanh(),
            nn.Linear(3, 4),
            nn.Tanh(),
            nn.Linear(4, 11),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded


def setup_seed(seed):
    torch.manual_seed(seed)
    # torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    # torch.backends.cudnn.deterministic = True


if __name__ == '__main__':
    setup_seed(0)
    data_dir = 'E:/data/CIC-IDS-2018/output'
    all_files = os.listdir(data_dir)
    all_results = {}
    outliers = {}

    with alive_bar(len(all_files)) as bar:
        for file in all_files:
            print(file)
            # 读数据
            original_data = pd.read_csv(data_dir + '/' + file, index_col=0)
            original_data.drop(columns=['URGs'], inplace=True)
            data_numpy_format = np.array(original_data.to_numpy())
            min_max_scaler = MinMaxScaler()
            scaled_data = min_max_scaler.fit_transform(data_numpy_format)
            data_numpy_format = torch.from_numpy(scaled_data.astype(np.float32))
            data_tensor = datautils.TensorDataset(data_numpy_format)
            data_loader = datautils.DataLoader(data_tensor, batch_size=100, shuffle=False)

            # 训练
            model = AutoEncoder()
            loss_func = nn.MSELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
            epochs = 500

            processed_data = []
            for epoch in range(epochs):
                total_loss = 0
                for i, (x,) in enumerate(data_loader):
                    encoded, decoded = model(V(x))
                    loss = loss_func(decoded, x)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    total_loss += loss
                if epoch % 50 == 0:
                    print(total_loss.data.numpy())

            for i, (x,) in enumerate(data_tensor):
                encoded, decoded = model(V(x))
                p_data = encoded.data.numpy()
                processed_data.append(p_data[0])

            processed_data = np.array(processed_data)
            print(processed_data)
            mcd = MinCovDet()
            try:
                mcd.fit(processed_data.reshape(-1, 1))
                support_vector = mcd.support_
            except ValueError:
                support_vector = [True] * len(processed_data)
            print(support_vector)
            print(f"Count of Outliers: {(len(support_vector) - sum(support_vector))}/{len(support_vector)}")
            outliers[file[:-4]] = (len(support_vector) - sum(support_vector), len(support_vector))
            anomaly_vector = get_anomaly(support_vector)
            ar_min, ar_max = get_max_min_anomaly_rate(anomaly_vector, 12)
            all_results[file[:-4]] = (ar_min, ar_max)
            bar()

    with open('autoencoder_result.txt', 'w') as f:
        for i, key in enumerate(all_results):
            f.write(f'{i+1},{key},{all_results[key][0]:.2f},{all_results[key][1]:.2f}\n')

    with open('outliers.txt', 'w') as f:
        for key in outliers:
            f.write(f'{key}: {outliers[key][0]}/{outliers[key][1]}\n')
