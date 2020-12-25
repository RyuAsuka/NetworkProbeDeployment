import os
import numpy as np
from deployer.BinaryTree import post_order, pre_order_without_leaf
from deployer.Solution import Solution, solve2
from deployer.builders import build_tree, build_struct
from deployer.visualizer import create_win, draw_tree_by_midorder
import matplotlib.pyplot as plt
from reprlib import Repr
from pprint import pprint
from alive_progress import alive_bar
from functools import cmp_to_key


def cmp(s1, s2):
    """
    比较两个解的质量

    Parameters
    ----------
    s1 : tuple of (list, deployer.Solution.Solution)
    s2 : tuple of (list, deployer.Solution.Solution)

    Returns
    -------
    int
    """
    if s1[1].cM > s2[1].cM:
        return 1
    elif s1[1].cM < s2[1].cM:
        return -1
    else:
        if s1[1].cI > s2[1].cI:
            return 1
        elif s1[1].cI < s2[1].cI:
            return -1
        else:
            return 0


def clear_post_seq(post_seq):
    for node in post_seq:
        node.dpr = False
        if not node.is_leaf:
            node.solutions.clear()


def get_solutions_repr(solutions):
    retStr = ''
    for sol in solutions:
        retStr += str(sol[0]) + ',' + str(sol[1].quality()) + '\n'
    return retStr


if __name__ == '__main__':
    # 生成二叉树结构，并进行后序遍历得到后序遍历序列
    # struct = build_struct('10eachgroup/random_host.txt')
    struct = build_struct('real_topo/autoencoder_result.txt')
    # pprint(struct)
    tree = build_tree(struct, 0)
    # tree.pprint()
    post_seq = post_order(tree)
    pprint(post_seq)
    print(len(post_seq))

    W = 100
    w_e = 30
    N_GENERATIONS = 200
    result = None

    # 生成初始概率向量 p_0
    p = []
    for i in range(len(post_seq)-1):
        if post_seq[i].is_leaf:
            p.append(0.0)
        else:
            p.append(0.5)
    p.append(1.0)

    print(p)

    # 用于DP解的测试
    # location = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    # print(location)
    # print(len(location))
    # for dpr, node in zip(location, post_seq):
    #     if dpr == 1:
    #         node.dpr = True
    # final_solution, invalid_solutions = solve2(post_seq)
    # print(final_solution, invalid_solutions)

    # 生成种群
    for t in range(N_GENERATIONS):
        pop = []
        for _ in range(W):
            x = []
            for i in range(len(p)):
                if np.random.rand() < p[i]:
                    x.append(1)
                else:
                    x.append(0)
            pop.append(x)

        all_solutions_in_pop = []
        # with alive_bar(len(pop)) as bar:
        for line in pop:
            clear_post_seq(post_seq)
            for dpr, node in zip(line, post_seq):
                if dpr == 1:
                    node.dpr = True
            # pprint(post_seq)
            # print('Solving...')
            final_solution, invalid_solutions = solve2(post_seq)
            # bar()
            final_solution.cM += invalid_solutions
            all_solutions_in_pop.append((line, final_solution))

        # pprint(all_solutions_in_pop)
        all_solutions_in_pop.sort(key=cmp_to_key(cmp))
        # print(get_solutions_repr(all_solutions_in_pop))

        # 交叉熵优化
        p = []
        for j in range(len(post_seq)):
            ones = 0
            for i in range(w_e):
                ones += all_solutions_in_pop[i][0][j]
            p.append(float(ones) / w_e)
        print(p)
        print(all_solutions_in_pop[0][1])
        print()
        result = all_solutions_in_pop[0]

    with open('result_ce_real.txt', 'w+') as f:
        f.write(str(result))
