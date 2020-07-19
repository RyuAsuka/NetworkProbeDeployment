from deployer.BinaryTree import TreeNode
from deployer.BinaryTree import mid_order


def test_mid_order():
    tree = TreeNode('1')
    tree.left = TreeNode('2')
    tree.right = TreeNode('3')
    tree.left.left = TreeNode('4')
    tree.left.right = TreeNode('5')
    tree.right.left = TreeNode('6')
    assert str(mid_order(tree)) == '[Node(4), Node(2), Node(5), Node(1), Node(6), Node(3)]'
