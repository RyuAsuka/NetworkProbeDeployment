"""
数据中心网络模拟生成器

生成
----

一个文件，文件名为 {n}tenants.txt，n 为数据中心中主机的总数

文件格式
--------

假设数据中心网络如论文图 6 所示。

.. image:: /imgs/fig6.png

如图所示，假设数据中心中包含 3 组，每组数量分别是 7 台、6 台和 7 台主机。

每组数据包含 m + 1 行数据，第一个数据是该组中的主机数量 m，

接下来的 m 行数据，每行包含 3 个数据，用逗号隔开。

第 1 个数据为主机的名称（编号），要求即使是不同组的主机，也使用连续编号。

第 2 个数据为主机的最小异常率 ``ar_min``，范围为 [0, 1]

第 3 个数据为主机的最大异常率 ``ar_max``，范围为 [0, 1]，且必须 >= 最小异常率。

::

    例如：有 4 台主机分 2 组，它们的编号分别是 1，2，3，4
    那么，文件中存储它们的方式为
    2
    1, ar_min1, ar_max1
    2, ar_min2, ar_max2
    2
    3, ar_min3, ar_max3
    4, ar_min4, ar_max4


"""
import random


OUTPUT_DIR = '../test'


def data_center_network_generator(n_groups, m_hosts, random_alarm_rate=False):
    """
    生成数据中心网络的描述文件

    Parameters
    ----------
    n_groups : int
        数据中心网络的组数
    m_hosts : list of int
        每组中数据中心网络的个数
    random_alarm_rate : bool
        是否随机生成异常率，若为 False，则所有的主机异常率为 0.0.
    """
    with open(f'{OUTPUT_DIR}/{sum(m_hosts)}tenants.txt', 'w+') as output_file:
        host_name = 1
        for group in range(n_groups):
            output_file.write(f"{m_hosts[group]}")
            output_file.write('\n')
            for host_num in range(m_hosts[group]):
                if random_alarm_rate:
                    ar_min, ar_max = _random_generate_alarm_rate()
                else:
                    ar_min, ar_max = 0.0, 0.0
                output_file.write(f"{host_name},{ar_min:0.2f},{ar_max:0.2f}\n")
                host_name += 1


def _random_generate_alarm_rate():
    """
    生成随机的 ``ar_min`` 和 ``ar_max``

    Returns
    -------
    tuple of (float, float):
        生成的 ``ar_min`` 和 ``ar_max``
    """
    ar_min = random.random()
    ar_max = random.random()
    while ar_max < ar_min:
        ar_max = random.random()
    return ar_min, ar_max
