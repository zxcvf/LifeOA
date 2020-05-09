import random
import string

"""
保存一些比较杂的方法的工厂
"""


def get_random_string(digit):
    return ''.join(random.sample(string.ascii_letters + string.digits, digit))
