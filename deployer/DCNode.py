# coding:utf-8
"""
数据中心节点类
"""

class DCNode(object):
    """
    定义数据中心节点类。包含节点的名称，最小/最大异常率。其中，最小异常率 <= 最大异常率。

    Attributes
    ----------
    name: str
        该节点的名称
    ar_min: float
        范围为 [0, 1]，该节点的最小异常率
    ar_max: float
        范围为 [0, 1]，该节点的最大异常率
    """
    def __init__(self, name, ar_min=0, ar_max=0):
        if ar_min > ar_max:
            raise ValueError('AR_min must be <= AR_max')
        self.name = name
        self.ar_min = ar_min
        self.ar_max = ar_max

    def __str__(self):
        return f'{self.name}: [{self.ar_min:0.2f}, {self.ar_max:0.2f}]'

    def __repr__(self):
        return f'{self.name}: [{self.ar_min:0.2f}, {self.ar_max:0.2f}]'
