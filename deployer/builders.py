from deployer.BinaryTree import TreeNode
from deployer.DCNode import DCNode
from deployer.Solution import Solution


def build_tree(struct, layer):
    """
    从数组结构中生成二叉树

    Parameters
    ----------
    struct: Iterable
        DCNode 组成的可迭代列表
    layer: int
        树的层数

    Returns
    -------
    TreeNode:
        生成的二叉树的根节点
    """
    if len(struct) == 1:
        nodes = []
        for i in range(len(struct[0])):
            node = TreeNode(name=struct[0][i].name + "\'")
            node.right = TreeNode(
                name=struct[0][i].name,
                solutions=[
                    Solution(
                        name=struct[0][i].name,
                        cI=0, cM=1,
                        pl=struct[0][i].ar_min,
                        pu=struct[0][i].ar_max
                    )
                ]
            )
            nodes.append(node)
        for i in range(1, len(nodes)):
            nodes[i - 1].left = nodes[i]
        return nodes[0]
    else:
        if layer == 0:
            root = TreeNode('root' + str(layer), dpr=True)
        else:
            root = TreeNode('root' + str(layer), dpr=False)
        root.left = build_tree(struct[:1], layer + 1)
        root.right = build_tree(struct[1:], layer + 1)
        return root


def build_struct(filename):
    """
    通过文件生成结构

    文件格式：
    一共有 n 组，每组 m+1 行数据，第 1 行是该组中有多少个节点。
    接下来的 m 行，每行表示 1 个节点，用三个数表示。
    第一个数是该节点的名称（用连续的数字表示），第二个数是其最小异常率，第三个数是其最大异常率。

    Parameters
    ----------
    filename: str
        输入文件的路径。

    Returns
    -------
    list:
        一个映射到数据中心网络的列表。
    """
    struct = []
    f = open(filename, 'r')
    all_lines = f.readlines()
    l = 0
    while l < len(all_lines):
        if len(all_lines[l].split(',')) == 1:
            pdu = []
            j = l + 1
            while j < l + int(all_lines[l]) + 1:
                # for j in range(l+1, int(all_lines[l])+1):
                node_info = all_lines[j].split(',')
                pdu.append(
                    DCNode(
                        node_info[0], float(
                            node_info[1]), float(
                            node_info[2])))
                j += 1
            struct.append(pdu)
            l += int(all_lines[l]) + 1
        else:
            raise ValueError(f'File format error in line {l}!')
    return struct

