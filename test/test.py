from deployer.BinaryTree import post_order
from deployer.Solution import solve
from deployer.builders import build_tree, build_struct
from deployer.visualizer import create_win, draw_tree_by_midorder
import matplotlib.pyplot as plt


if __name__ == '__main__':
    struct = build_struct('output\\w50.txt')
    # struct = build_struct('4tenants.txt')
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
    print(f"Total DPR count in tree: {dpr_count}")
    tree.pprint()

    # # 可视化
    # _, ax, x, y = create_win(root)
    # draw_tree_by_midorder(root, x, y, ax)
    # plt.show()
