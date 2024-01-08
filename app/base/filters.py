import datetime
import arrow
import mimetypes
import os
from flask import current_app as app

# ############################ Jinja Filters ######

additional_file_types = {
    '.md': 'text/markdown'
}


@app.template_filter('datetime_format')
def datetime_format(date_str, locale=os.environ.get('LOCAL_FR')):
    if not date_str:
        return None
    dt = arrow.get(date_str)

    return dt.format('ddd. DD MMM. YYYY  HH:mm', locale=locale)


@app.template_filter('datetime_format_sm')
def datetime_format_sm(date_str, locale=os.environ.get('LOCAL_FR')):
    if not date_str:
        return None
    dt = arrow.get(date_str)
    return dt.format("DD MMM. YYYY HH:mm", locale=locale)


@app.template_filter('date_format')
def date_format(date_str, locale=os.environ.get('LOCAL_FR')):
    if not date_str:
        return None
    dt = arrow.get(date_str)
    return dt.format("dddd DD MMMM YYYY", locale=locale)


@app.template_filter('date_format_sm')
def date_format_sm(date_str, locale=os.environ.get('LOCAL_FR')):
    if not date_str:
        return None
    dt = arrow.get(date_str)
    return dt.format("DD MMM. YYYY", locale=locale)


@app.template_filter('date_format_xs')
def date_format_xs(date_str, locale=os.environ.get('LOCAL_FR')):
    if not date_str:
        return None
    dt = arrow.get(date_str)
    return dt.format("DD/MM/YY", locale=locale)


@app.template_filter('time_format')
def time_format(date_str, locale=os.environ.get('LOCAL_FR')):
    if not date_str:
        return None
    dt = arrow.get(date_str)
    return dt.format("HH [h] mm [min] ", locale=locale)


@app.template_filter('datetime_humanize')
def datetime_humanize(date_str, locale=os.environ.get('LOCAL_FR')):
    if not date_str:
        return None
    dt = arrow.get(date_str)
    return dt.humanize(locale=locale)


@app.template_filter('file_type')
def file_type(key):
    file_info = os.path.splitext(key)
    file_extension = file_info[1]
    try:
        return mimetypes.types_map[file_extension]
    except KeyError:
        filetype = 'Unknown'
        if file_info[0].startswith('.') and file_extension == '':
            filetype = 'text'

        if file_extension in additional_file_types.keys():
            filetype = additional_file_types[file_extension]

        return filetype