import argparse
import yaml
import codecs
import logging

class ConversionException(Exception):
    pass

class MissingFieldException(ConversionException):
    pass

class DuplicateKeyException(ConversionException):
    pass

def required_fields():
    return {
        "book": [["author", "authors"], "title", "year","publisher"],
        "journal": [["author", "authors"], "title","journal", "year"],
        "conference": [["author", "authors"], "title","booktitle", "year"],
        "collection": [["author", "authors"], "title","booktitle", "year", "publisher"],
        "masters thesis": [["author", "authors"],"title", "school", "year"],
        "phd thesis": [["author", "authors"], "title","school", "year"],
        "tech report": [["author", "authors"], "title","year", "institution", "number"]
        }

def type_identifiers():
    return {
        "book": "@book",
        "journal": "@article",
        "conference": "@inproceedings",
        "collection": "@incollection",
        "masters thesis": "@mastersthesis",
        "phd thesis": "@phdthesis",
        "tech report": "@techreport"
    }

def check_required_fields(item):
    req_fields = required_fields().get(item['type'], [])
    for field in req_fields:
        if isinstance(field, list):
            if not any(option in item for option in field):
                raise MissingFieldException(f"Missing required field: {' or '.join(field)}")
        elif field not in item:
            raise MissingFieldException(f"Missing required field: '{field}'")

def process_item(key, item, out_file):
    logging.info(f"Processing {key}")
    typ = item.get('type')
    if not typ:
        raise MissingFieldException("Missing type")
    out_file.write(f"{type_identifiers().get(typ, 'Unknown type')}{{")
    authors = item.get('authors', [item.get('author')])
    if not authors[0]:
        raise MissingFieldException("Missing author")
    if 'year' not in item:
        raise MissingFieldException("Missing year")
    check_required_fields(item)
    logging.info(f"Writing: {key}")
    out_file.write(f"{key} ,\n  author = {{{' and '.join(authors)}}},\n")
    for field in ['type', 'author', 'authors']:
        item.pop(field, None)
    for k, v in item.items():
        out_file.write(f"  {k} = {{{' and '.join(v) if isinstance(v, list) else v}}},\n")
    out_file.write("}\n\n")

def main():
    parser = argparse.ArgumentParser(description='Translate bibliography from YAML to BIB.')
    parser.add_argument('input', help='Input YAML file')
    parser.add_argument('output', nargs='?', help='Output BIB file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    in_file_name = args.input
    out_file_name = args.output or f"{in_file_name.rsplit('/', 1)[-1].rsplit('.', 1)[0]}.bib"
    logging.info(f"Input = {in_file_name}\nOutput = {out_file_name}")

    with codecs.open(in_file_name, encoding='utf-8', mode='r') as in_file, \
        codecs.open(out_file_name, encoding='utf-8', mode='w') as out_file:
        data = yaml.load(in_file, Loader=yaml.SafeLoader)
        items = {}
        for key, item in data.items():
            try:
                if key in items:
                    raise DuplicateKeyException(f"Duplicate key: {key}")
                items[key] = item
                process_item(key, item, out_file)
            except ConversionException as e:
                logging.error(f"*** Error while processing an item: {e}")

if __name__ == "__main__":
    main()

