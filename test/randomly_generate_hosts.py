import random


weights = {0.0: 80, 0.2: 10, 0.4: 10}


def generate_random_anomaly_rate_by_list():
    """
    通过产生一个具有权重的数组，再从数组中随机取下标

    Returns
    -------
    float
        返回随机下标对应的异常率值
    """
    all_data = []
    for v, w in weights.items():
        temp = []
        for i in range(w):
            temp.append(v)
        all_data.extend(temp)
    n = random.randint(0, len(all_data) - 1)
    return all_data[n]


with open('real_topo/random_host.txt', 'w+') as f:
    host_no = 1
    for i in range(6):
        if i in [0, 1, 2, 3]:
            f.write('100\n')
            for j in range(100):
                ar = generate_random_anomaly_rate_by_list()
                if ar == 0.0:
                    f.write(f'{str(host_no)},{str(host_no)},0.0,0.0\n')
                else:
                    f.write(f'{str(host_no)},{str(host_no)},{ar},1.0\n')
                host_no += 1
        elif i == 4:
            f.write('30\n')
            for j in range(30):
                ar = generate_random_anomaly_rate_by_list()
                if ar == 0.0:
                    f.write(f'{str(host_no)},{str(host_no)},0.0,0.0\n')
                else:
                    f.write(f'{str(host_no)},{str(host_no)},{ar},1.0\n')
                host_no += 1
        else:
            f.write('20\n')
            for j in range(20):
                ar = generate_random_anomaly_rate_by_list()
                if ar == 0.0:
                    f.write(f'{str(host_no)},{str(host_no)},0.0,0.0\n')
                else:
                    f.write(f'{str(host_no)},{str(host_no)},{ar},1.0\n')
                host_no += 1
