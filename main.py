import argparse
from reconciler.reconciler import Reconciler
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(description="Provivi data reconciler, Jalisco only")
    parser.add_argument(
        "-i", "--input", help="The input directory with Jalisco Provivi data files that this utility will reconcile.", required=True
    )

    parser.add_argument(
        "-o", "--output", help="The output file where logs will go.", required=True
    )
    return parser


def parse_args():
    parser = build_parser()
    args = parser.parse_args()
    if not Path(args.input).is_dir():
        print('The input file "{input}" must exist.')
        return
    else:
        return args


def main():
    args = parse_args()
    reconciler = Reconciler()
    reconciler.reconcile_data_files(args.input, args.output)


if __name__ == "__main__":
    main()
