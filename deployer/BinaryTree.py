"""
参考了 BinaryTree 库，定义了二叉树结点，树的表示方法等
"""


def _build_tree_string(root, curr_index, index=False, delimiter='-'):
    """
    递归地生成表示树的字符串。

    Parameters
    ----------
    root: TreeNode
        树的根节点。
    curr_index: int
        当前节点的标号。
    index: boolean, default=False
        （作用暂且不明）
    delimiter: str, default='-'
        树的节点之间的连接符

    Returns
    -------
    tuple(list, int, int, int):
        树的节点的字符串表示。
    """
    if root is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    if index:
        node_repr = '{}{}{}'.format(curr_index, delimiter, root.name)
    else:
        node_repr = str(root.name)

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = \
        _build_tree_string(root.left, 2 * curr_index + 1, index, delimiter)
    r_box, r_box_width, r_root_start, r_root_end = \
        _build_tree_string(root.right, 2 * curr_index + 2, index, delimiter)

    # Draw the branch connecting the current root node to the left sub-box
    # Pad the line with whitespaces where necessary
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(' ' * (l_root + 1))
        line1.append('_' * (l_box_width - l_root))
        line2.append(' ' * l_root + '/')
        line2.append(' ' * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root node
    line1.append(node_repr)
    line2.append(' ' * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box
    # Pad the line with whitespaces where necessary
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append('_' * r_root)
        line1.append(' ' * (r_box_width - r_root + 1))
        line2.append(' ' * r_root + '\\')
        line2.append(' ' * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    gap = ' ' * gap_size
    new_box = [''.join(line1), ''.join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
        r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root repr positions
    return new_box, len(new_box[0]), new_root_start, new_root_end


def pre_order(tree):
    """
    使用栈方式前序遍历二叉树

    Parameters
    ----------
    tree: TreeNode
        二叉树根节点

    Returns
    -------
    list of TreeNode:
        二叉树的前序遍历顺序
    """
    result = []
    stack = [tree]
    while stack:
        node = stack.pop()
        if node:
            result.append(node)
            stack.append(node.right)
            stack.append(node.left)
    return result


def mid_order(tree):
    """
    中序遍历二叉树

    Parameters
    ----------
    tree: TreeNode
        二叉树根节点

    Returns
    -------
    list of TreeNode:
        二叉树的中序遍历顺序
    """
    result = []
    stack = []
    node = tree

    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        if stack:
            node = stack.pop()
            result.append(node)
            node = node.right

    return result


def post_order(tree):
    """
    使用栈方式后序遍历二叉树

    Parameters
    ----------
    tree: TreeNode
        要进行后序遍历的（子）树

    Returns
    -------
    list[TreeNode]:
        后序遍历的节点顺序列表
    """
    result = []
    stack = [tree]
    while stack:
        node = stack.pop()
        if node:
            result.append(node)  # This sentence could be replaced
            stack.append(node.left)
            stack.append(node.right)
    return result[::-1]


class TreeNode(object):
    """
    二叉树节点

    Attributes
    ----------
    name: str
        该节点的名称
    dpr: boolean
        是否在该节点上部署 DPR
    solutions: list[Solution]
        该节点上的解集列表
    left: TreeNode
        该节点的左子节点
    right: TreeNode
        该节点的右子节点
    """
    def __init__(self, name, dpr=False, solutions=None, left=None, right=None):
        self.name = name
        self.dpr = dpr
        if not solutions:
            self.solutions = []
        else:
            self.solutions = solutions
        self.left = left
        self.right = right

    def __str__(self):
        return 'Node({})'.format(self.name)

    def pprint(self):
        """
        打印二叉树
        """
        lines = _build_tree_string(self, 0, False, '-')[0]
        print('\n' + '\n'.join((line.rstrip() for line in lines)), end='')

    def __repr__(self):
        return 'Node({})'.format(self.name)

    @property
    def is_leaf(self):
        """
        指示该节点是否是叶子节点（即左右子节点均为空的节点）

        Returns
        -------
        boolean:
            如果是叶子节点返回 True，否则为 False
        """
        return self.left is None and self.right is None
