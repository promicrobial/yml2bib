### Usage Statement

The `test_yml2bib.py` script is designed to test the functionality of the `yml2bib.py` script, which translates bibliography data from YAML format to BibTeX format. The tests ensure that the configuration is loaded correctly, required fields are checked properly, and bibliography items are processed as expected.

```sh
python -m unittest tests/test_yml2bib.py
```

#### How to Run the Tests

1. **Ensure Dependencies are Installed**:
   Make sure you have Python installed and the necessary dependencies (`unittest` and `yaml` modules) are available.

2. **Prepare the Configuration File**:
   Ensure you have a `bibtex-doc-types.yaml` file with the required and optional fields for each BibTeX type.

3. **Run the Test Script**:
   Execute the following command in your terminal to run the tests:
   ```sh
   python -m unittest test_convert_bib.py
   ```

#### Example Configuration File

```yaml
fields:
  "@book":
    required: [["author", "authors"], "title", "year", "publisher"]
    optional: ["volume", "number", "note"]
  "@article":
    required: [["author", "authors"], "title", "journal", "year"]
    optional: ["volume", "number", "pages", "note"]
  # Add other types as needed
```

#### Test Cases

- **`test_load_config`**: Verifies that the configuration is loaded correctly from the `config.yaml` file.
- **`test_check_required_fields`**: Ensures that the required fields for each bibliography item are checked properly.
- **`test_process_item`**: Confirms that bibliography items are processed correctly and the expected BibTeX output is generated.

#### Expected Output

When you run the test script, you should see output indicating the results of the tests. For example:

```
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

This output indicates that all tests passed successfully. If any tests fail, the output will provide details about the failures.
