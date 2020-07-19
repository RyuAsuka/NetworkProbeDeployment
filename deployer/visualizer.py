"""
树的可视化。
要求：
能够正确地画出二叉树
能够根据节点的不同属性给节点上不同的颜色
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from deployer.BinaryTree import TreeNode
from deployer.BinaryTree import mid_order


def get_left_width(root):
    """
    获得根左边宽度

    Parameters
    ----------
    root: TreeNode
        树的根节点

    Returns
    -------
    int:
        根左边的宽度值
    """
    return get_width(root.left)


def get_right_width(root):
    """
    获取根右边的宽度

    Parameters
    ----------
    root: TreeNode
        树的根节点

    Returns
    -------
    int:
        根右边的宽度值
    """
    return get_width(root.right)


def get_width(root):
    """
    获得树的宽度

    Parameters
    ----------
    root: TreeNode
        树的根节点

    Returns
    -------
    int:
        宽度值
    """
    if not root:
        return 0
    return get_width(root.left) + 1 + get_width(root.right)


def get_height(root):
    """
    获得树的高度

    Parameters
    ----------
    root: TreeNode
        树的根节点

    Returns
    -------
    int:
        树的高度值
    """
    if not root:
        return 0
    return max(get_height(root.left), get_height(root.right))


d_hor = 4  # 节点水平距离
d_vec = 8  # 节点垂直距离
radius = 1  # 节点的半径


def get_width_and_height(root):
    """
    调用 get_width 函数和 get_height 函数获得树的宽度和高度

    Parameters
    ----------
    root: TreeNode
        树的根节点

    Returns
    -------
    tuple(int, int):
        返回树的宽度和高度
    """
    w = get_width(root)
    h = get_height(root)
    return w, h


def draw_a_node(x, y, val, ax, color):
    """
    画一个节点

    Parameters
    ----------
    x: int
        节点的 x 坐标
    y: int
        节点的 y 坐标
    val: str
        节点的名称
    ax: matplotlib.pyplot.Axes
        Axes 画布
    color: str
        颜色
    """
    c_node = Circle((x, y), radius=radius, color=color)
    ax.add_patch(c_node)
    plt.text(x, y, f'{val}', ha='center', va='bottom', fontsize=11)


def draw_an_edge(x1, x2, y1, y2, r=radius):
    """
    绘制一条边

    Parameters
    ----------
    x1: int
        第一个点的第一个坐标
    x2: int
        第一个点的第二个坐标
    y1: int
        第二个点的第一个坐标
    y2: int
        第二个点的第二个坐标
    r: int
        半径
    """
    x = (x1, x2)
    y = (y1, y2)
    plt.plot(x, y, 'k-')


def create_win(root):
    """
    创建窗口

    Parameters
    ----------
    root: 树的根节点

    Returns
    -------
    tuple(`~matplotlib.figure.Figure`, `~matplotlib.pyplot.Axes`, int, int):
        返回 figure 对象, Axes 对象，以及第一个点的坐标
    """
    width, height = get_width_and_height(root)
    width = (width + 1) * d_hor
    height = (height + 1) * d_vec
    lim_value = max(width, height)
    # fig = plt.figure(figsize=(11, 9))
    # ax = fig.add_subplot(111)
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.tight_layout()
    plt.xlim(-lim_value, lim_value)
    plt.ylim(-lim_value, lim_value)
    plt.xticks([])
    plt.yticks([])

    x = (get_left_width(root) + 1) * d_hor
    y = height - d_vec
    return fig, ax, x, y


def draw_tree_by_midorder(root, x, y, ax):
    """
    通过中序遍历打印二叉树

    Parameters
    ----------
    root: TreeNode
        树的根节点
    x: int
        第一个点的 x 坐标
    y: int
        第一个点的 y 坐标
    ax: `~matplotlib.pyplot.Axes`
        Axes 对象
    """
    if not root:
        return
    if root.dpr:
        draw_a_node(x, y, root.name, ax, color='green')
    else:
        draw_a_node(x, y, root.name, ax, color='yellow')
    lx = rx = 0
    ly = ry = y - d_vec
    if root.left:
        lx = x - d_hor * (get_right_width(root.left) + 1)
        draw_an_edge(x, lx, y, ly, radius)
    if root.right:
        rx = x + d_hor * (get_right_width(root.right) + 1)
        draw_an_edge(x, rx, y, ry, radius)
    draw_tree_by_midorder(root.left, lx, ly, ax)
    draw_tree_by_midorder(root.right, rx, ry, ax)
