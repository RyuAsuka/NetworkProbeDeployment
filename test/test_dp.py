import os
import numpy as np
from deployer.BinaryTree import post_order, pre_order_without_leaf
from deployer.Solution import solve
from deployer.builders import build_tree, build_struct
from deployer.visualizer import create_win, draw_tree_by_midorder
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # struct = build_struct(f'{data_dir}/{file}')
    # struct = build_struct('4tenants.txt')
    struct = build_struct('real_topo/random_host.txt')
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

    probe_distance = []
    distance = 1
    for node in pre_seq:
        if node.dpr:
            probe_distance.append(distance)
            distance = 1
        else:
            distance += 1
    print(f'Average distance of each probe: {sum(probe_distance) / dpr_count}')

    tree.pprint()

    # # 可视化
    # _, ax, x, y = create_win(root)
    # draw_tree_by_midorder(root, x, y, ax)
    # plt.show()
