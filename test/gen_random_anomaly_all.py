import json
import random


target_dir = 'real_topo/'
ar_file = 'random_host.txt'


def gen_random_anomaly(ar):
    anomaly_list = []
    for i in range(24):
        r = random.random()
        if r < ar:
            anomaly_list.append(1)
        else:
            anomaly_list.append(0)
    return anomaly_list


for day in range(30):
    with open(target_dir + ar_file, 'r') as f:
        all_anomalies = {}
        for line in f.readlines():
            if len(line.split(',')) != 4:
                continue
            else:
                number, name, ar_min, ar_max = line.split(',')
                ar_min = float(ar_min)
                ar_max = float(ar_max)
                if ar_min == 0.0:
                    all_anomalies[name] = [0] * 24
                else:
                    all_anomalies[name] = gen_random_anomaly(ar_min)

    with open(target_dir + f'all_anomalies_{day}.json', 'w') as f:
        json.dump(all_anomalies, f)
