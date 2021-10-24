#!/usr/bin/env python3
from urllib import request
import datetime
import filecmp
import os
import sys
import json

FORCE = '-f' in sys.argv
if FORCE:
    sys.argv.remove('-f')
if len(sys.argv) < 3:
    print('Usage:  cd PATH && {} domain.com calId [calId]'.format(sys.argv[0]))
    exit(0)
DOMAIN = sys.argv[1]


def nextcloud_ical_url(params: dict = {}):
    params['start'] = relative_month(-1)  # start of last month
    params['end'] = relative_month(4) - 1  # end of +3 month
    return 'https://{}/remote.php/dav/public-calendars/{}?export&{}'.format(
        DOMAIN, CAL_ID, '&'.join(k + '=' + str(v) for k, v in params.items()))


# def strip_cal_username(txt: str):
#     return txt[:txt.rindex(' (')] + txt[txt.rindex(')') + 1:]  # keep newline


def relative_month(month_diff):
    today = datetime.date.today()
    m = today.month + month_diff - 1
    dy, m = m // 12, (m % 12) + 1
    return int(datetime.date(today.year + dy, m, 1).strftime('%s'))


def load_ical(dest: str):
    tmp_file = 'tmp_' + CAL_ID
    request.urlretrieve(nextcloud_ical_url({
        'componentType': 'VEVENT',
    }), tmp_file)
    with open(tmp_file) as fp:
        data = ''
        for _ in range(10):  # calname should be in the first 10 lines
            line = fp.readline()
            if line.startswith('X-WR-CALNAME:'):
                # if line.rstrip().endswith(')'):
                #     data += strip_cal_username(line)
                data += 'X-WR-CALNAME:OWBA' + line[-1:]  # keep newline
                break
            data += line
        data += fp.read()
    with open(tmp_file, 'w') as fpw:
        fpw.write(data)

    # filecmp.clear_cache()
    needs_update = FORCE or not os.path.isfile(dest) or \
        not filecmp.cmp(dest, tmp_file, shallow=False)
    if needs_update:
        os.replace(tmp_file, dest)
    else:
        os.remove(tmp_file)
    return needs_update


def load_jcal(dest: str):
    request.urlretrieve(nextcloud_ical_url({
        'accept': 'jcal',
        'expand': 1,
    }), dest)

    with open(dest) as fp:
        obj = json.load(fp)

    for x in obj[1]:
        if x[0] == 'x-wr-calname':
            # if x[-1].endswith(')'):
            #     x[-1] = strip_cal_username(x[-1])
            x[-1] = 'OWBA'
            with open(dest, 'w') as fpw:
                json.dump(obj, fpw)
            break

    return obj


def parse_jcal(jcal: list, dest: str):
    KEY_MAP = {
        # 'uid': 'groupId',
        'url': 'link',
        'summary': 'title',
        'dtstart': 'start',
        'dtend': 'end',
        'location': 'place',
        'description': 'desc',
        'color': 'color',
        # 'categories': 'tags',
    }
    arr = []
    for event in jcal[2]:
        if event[0] != 'vevent':
            continue
        obj = {}
        for attr in event[1]:
            key = KEY_MAP.get(attr[0])
            if key:
                obj[key] = attr[3]
        arr.append(obj)
    with open(dest, 'w') as fpw:
        json.dump(arr, fpw)


for CAL_ID in sys.argv[2:]:
    if load_ical(CAL_ID + '.ics'):
        jcal = load_jcal(CAL_ID + '.jcal')
        parse_jcal(jcal, CAL_ID + '.json')
