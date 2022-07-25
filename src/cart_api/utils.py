import codecs
import datetime
import os
import re
from decimal import Decimal
from json import dumps
from urllib.parse import (parse_qsl, ParseResult, unquote, urlencode, urlparse)

import pandas as pd
import pytz
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.formats import number_format
from django.utils.translation import gettext_lazy as _
from django_models.utils import remove_special_characters
from unipath import Path

ALLOWED_COUNTRY_PREFIXES = ('55',)
BASE_DIR = Path(__file__).ancestor(3)


def calculate_duration(start_time, end_time, verbose=True):
    run_time = end_time - start_time
    minutes = 0
    seconds = run_time
    if run_time > 60:
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)

    if verbose:
        duration = f"{seconds:.2f} secs"
        if minutes:
            duration = f"{round(minutes)} min and {duration}"
    else:
        duration = (
            '{minutes}" '
            '{duration}'
            "'"
        ).format(minutes=round(minutes), seconds=int(seconds))
    return duration


def calculate_percentage(total, partial):
    return round((partial / total) * 100, 1)


def remove_cellphone_prefix(cellphone):
    for prefix in ALLOWED_COUNTRY_PREFIXES:
        cellphone = cellphone.replace('+', '')
        if cellphone.startswith(prefix):
            cellphone = cellphone[2:]
    return cellphone


def add_cellphone_prefix(cellphone):
    if not any(cellphone.startswith(prefix) for prefix in ALLOWED_COUNTRY_PREFIXES):
        cellphone = f'55{cellphone}'
    return cellphone


def remove_html(raw_html):
    pattern = re.compile('<.*?>')
    return re.sub(pattern, '', raw_html)


def clean_filename(filename):
    fragment_filename = filename.split('.')
    name = '_'.join(remove_special_characters(
        ''.join(fragment_filename[:-1])).split()).lower()
    ext = fragment_filename[-1]
    return '{}.{}'.format(name, ext)


def get_version():
    current_version = ''
    changes = os.path.join(BASE_DIR, "CHANGES.rst")
    pattern = r'^(?P<version>[0-9]+.[0-9]+(.[0-9]+)?)'
    with codecs.open(changes, encoding='utf-8') as changes:
        for line in changes:
            match = re.match(pattern, line)
            if match:
                current_version = match.group("version")
                break
    return current_version or '0.1.0'


def upload_to(instance, filename, document_type='image'):
    folder = type(instance).__name__.lower()

    root_path = settings.MODEL_STORAGE_ROOT.get(
        folder, '{}s/'.format(document_type))
    filename = clean_filename(filename)

    return os.path.join(*[
        root_path,
        folder,
        str(instance.id),
        filename
    ])


def is_email(text):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return bool(re.search(pattern, text))


def get_verbose_timedelta(days):
    years = 0
    months = int(days / 30)
    if months > 12:
        years = int(months / 12)
        months = months - (years * 12)
    return _("{} years and {} months").format(years, months)


def clean_url(url):
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    parsed_get_args = dict(parse_qsl(get_args))
    # Merging URL arguments dict with new params
    parsed_get_args.pop('page', '')

    parsed_get_args.update(
        {k: dumps(v) for k, v in parsed_get_args.items()
         if isinstance(v, (bool, dict))}
    )

    # Converting URL argument to proper query string
    encoded_get_args = urlencode(parsed_get_args, doseq=True)
    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()

    return new_url


def slugify(word):
    return '_'.join(remove_special_characters(''.join(word)).split()).lower()


def generate_activation_code(length=6):
    allowed = [str(x) for x in range(10)]
    return get_random_string(length=length, allowed_chars=allowed)


def phone_mask(item, mask="({}) {}-{}"):
    """ return (00) 00000-0000 or (00) 0000-0000  """
    if item and len(item) >= 11:
        return mask.format(
            item[0:2],
            item[2:7],
            item[7:11]
        )
    elif item:
        return mask.format(
            item[0:2],
            item[2:6],
            item[6:10]
        )


def cpf_mask(item, mask="{}.{}.{}-{}"):
    """ return 000.000.000-00 """
    if item:
        return mask.format(
            item[0:3],
            item[3:6],
            item[6:9],
            item[9:11]
        )
    else:
        return None


def rg_mask(item, mask="{}.{}.{}-{}", other_mask="{}.{}.{}"):
    """
    return 00.000.000-0 or 0.000.000
    in this case I was have to create another mask to work with in both objects
    """
    if item and len(item) >= 8:
        return mask.format(
            item[0:2],
            item[2:5],
            item[5:8],
            item[8:9]
        )
    else:
        return other_mask.format(
            item[0:1],
            item[1:4],
            item[4:7]
        )


def cnpj_mask(item, mask="{}.{}.{}/{}-{}"):
    """ return 00.000.000/0000-00 """
    if item:
        return mask.format(
            item[0:2],
            item[2:5],
            item[5:8],
            item[8:12],
            item[12:14]
        )
    else:
        return None


def cep_mask(item, mask="{}-{}"):
    """ Return 00000-000 """
    if item:
        return mask.format(
            item[0:5],
            item[5:8]
        )
    else:
        return None


def value_to_cents(value):
    return str(int(value * 100))


def cost_format(cost):
    if cost == 'N/A' or not cost:
        return cost
    return number_format(round(Decimal(cost), 2))


def time_in_range(hour_block, timestamp):
    """Return true if x is in the range [start, end]"""
    if hour_block == '20+':
        _start = 20
        _end = 0
    else:
        _start, _end = hour_block.split('-')

    start = datetime.time(int(_start), 0, 0)
    end = datetime.time(int(_end), 0, 0)
    if start <= end:
        return start <= timestamp <= end
    else:
        return start <= timestamp or timestamp <= end


def clean_fields(data, extra_fields=[], code_field=False):
    to_remove = ['id', 'created_at', 'updated_at'] + extra_fields
    if not code_field:
        to_remove.append('code')

    for key in to_remove:
        data.pop(key, '')
    return data


def create_new_dict_from_keys(data_dict, keys):
    return {key: data_dict.get(key, '') for key in keys}


def get_name_from_slug(slug, delimiter='_'):
    return ' '.join([word.title() for word in slug.split(delimiter)])


def dataframe_is_empty_check(df):
    if isinstance(df, pd.DataFrame):
        return df.empty
    else:
        return True


def clean_voltages_zero(df: pd.DataFrame, cutoff: int = 1) -> pd.DataFrame:
    # TODO: Remove as soon we have a common attr

    voltage_keys_added = []
    for col in ["voltage_phase_1", "voltage_phase_2", "voltage_phase_3"]:
        if col in df.keys():
            voltage_keys_added.append(col)

    if voltage_keys_added:
        mask = (
                (df[voltage_keys_added[0]] < cutoff)
                & (df[voltage_keys_added[1]] < cutoff)
                & (df[voltage_keys_added[2]] < cutoff)
        )
        df = df[~mask]
    return df


def get_all_timezones_choices():
    return tuple((tz, tz) for tz in pytz.all_timezones)
