"""Catalog search over fictional sample records; not an authoritative frequency list."""
import json
import csv
from pathlib import Path

def records(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def search(data, state='', mode='', city=''):
    return [row for row in data if all([
        not state or row['state'].casefold()==state.casefold(),
        not mode or row['mode'].casefold()==mode.casefold(),
        not city or city.casefold() in row['city'].casefold()])]

def configure(sub):
    p=sub.add_parser('search',help='Search sample or sourced local dataset')
    p.add_argument('--data',default=str(Path(__file__).resolve().parents[2]/'samples'/'repeaters.json'))
    p.add_argument('--state',default='');p.add_argument('--mode',default='');p.add_argument('--city',default='')

def run(args):
    return {'records':search(records(args.data),args.state,args.mode,args.city),
            'warning':'All bundled data is fictional; not for radio operation or emergency use.'}

def demo():
    return {'records':search(records(Path(__file__).resolve().parents[2]/'samples'/'repeaters.json')),
            'warning':'Demonstration records only. No real repeater frequencies.'}
