"""
从数据矩阵中读取异常率，并计算最小/最大异常率。

异常的产生
----------

根据马氏距离和 Minimum Covariace Determinant （最小协方差行列式）计算数据集的异常。
该算法由 ``sklearn.covariance.MinCovDet`` 实现。

数据集格式
^^^^^^^^^^^^

每个数据中心租户的在 $d$ 天内的 $n$ 个时段所产生的数据组成一个 $d \times n$ 的矩阵。::

    [[r11,     r12,     ...,     r1n], -> 第一天的数据
     [r21,     r22,     ...,     r2n], -> 第二天的数据
     ...
     [rd1,     rd2,     ...,     rdn]] -> 第 d 天的数据
     |          |                |
     V          V                V
     第一个时段 第二个时段    第n个时段

异常率的计算
------------

根据公式 $AR_w(s) = \sum_{t=s}^{s+w-1} I(t)/w$，异常率即为在大小为 $w$ 的窗口范围内的平均异常数。

通过不断移动窗口，计算每个窗口内的异常率，最后找出该异常率数组中的最大值和最小值。
"""
import numpy as np
from sklearn.covariance import MinCovDet


def get_anomaly(data_array):
    """
    根据数据矩阵，获取其异常数列表。

    Parameters
    ----------
    data_array : numpy.ndarray
        一个形状为 (d, n) 的矩阵，其中 d 为数据的天数，n 为数据的时段数。表示输入数据。

    Returns
    -------
    list
        一个形状为 (n*d, 1) 的向量，表示整个数据集中有多少个异常点。其中，异常点标记为 1，非异常点标记为0。
    """
    flattened_array = data_array.reshape(-1, 1)
    mcd = MinCovDet()
    mcd.fit(flattened_array)
    support = mcd.support_
    anomaly = []
    for is_not_outline in support:
        if is_not_outline:
            anomaly.append(0)
        else:
            anomaly.append(1)
    return anomaly


def get_anomaly_rate(anomaly_vec, window_size, start_pos):
    """
    AR函数的实现。

    通过遍历 ``anomaly_vec`` 数组，根据窗口大小 ``window_size`` 和起始位置 ``start_pos`` 计算该条件下的异常率。

    Parameters
    ----------
    anomaly_vec : list
        根据 ``get_anomaly`` 函数计算得到的异常数列表。
    window_size : int
        窗口大小
    start_pos : int
        起始位置，范围是 ``[1, len(anomaly_vec)-window_size+1]``. 计算时应注意从 1 开始计算。
        因此数组中的 ``start_pos`` 要减一。

    Returns
    -------
    float
        该窗口和起始位置条件下的异常率。
    """
    return float(sum(anomaly_vec[start_pos-1:start_pos+window_size-1])) / window_size


def get_max_min_anomaly_rate(anomaly_vec, window_size):
    """
    求最大和最小异常率。

    Parameters
    ----------
    anomaly_vec : List
        根据 ``get_anomaly`` 函数计算的到的异常数列表。
    window_size : int
        窗口大小

    Returns
    -------
    tuple of (float, float)
        分别表示最小异常率和最大异常率。
    """
    all_anomaly_rates = []
    for start_pos in range(1, len(anomaly_vec)-window_size+1):
        all_anomaly_rates.append(get_anomaly_rate(anomaly_vec, window_size, start_pos))
    return min(all_anomaly_rates), max(all_anomaly_rates)
