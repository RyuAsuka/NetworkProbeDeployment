import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.covariance import MinCovDet
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
from scipy import stats
from AnomalyRate import get_anomaly


def get_mcd_support(data):
    mcd = MinCovDet(random_state=0)
    mcd.fit(data)
    return mcd.support_


def get_anomalies_directly(data_frame):
    support = get_mcd_support(data_frame)
    return generate_result(support)


def get_anomalies_norm(data_frame):
    normalizer = Normalizer()
    data_norm = normalizer.fit_transform(data_frame)
    support = get_mcd_support(data_norm)
    return generate_result(support)


def get_anomalies_pca(data_frame, n_components):
    pca = PCA(n_components=n_components, random_state=0)
    data_pca = pca.fit_transform(data_frame)
    support = get_mcd_support(data_pca)
    return generate_result(support)


def get_anomalies_mode(data_frame):
    all_anomalies = []
    for col in data_frame.columns:
        support_col = get_mcd_support(data_frame[col].to_numpy().reshape(-1, 1))
        all_anomalies.append(generate_result(support_col)[0])
    all_anomalies = np.array(all_anomalies)
    anomalies_mode = stats.mode(all_anomalies, axis=0)[0]
    return anomalies_mode.tolist(), sum(anomalies_mode[0])


def generate_result(support):
    anomalies = get_anomaly(support)
    num_of_anomalies = sum(anomalies)
    return anomalies, num_of_anomalies


def find_min_anomalies():
    data_dir = "E:\\data\\CIC-IDS-2018\\output"
    all_files = os.listdir(data_dir)
    all_results = {}

    for file in tqdm(all_files):
        data_frame = pd.read_csv(data_dir + "\\" + file, index_col=0)
        data_frame.drop(columns=['URGs'], inplace=True)
        ip_addr = file[:-4]
        tqdm.write(ip_addr)
        d_dir, n_dir = get_anomalies_directly(data_frame)
        d_norm, n_norm = get_anomalies_norm(data_frame)
        d_mode, n_mode = get_anomalies_mode(data_frame)
        results = [
            {
                'name': 'directly',
                'num_of_anomalies': int(n_dir),
                'data': d_dir
            },
            {
                'name': 'normalized',
                'num_of_anomalies': int(n_norm),
                'data': d_norm
            },
            {
                'name': 'mode',
                'num_of_anomalies': int(n_mode),
                'data': d_mode
            }
        ]
        for i in range(1, 11):
            d_pca, n_pca = get_anomalies_pca(data_frame, n_components=i)
            results.append({
                'name': 'pca',
                'n_component': int(i),
                'num_of_anomalies': int(n_pca),
                'data': d_pca
            })
        all_results[ip_addr] = results

    with open('all_results.txt', 'w+') as f:
        f.write("{\n")
        for ip in all_results:
            f.write("    " + ip + ": [\n")
            for result in all_results[ip]:
                f.write("    {\n")
                for key in result:
                    f.write("        " + key + ": " + str(result[key]) + ",\n")
                f.write("    },\n")
            f.write("    " + "],\n")
        f.write("}\n")


if __name__ == '__main__':
    find_min_anomalies()
