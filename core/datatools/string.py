import string
import random
from itertools import chain


def random_string(length: int=5) -> str:
    return ''.join(random.choices(list(chain(string.ascii_letters, string.digits)), k=length))
