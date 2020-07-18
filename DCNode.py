class DCNode(object):
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
