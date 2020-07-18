from src.BinaryTree import post_order
from src.Solution import solve
from src.builders import build_tree, build_struct


if __name__ == '__main__':
    struct = build_struct('20tenants.txt')
    # struct = build_struct('4tenants.txt')
    print(struct)
    tree = build_tree(struct, 0)
    tree.pprint()
    post_seq = post_order(tree)
    for node in post_seq:
        print(f'{node.name}, {node.solutions}, {node.dpr}, {node.is_leaf}')

    best_solution = solve(post_seq)
    print(best_solution)
    print()
    post_seq = post_order(tree)
    for node in post_seq:
        print(f'{node.name}, {node.solutions}, {node.solutions[0].history}, {node.dpr}')
