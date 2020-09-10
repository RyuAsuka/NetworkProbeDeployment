import os
from tqdm import tqdm
import pandas as pd
from sklearn.covariance import MinCovDet
from deployer.AnomalyRate import get_anomaly_rate
from deployer.AnomalyRate import get_max_min_anomaly_rate
from deployer.anomaly_rate_stats import get_anomalies_mode
import json
import random_pick


def get_anomaly(data_array):
    mcd = MinCovDet()
    mcd.fit(data_array)
    support = mcd.support_
    anomaly = []
    for is_not_outline in support:
        if is_not_outline:
            anomaly.append(0)
        else:
            anomaly.append(1)
    return anomaly


def max_length(d):
    max_l = 0
    for key in d:
        if len(d[key]) > max_l:
            max_l = len(d[key])
    return max_l


def get_network(ip):
    split_ip = ip.split('.')
    return '.'.join(split_ip[:3]) + '.0'


# source_dir = 'E:\\data\\CIC-IDS-2018\\output'
target_dir = 'randomly_struct'
# if not os.path.exists(source_dir + '\\' + target_dir):
#     os.mkdir(target_dir)
# # all_ip_files = os.listdir(source_dir)
# all_ip_files = random_pick.random_pick(90)
# all_anomalies = {}
# for row in all_ip_files:
#     for ip in row:
#         ip_data = pd.read_csv(source_dir + '\\' + ip + '.csv', index_col=0)
#         ip_data.drop(columns=['URGs'], inplace=True)
#         all_anomalies[ip] = get_anomalies_mode(ip_data)[0][0]
# with open(target_dir + '/' + 'all_anomalies.json', 'w+') as f:
#     json.dump(all_anomalies, f)
with open('randomly_struct\\all_anomalies.json', 'r') as f:
    all_anomalies = json.load(f)
max_window_size = max_length(all_anomalies)
for w in tqdm(range(1, max_window_size)):
    ip_anomalies = {}
    for ip in tqdm(all_anomalies):
        if get_network(ip) not in ip_anomalies:
            ip_anomalies[get_network(ip)] = []
        try:
            ar_min, ar_max = get_max_min_anomaly_rate(all_anomalies[ip], w)
        except:
            print(ip, w)
        ip_anomalies[get_network(ip)].append((ip, ar_min, ar_max))
    with open(f'{target_dir}/w{w}.txt', 'w+') as f:
        i = 1
        for network in ip_anomalies:
            f.write(f'{len(ip_anomalies[network])}\n')
            for item in ip_anomalies[network]:
                f.write(f'{i},{item[0]},{item[1]},{item[2]}\n')
                i += 1
