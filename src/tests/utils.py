import json
import random
import numpy
import pandas as pd

from apps.core.fields import CompressedBinaryField
from faker import Faker


fake = Faker(locale='pt_BR')


def random_json():
    value = json.dumps({'asdf': random.random()}).encode('utf-8')
    return CompressedBinaryField.compress(value)


def random_dataframe():
    value = pd.DataFrame(numpy.array([[0, 1, random.randint(0, 100)],
                         [3, random.randint(0, 100), 4, 5],
                         [random.randint(0, 100), 7, 8]]))
    value = json.dumps(value).encode('utf-8')
    return value
