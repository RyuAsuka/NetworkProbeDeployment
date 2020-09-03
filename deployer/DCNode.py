# coding:utf-8
"""
数据中心节点类
"""


class DCNode(object):
    """
    定义数据中心节点类。包含节点的名称，最小/最大异常率。其中，最小异常率 <= 最大异常率。

    Parameters
    ----------
    name : str
        节点的名称。
    ar_min : float, default 0
        节点的最小异常率。
    ar_max : float, default 0
        节点的最大异常率。

    Attributes
    ----------
    name: str
        该节点的名称。
    ar_min: float
        范围为 [0, 1]，该节点的最小异常率。
    ar_max: float
        范围为 [0, 1]，该节点的最大异常率。

    Raises
    ------
    ValueError : 如果输入不合法则抛出 ValueError 异常。
    """
    def __init__(self, name, ip, ar_min=0, ar_max=0):
        if ar_min < 0 or ar_min > 1 or ar_max < 0 or ar_max > 1:
            raise ValueError('Invalid ar_min and ar_max value! It should between [0, 1].')
        if ar_min > ar_max:
            raise ValueError('AR_min must be <= AR_max')
        self.name = name
        self.ip = ip
        self.ar_min = ar_min
        self.ar_max = ar_max

    def __str__(self):
        return f'{self.name}: [{self.ar_min:0.2f}, {self.ar_max:0.2f}]'

    def __repr__(self):
        return f'{self.name}: [{self.ar_min:0.2f}, {self.ar_max:0.2f}]'
