### Usage Statement

The `yml2bib.py` script translates bibliography data from YAML format to BibTeX format. It reads an input YAML file, processes each bibliography entry according to the specified configuration, and writes the output to a BibTeX file.

#### How to Run the Script

1. **Ensure Dependencies are Installed**:
   Make sure you have Python installed and the necessary dependencies (`argparse`, `yaml`, `codecs`, and `logging` modules) are available.

2. **Prepare the Configuration File**:
   Ensure you have a `assets/bibtex-doc-types.yml` file with the required and optional fields for each BibTeX type.

3. **Run the Script**:
   Execute the following command in your terminal to run the script:
   ```sh
   python yml2bib.py input.yaml output.bib
   ```

#### Command-Line Arguments

- **`input`**: The input YAML file containing the bibliography data.
- **`output`** (optional): The output BibTeX file. If not provided, the script will generate a default name based on the input file name.
- **`-c`, `--config`**: The configuration YAML file specifying the required and optional fields for each BibTeX type. Default is `assets/bibtex-doc-types.yml`.
- **`-v`, `--verbose`**: Enable verbose output for detailed logging.

#### Example Usage

```sh
python yml2bib.py bibliography.yaml bibliography.bib -c assets/bibtex-doc-types.yml -v
```

This command will:
- Read the bibliography data from `bibliography.yaml`.
- Use the configuration specified in `assets/bibtex-doc-types.yml`.
- Write the output to `bibliography.bib`.
- Enable verbose logging to provide detailed information about the processing.

#### Default Configuration File

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

#### Expected Output

The script will generate a BibTeX file with entries formatted according to the specified configuration. For example, an entry in the input YAML file like this:

```yaml
example_key:
  type: "@book"
  authors: ["John Doe"]
  title: "Example Book"
  year: 2020
  publisher: "Example Publisher"
```

Will be converted to the following BibTeX entry in the output file:

```bibtex
@book{example_key ,
  author = {John Doe},
  title = {Example Book},
  year = {2020},
  publisher = {Example Publisher},
}
```
