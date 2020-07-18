from BinaryTree import TreeNode
from DCNode import DCNode
from Solution import Solution


def build_tree(struct, layer):
    """
    From struct string to build a binary tree

    Parameters
    ----------
    struct: list[list[DCNode]]
        The list of generated DCNodes
    layer: int
        The layer of trees

    Returns
    -------
    TreeNode: The root of built tree.
    """
    if len(struct) == 1:
        nodes = []
        for i in range(len(struct[0])):
            node = TreeNode(name=struct[0][i].name + "\'")
            node.right = TreeNode(name=struct[0][i].name,
                                  solutions=[Solution(name=struct[0][i].name,
                                                      cI=0, cM=1,
                                                      pl=struct[0][i].ar_min,
                                                      pu=struct[0][i].ar_max)
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
    build struct lists by file.

    File format:
    A single number, indicating number of next lines belong to which PDU.
    A number of lines with format: name, ar_min, ar_max.

    Parameter
    ---------
    filename: str
        The path of input file.

    Returns
    -------
    list: A list mapping to the PDU networks.
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
