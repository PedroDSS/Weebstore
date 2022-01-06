from string import ascii_lowercase, ascii_uppercase, digits
from random import choice


def random_key(length, chars=None):
    """
        Generate a key alphanumeric (A-Za-z0-9) of size length.

        :param length integer: The key length to generate
        :param chars str: The list of potential character to use for the result
        :rtype: str
        :return: The random key
    """

    key = ''
    if chars is None:
        chars = ascii_lowercase + ascii_uppercase + digits
    for i in range(length):
        key += choice(chars)
    return key
