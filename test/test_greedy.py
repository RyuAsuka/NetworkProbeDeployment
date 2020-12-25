import os
from deployer.BinaryTree import TreeNode
from deployer.BinaryTree import post_order
from deployer.BinaryTree import pre_order
from deployer.Solution import solve
from deployer.builders import build_tree, build_struct
from deployer.visualizer import create_win, draw_tree_by_midorder
import matplotlib.pyplot as plt


if __name__ == '__main__':
    data_dir = 'real_topo'
    results = []
    # struct = build_struct(f'{data_dir}/autoencoder_result.txt')
    # struct = build_struct('4tenants.txt')
    # struct = build_struct('20tenants.txt')
    struct = build_struct('real_topo/autoencoder_result.txt')
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
    tree.pprint()
