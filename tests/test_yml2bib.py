import unittest
from io import StringIO
from yml2bib import load_config, check_required_fields, process_item, ConversionException, MissingFieldException

class TestConvertBib(unittest.TestCase):

    def setUp(self):
        # Sample configuration data
        self.config_data = {
            'fields': {
                '@book': {
                    'required': [["author", "authors"], "title", "year", "publisher"],
                    'optional': ["volume", "number", "note"]
                },
                '@article': {
                    'required': [["author", "authors"], "title", "journal", "year"],
                    'optional': ["volume", "number", "pages", "note"]
                }
            }
        }
        # Sample bibliography item
        self.sample_item = {
            'type': '@book',
            'authors': ['John Doe'],
            'title': 'Example Book',
            'year': 2020,
            'publisher': 'Example Publisher'
        }
        # Sample incomplete item
        self.incomplete_item = {
            'type': '@book',
            'title': 'Example Book',
            'year': 2020
        }

    def test_load_config(self):
        # Test loading configuration from a file
        config = load_config('assets/bibtex-doc-types.yml')
        self.assertIn('@book', config['fields'])
        self.assertIn('required', config['fields']['@book'])
        self.assertIn('optional', config['fields']['@book'])

    def test_check_required_fields(self):
        # Test checking required fields
        fields = self.config_data['fields']
        try:
            check_required_fields(self.sample_item, fields)
        except MissingFieldException:
            self.fail("check_required_fields() raised MissingFieldException unexpectedly!")

        with self.assertRaises(MissingFieldException):
            check_required_fields(self.incomplete_item, fields)

    def test_process_item(self):
        # Test processing a bibliography item
        fields = self.config_data['fields']
        out_file = StringIO()
        try:
            process_item('example_key', self.sample_item, out_file, fields)
            output = out_file.getvalue()
            self.assertIn('@book{example_key ,', output)
            self.assertIn('author = {John Doe}', output)
        except ConversionException:
            self.fail("process_item() raised ConversionException unexpectedly!")

if __name__ == '__main__':
    unittest.main()
