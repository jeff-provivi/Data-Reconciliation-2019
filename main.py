import argparse
from conversion.converter import Converter
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(description="Provivi data converter")
    parser.add_argument(
        "-i", "--input", help="The input directory with Provivi data files that this utility will transform.", required=True
    )

    parser.add_argument(
        "-o", "--output", help="The output directory where transformed files will go.", required=True
    )
    return parser


def parse_args():
    parser = build_parser()
    args = parser.parse_args()
    if not Path(args.input).is_dir():
        print(f'The input file "{input}" must exist.')
        return
    else:
        return args


def main():
    args = parse_args()
    converter = Converter()
    converter.correct_data_files(args.input, args.output)


if __name__ == "__main__":
    main()
