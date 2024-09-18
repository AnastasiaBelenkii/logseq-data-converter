from pathlib import Path
from lark import Lark
from lark.visitors import Transformer, merge_transformers
from pprint import pprint
import sys

__dir__ = Path(__file__).parent


class LogseqTransformer(Transformer):

    def start(self, children):
        return children

    def block(self, children):
        return {"type": "block", "content": children}

    def firstline(self, children):
        return {
            "type": "firstline",
            "content": children[1] if len(children) > 1 else ""
        }

    def property(self, children):
        return {
            "type": "property",
            "key": str(children[1]),
            "value": str(children[3])
        }

    def MARKDOWN_TEXT(self, token):
        return str(token)


class RecfileTransformer(Transformer):

    def start(self, children):
        return children

    def recfile_record(self, children):
        return {"type": "record", "content": children}

    def property(self, children):
        return {
            "type": "property",
            "key": str(children[0]),
            "value": str(children[2])
        }


def logseq_to_intermediate(parsed_tree):
    return LogseqTransformer().transform(parsed_tree)


def recfile_to_intermediate(parsed_tree):
    return RecfileTransformer().transform(parsed_tree)


logseq_parser = Lark.open("logseq.lark", rel_to=__file__)
recfile_parser = Lark.open("recfile.lark", rel_to=__file__)


def get_parser_and_transformer(file_path):
    file_extension = Path(file_path).suffix
    if file_extension == '.rec':
        return recfile_parser, recfile_to_intermediate
    elif file_extension == '.md':
        return logseq_parser, logseq_to_intermediate
    else:
        raise ValueError('Unsupported file extension')


def convert_to_intermediate(input_file, verbose=False):
    parser, transformer = get_parser_and_transformer(input_file)
    with open(input_file, 'r') as file:
        input_text = file.read()
    parsed_tree = parser.parse(input_text)
    transformed = transformer(parsed_tree)
    if verbose:
        print(parsed_tree.pretty())
        pprint(transformed)
    return transformed


def intermediate_to_recfile(intermediate):
    output = []
    for block in intermediate:
        properties = []
        firstline = next(
            (c for c in block['content'] if c['type'] == 'firstline'), None)
        if firstline and firstline['content'].strip(
        ):  # Check if firstline is not empty
            properties.append(f"firstline: {firstline['content'].strip()}")
        for item in block['content']:
            if item['type'] == 'property':
                properties.append(f"{item['key']}:{item['value']}")
        output.append('\n'.join(properties))
    return '\n\n'.join(output)  # Double newline to separate records


def intermediate_to_logseq(intermediate):
    output = []
    for record in intermediate:
        block_text = "- "  # Start with the block marker
        properties = []
        for item in record['content']:
            if isinstance(item, dict) and item['type'] == 'property':
                if item['key'] == 'firstline':
                    block_text += item['value'].strip() + '\n'
                else:
                    properties.append(f"  {item['key']}::{item['value']}")

        if block_text == "- ":  # If no id was found, add a newline
            block_text += '\n'
        block_text += '\n'.join(properties)
        output.append(block_text)
    return '\n\n'.join(output)  # Double newline to separate blocks


def intermediate_to_csv(intermediate):
    # Collect all unique keys
    all_keys = set()
    for block in intermediate:
        for item in block['content']:
            if item['type'] == 'property':
                all_keys.add(item['key'])

    # Sort keys for consistent ordering
    sorted_keys = sorted(all_keys)

    # Prepare the header
    header = ['firstline'] + sorted_keys

    # Prepare the CSV rows
    rows = [','.join(header)]
    for block in intermediate:
        row = [''] * (len(header))  # Initialize with empty strings
        for item in block['content']:
            if item['type'] == 'firstline':
                row[0] = item['content'].strip()
            elif item['type'] == 'property':
                index = header.index(item['key'])
                row[index] = item['value'].strip()
        rows.append(','.join(row))

    return '\n'.join(rows)


def convert_format(input_file, output_format, verbose=False):
    intermediate = convert_to_intermediate(input_file, verbose)
    if output_format == 'recfile':
        return intermediate_to_recfile(intermediate)
    elif output_format == 'logseq':
        return intermediate_to_logseq(intermediate)
    elif output_format == 'csv':
        return intermediate_to_csv(intermediate)
    else:
        raise ValueError('Unsupported output format')


def test_conversion(input_file, output_format, verbose=False):
    converted = convert_format(input_file, output_format, verbose)
    return converted


def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_file> <output_format> [verbose]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_format = sys.argv[2]
    verbose = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else False

    # Handle relative paths
    if not input_file.is_absolute():
        input_file = Path.cwd() / input_file

    try:
        converted = convert_format(input_file, output_format, verbose)
        print(converted)  # Output to stdout
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
