"""
定义解集类和求解函数
"""


class Solution(object):
    """
    定义一个二叉树节点的 DPR 插入解

    Parameters
    ----------
    name : str
        该解的名称，应和该解所在节点的名称一致。
    cI : int
        该解中，插入 DPR 的个数
    cM : int
        该解中，该节点下游未插入 DPR 的个数
    pl : float
        该解中的异常率下限（>= 0）
    pu : float
        该解中的异常率上限 (<= 1)
    dpr : bool
        该解中，该节点是否插入 DPR
    history : list of int
        该解下游所有历史解


    Attributes
    ----------
    name : str
        该解的名称，应和该解所在节点的名称一致。
    cI : int, default 0
        该解中，插入 DPR 的个数
    cM : int, default 0
        该解中，该节点下游未插入 DPR 的个数
    pl : float, default 0
        该解中的异常率下限（>= 0）
    pu : float, default 0
        该解中的异常率上限 (<= 1)
    dpr : boolean, default False
        该解中，该节点是否插入 DPR
    history : list of int, optional
        该解下游所有历史解
    """
    def __init__(self, name, cI=0, cM=0, pl=0, pu=0, dpr=False, history=None):
        self.name = name
        self.cI = cI
        self.cM = cM
        self.p = [pl, pu]
        self.dpr = dpr
        if not history:
            self.history = []
        else:
            self.history = history

    def __repr__(self):
        return f'Solution({self.name}: <{self.cI}, {self.cM}, [{self.p[0]}, {self.p[1]}]>, insert_dpr={self.dpr})'

    def __ge__(self, other):
        assert isinstance(other, Solution)
        return self.cI >= other.cI and self.cM >= other.cM and \
               (self.p[0] + self.p[1]) / 2 >= (other.p[0] + other.p[1]) / 2

    def __le__(self, other):
        assert isinstance(other, Solution)
        return self.cI <= other.cI and self.cM <= other.cM and \
               (self.p[0] + self.p[1]) / 2 <= (other.p[0] + other.p[1]) / 2

    def is_valid(self, p_max, c_max):
        """
        判断该解是否合法

        Parameters
        ----------
        p_max : float
            设定的最大异常率，如果该解的异常率超过该阈值，该解会被丢弃。

        Returns
        -------
        bool
            返回指示该解是否合法的 bool 值。
        """
        return (self.p[0] + self.p[1]) / 2 <= p_max and self.cM <= c_max


P_MAX = 0.5
C_MAX = 10


def generate_solutions(node):
    """
    一个节点的解需要并且只需要左右子节点的解。因此，根据左右子节点的解，生成该节点的解。

    Parameters
    ----------
    node: TreeNode
        树节点
    """
    if not node.left:
        for sr in node.right.solutions:
            new_sol = Solution(node.name, 0, 0, 0, 0, False)
            if node.dpr:
                # 当该节点存在DPR时：
                # 1. 该解的cI + 1;
                # 2. 该节点及该节点下游的未发现节点数，即该解的 cM = 0;
                # 3. 该节点及其全部下游节点的异常率范围为 [0, 0];
                new_sol.cI = sr.cI + 1
                new_sol.cM = 0
                new_sol.p = [0, 0]
                new_sol.dpr = True
                new_sol.history.append(1)
            else:
                new_sol.cI = sr.cI
                new_sol.cM = sr.cM
                new_sol.p = [sr.p[0], sr.p[1]]
                new_sol.history.append(0)
            if new_sol.is_valid(P_MAX, C_MAX):
                node.solutions.append(new_sol)
    else:
        for sl in node.left.solutions:
            for sr in node.right.solutions:
                new_sol = Solution(node.name, 0, 0, 0, 0, False,
                                   history=sl.history + sr.history)
                if node.dpr:
                    new_sol.cI = sl.cI + sr.cI + 1
                    new_sol.cM = 0
                    new_sol.p = [0, 0]
                    new_sol.dpr = True
                    new_sol.history.append(1)
                else:
                    new_sol.cI = sl.cI + sr.cI
                    new_sol.cM = sl.cM + sr.cM
                    new_sol.p = [
                        sl.p[0] + sr.p[0] - sl.p[0] * sr.p[0],
                        sl.p[1] + sr.p[1] - sl.p[1] * sr.p[1]
                    ]
                    new_sol.history.append(0)
                if new_sol.is_valid(P_MAX, C_MAX):
                    node.solutions.append(new_sol)


def solve(post_seq):
    """
    后序遍历生成解

    Parameters
    ----------
    post_seq: list of TreeNode
        后序遍历生成的节点序列

    Returns
    -------
    Solution
        根节点的最佳解。
    """
    for node in post_seq:
        # 如果是叶子节点直接保留叶子的解
        if node.is_leaf:
            continue
        if node.name != 'root0':
            for insert_dpr in [False, True]:  # 分别计算不插入/插入 DPR 时生成候选解的情况
                node.dpr = insert_dpr
                generate_solutions(node)
                # 使用其左右子节点生成候选解
                node.solutions = merge_solutions(node.solutions)
        else:
            node.dpr = True
            generate_solutions(node)
            node.solutions = merge_solutions(node.solutions)
    return post_seq[-1].solutions[0]


def merge_solutions(solutions):
    """
    合并解

    Parameters
    ----------
    solutions: list of Solution
        解集列表

    Returns
    -------
    list of Solution
        合并后的解集，其中的每个解都应满足：和其他的解无法比较大小
    """
    i = 0
    while i < len(solutions):
        j = 0
        while j < len(solutions):
            if i == j:
                j += 1
                continue
            if solutions[i] >= solutions[j]:
                del_sol = solutions[i]
                solutions.remove(del_sol)
                if i >= len(solutions) or j >= len(solutions):
                    break
            elif solutions[i] <= solutions[j]:
                del_sol = solutions[j]
                solutions.remove(del_sol)
                if i >= len(solutions) or j >= len(solutions):
                    break
            else:
                j += 1
        i += 1
    return solutions
