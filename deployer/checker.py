"""
实现下列功能：

1. 为了识别数据中心中所有异常主机，需要检查的主机平均数量。
2. 为了识别一个异常主机，需要检查主机的平均数量。

先决条件：

1. 网络树的前序遍历序列（除去叶子节点）
2. 异常向量矩阵
"""
import json
import numpy as np
import pandas as pd
from deployer.BinaryTree import post_order, pre_order_without_leaf, pre_order
from deployer.Solution import solve
from deployer.builders import build_tree, build_struct


TARGET_DIR = '../test/real_topo/'
STRUCT_FILE = 'random_host.txt'


def get_anomaly_matrix(json_file):
    with open(json_file, 'r') as f:
        all_anomalies = json.load(f)
    anomaly_matrix = []
    for ip in all_anomalies:
        anomaly_matrix.append(all_anomalies[ip])
    return np.array(anomaly_matrix)


def get_average_hosts_to_check(tree_pre_seq, ano_mat):
    all_total_hosts_to_check = []
    all_avg_hosts_to_check = []
    for col in range(ano_mat.shape[1]):
        current_probe = None
        all_distances = []
        d_max = 1
        for i in range(ano_mat.shape[0]):
            if ano_mat[i, col] == 1:
                probe, d = find_nearest_upstream_probe(tree_pre_seq, i+1)
                if not current_probe or probe != current_probe:
                    current_probe = probe
                    if d > d_max:
                        d_max = d
                    all_distances.append(d_max)
                elif current_probe == probe:
                    if d > d_max:
                        d_max = d
        all_distances.append(d_max)
        total_hosts_to_check = sum(all_distances)
        if total_hosts_to_check == 0 or np.sum(ano_mat[:, col]) == 0:
            avg_hosts_to_check = 0
        else:
            avg_hosts_to_check = total_hosts_to_check / np.sum(ano_mat[:, col])
        all_total_hosts_to_check.append(total_hosts_to_check)
        all_avg_hosts_to_check.append(avg_hosts_to_check)
        print(all_total_hosts_to_check, all_avg_hosts_to_check)
    return np.mean(all_total_hosts_to_check), np.mean(all_avg_hosts_to_check)


def find_nearest_upstream_probe(tree_pre_seq, host_no):
    d = 1
    probe = 'root0'
    for node in tree_pre_seq:
        if node.dpr:
            probe = node.name
            d = 1
        if node.right.name == str(host_no):
            return probe, d
        else:
            d += 1


def test_dp(json_file):
    struct = build_struct(TARGET_DIR + STRUCT_FILE)
    print(struct)
    tree = build_tree(struct, 0)
    # tree.pprint()
    post_seq = post_order(tree)
    for node in post_seq:
        print(f'{node.name}, {node.solutions}, {node.dpr}, {node.is_leaf}')

    best_solution = solve(post_seq)
    print(best_solution)
    print()
    post_seq = post_order(tree)
    for node in post_seq:
        print(f'{node.name}, {node.solutions}, {node.solutions[0].history}, {node.dpr}')
    root, final_solution = post_seq[-1], post_seq[-1].solutions[0].history
    print("Final solution: ", final_solution)
    i = 0
    for node in post_seq:
        if not node.is_leaf:
            if final_solution[i] == 0:
                node.dpr = False
            elif final_solution[i] == 1:
                node.dpr = True
            i += 1
    dpr_count = 0
    for node in post_seq:
        if "\'" in node.name:
            print(f'{node.name}({node.ip}): {node.dpr}')
        if 'root' in node.name:
            print(f'{node.name}: {node.dpr}')
        if node.dpr:
            dpr_count += 1
    print(f"Total DPRs in DP Tree: {dpr_count}")

    pre_seq = pre_order_without_leaf(tree)
    print(pre_seq)

    anomaly_matrix = get_anomaly_matrix(json_file)
    total, avg = get_average_hosts_to_check(pre_seq, anomaly_matrix)
    print(total, avg)
    return total, avg


def test_greedy(json_file):
    struct = build_struct(TARGET_DIR + STRUCT_FILE)
    print(struct)
    tree = build_tree(struct, 0)
    # tree.pprint()
    post_seq = post_order(tree)
    for node in post_seq:
        print(f'{node.name}, {node.solutions}, {node.dpr}, {node.is_leaf}')

    pre_seq = pre_order(tree)
    print(pre_seq)
    current_root = None
    dpr_count = 0
    count = 0
    for i in range(len(pre_seq)):
        if not pre_seq[i].is_leaf:
            if 'root' in pre_seq[i].name:
                current_root = pre_seq[i]
                count = 0
            elif current_root and (current_root.left == pre_seq[i] or current_root.right == pre_seq[i]):
                pre_seq[i].dpr = True
                dpr_count += 1
                count += 1
            elif count > 0 and count % 5 == 0:
                pre_seq[i].dpr = True
                dpr_count += 1
                count += 1
            else:
                count += 1

    for node in post_seq:
        if "\'" in node.name:
            print(f'{node.name}({node.ip}): {node.dpr}')
        if 'root' in node.name:
            print(f'{node.name}: {node.dpr}')
    print(f'Total DPRs in Greedy Alg: {dpr_count}')

    pre_seq = pre_order_without_leaf(tree)
    print(pre_seq)

    anomaly_matrix = get_anomaly_matrix(json_file)
    total, avg = get_average_hosts_to_check(pre_seq, anomaly_matrix)
    print(total, avg)
    return total, avg


if __name__ == '__main__':
    result = {
        'total_dp': [],
        'total_gr': [],
        'avg_dp': [],
        'avg_gr': []
    }
    for day in range(30):
        input_file = f'{TARGET_DIR}all_anomalies_{day}.json'
        total_dp, avg_dp = test_dp(input_file)
        total_gr, avg_gr = test_greedy(input_file)
        result['total_dp'].append(total_dp)
        result['total_gr'].append(total_gr)
        result['avg_dp'].append(avg_dp)
        result['avg_gr'].append(avg_gr)
    df = pd.DataFrame(result)
    df.to_excel(TARGET_DIR + 'result.xlsx')
