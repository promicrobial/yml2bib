import argparse  # Module for parsing command-line arguments
import yaml      # Module for reading and writing YAML files
import codecs    # Module for encoding and decoding data
import logging    # Module for logging messages

# Custom exception for conversion errors
class ConversionException(Exception):
    pass

# Exception for missing required fields
class MissingFieldException(ConversionException):
    pass

# Exception for duplicate keys in the input data
class DuplicateKeyException(ConversionException):
    pass

# Function to load configuration from a YAML file
def load_config(config_file):
    """
    Load configuration from a YAML file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Configuration data loaded from the file.
    """
    with open(config_file, 'r') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    return config

# Function to check if all required fields are present in an item
def check_required_fields(item, fields):
    """
    Check if all required fields are present in an item.

    Args:
        item (dict): Bibliography item to check.
        fields (dict): Dictionary of fields for each type.

    Raises:
        MissingFieldException: If a required field is missing.
    """
    req_fields = fields.get(item['type'], {}).get('required', [])
    for field in req_fields:
        if isinstance(field, list):
            # Check if at least one of the options in the list is present
            if not any(option in item for option in field):
                raise MissingFieldException(f"Missing required field: {' or '.join(field)}")
        elif field not in item:
            raise MissingFieldException(f"Missing required field: '{field}'")

# Function to process each bibliography item and write it to the output file
def process_item(key, item, out_file, fields):
    """
    Process a bibliography item and write it to the output file.

    Args:
        key (str): Key of the bibliography item.
        item (dict): Bibliography item data.
        out_file (file object): Output file to write to.
        fields (dict): Dictionary of fields for each type.
    """
    logging.info(f"Processing {key}")  # Log the processing of the item
    typ = item.get('type')  # Get the type of the bibliography entry
    if not typ:
        raise MissingFieldException("Missing type")  # Raise an error if type is missing
    out_file.write(f"{typ}{{")  # Write the BibTeX type

    # Get authors, defaulting to a list containing the single author if 'authors' is not present
    authors = item.get('authors', [item.get('author')])
    if not authors[0]:
        raise MissingFieldException("Missing author")  # Raise an error if no author is found
    if 'year' not in item:
        raise MissingFieldException("Missing year")  # Raise an error if year is missing

    check_required_fields(item, fields)  # Check for other required fields
    logging.info(f"Writing: {key}")  # Log the writing of the item
    out_file.write(f"{key} ,\n  author = {{{' and '.join(authors)}}},\n")  # Write the key and authors

    # Remove certain fields from the item before writing the rest
    for field in ['type', 'author', 'authors']:
        item.pop(field, None)
    
    # Write remaining fields to the output file
    for k, v in item.items():
        out_file.write(f"  {k} = {{{' and '.join(v) if isinstance(v, list) else v}}},\n")

    # Write optional fields if they are present
    optional = fields.get(typ, {}).get('optional', [])
    for field in optional:
        if field in item:
            out_file.write(f"  {field} = {{{item[field]}}},\n")

    out_file.write("}\n\n")  # Close the BibTeX entry

def main():
    """
    Main function to handle command-line arguments and file processing.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Translate bibliography from YAML to BIB.')
    parser.add_argument('input', help='Input YAML file')  # Input YAML file argument
    parser.add_argument('output', nargs='?', help='Output BIB file')  # Optional output file argument
    parser.add_argument('-c', '--config', default='assets/bibtex-doc-types.yml', help='Configuration YAML file')  # Config file argument
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')  # Verbose flag
    args = parser.parse_args()  # Parse the arguments

    # Set logging level based on verbosity
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    
    # Load configuration from the specified config file
    config = load_config(args.config)
    fields = config['fields']

    # Assign the input file name from the command-line arguments
    in_file_name = args.input

    # Determine the output file name
    # If an output file name is provided, use it; otherwise, generate a default name
    # The default name is derived from the input file name by:
    # 1. Splitting the input file name on '/' to get the last part (the file name)
    # 2. Splitting that last part on '.' to remove the file extension
    # 3. Appending '.bib' to create the output file name
    out_file_name = args.output or f"{in_file_name.rsplit('/', 1)[-1].rsplit('.', 1)[0]}.bib"

    # Log the input and output file names for debugging purposes
    logging.info(f"Input = {in_file_name}\nOutput = {out_file_name}")

    # Open the input file for reading and the output file for writing
    # Using 'codecs.open' to ensure proper handling of UTF-8 encoding
    with codecs.open(in_file_name, encoding='utf-8', mode='r') as in_file, \
         codecs.open(out_file_name, encoding='utf-8', mode='w') as out_file:
        # Load the YAML data from the input file
        # Using 'yaml.load' with 'Loader=yaml.SafeLoader' for safe parsing of YAML
        data = yaml.load(in_file, Loader=yaml.SafeLoader)

        # Initialize an empty dictionary to store items from the YAML data
        items = {}

        # Iterate over each key-value pair in the loaded YAML data
        for key, item in data.items():
            try:
                # Check for duplicate keys in the items dictionary
                if key in items:
                    raise DuplicateKeyException(f"Duplicate key: {key}")  # Raise an error if a duplicate key is found
                
                # Store the item in the items dictionary using the key
                items[key] = item
                
                # Process the item and write it to the output file
                process_item(key, item, out_file, fields)
            
            # Catch any conversion-related exceptions that occur during processing
            except ConversionException as e:
                # Log an error message indicating the issue with processing the item
                logging.error(f"*** Error while processing an item: {e}")

    # Check if the script is being run directly (not imported as a module)
    if __name__ == "__main__":
        main()  # Call the main function to start the script
