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
    e=sub.add_parser('export-csv',help='Export filtered catalog to CSV (spreadsheet-safe)')
    e.add_argument('--data', default=str(Path(__file__).resolve().parents[2]/'samples'/'repeaters.json'))
    e.add_argument('--output', required=True);e.add_argument('--state', default='');e.add_argument('--mode', default='');e.add_argument('--city', default='')
    v=sub.add_parser('validate',help='Detect duplicate records and invalid coordinates')
    v.add_argument('--data',default=str(Path(__file__).resolve().parents[2]/'samples'/'repeaters.json'))

def run(args):
    matching = search(records(args.data), args.state, args.mode, args.city)
    if args.command == 'export-csv':
        return export_csv(matching, args.output)
    if args.command == 'validate':
        return validate_catalog(records(args.data))
    return {'records':matching, 'warning':'All bundled data is fictional; not for radio operation or emergency use.'}

def demo():
    return {'records':search(records(Path(__file__).resolve().parents[2]/'samples'/'repeaters.json')),
            'warning':'Demonstration records only. No real repeater frequencies.'}

EXPORT_FIELDS = ('id','city','state','mode','frequency_mhz','verified','source')

def export_csv(data, destination):
    """Export catalog records safely for spreadsheet review.

    Formula-prefixed text is escaped to mitigate spreadsheet formula injection.
    """
    def safe(value):
        if value is None:
            return ''
        if isinstance(value, bool):
            return str(value).lower()
        text = str(value)
        if text.lstrip().startswith(('=', '+', '-', '@')) or text.startswith(('\t', '\r', '\n')):
            return "'" + text
        return text
    path = Path(destination)
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=EXPORT_FIELDS, extrasaction='ignore')
        writer.writeheader()
        for record in data:
            writer.writerow({k: safe(record.get(k)) for k in EXPORT_FIELDS})
    return {'exported': len(data), 'output': str(path),
            'warning': 'Check dataset provenance and radio regulations before operational use.'}


def validate_catalog(data):
    """Catalog consistency checks; does not validate frequencies or authorization."""
    from math import isfinite
    seen=set(); issues=[]
    for row_no,row in enumerate(data,1):
        key=tuple(str(row.get(k,'')).casefold() for k in ('state','city','mode','frequency_mhz'))
        if key in seen: issues.append({'row':row_no,'issue':'duplicate-repeater-record'})
        seen.add(key)
        for field,minimum,maximum in (('latitude',-90,90),('longitude',-180,180)):
            if row.get(field) is None: continue
            try:
                v=float(row[field])
                if not isfinite(v) or not minimum<=v<=maximum: raise ValueError
            except (ValueError,TypeError):
                issues.append({'row':row_no,'issue':'invalid-'+field})
    return {'records':len(data),'valid':not issues,'problems':issues,
            'warning':'Internal checks are not proof that source data is accurate or legally usable.'}
