#!/usr/bin/env python3
'''Command line interface for kicad-sandwiches'''
import argparse
import sys
import os
from pathlib import Path

from .core import sandwich_from_file


def main():
    parser = argparse.ArgumentParser(
        description='creates sandwich/oreo PCB boards from KiCad files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s board.kicad_pcb --which-one LOW
  %(prog)s board.kicad_pcb --which-one TOP --outfile top_board.kicad_pcb
  %(prog)s board.kicad_pcb --which-one MID --outfile output/mid_board.kicad_pcb

Available which_one values:
  TOP     - Top board of the sandwich
  LOW     - Bottom board of the sandwich
  MID     - Middle board (for 3-board sandwiches)
  STENCIL - Stencil board
        """
    )

    parser.add_argument(
        'infile',
        help='Input KiCad PCB file (.kicad_pcb)'
    )

    parser.add_argument(
        '--which-one',
        choices=['TOP', 'LOW', 'MID', 'STENCIL'],
        default='LOW',
        help='Which board layer to generate (default: LOW)'
    )

    parser.add_argument(
        '--outfile', '-o',
        help='Output PCB file (default: creates kisandwich-out/[basename]-sandwich_[which_one].kicad_pcb)'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Validate input file exists
    if not os.path.exists(args.infile):
        print(f"Error: Input file '{args.infile}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Validate input file extension
    if not args.infile.lower().endswith('.kicad_pcb'):
        print(f"Error: Input file must be a .kicad_pcb file", file=sys.stderr)
        sys.exit(1)

    # Create output directory if needed
    if args.outfile:
        out_dir = os.path.dirname(args.outfile)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

    try:
        sandwich_from_file(args.infile, args.which_one, args.outfile)
        print(f"Successfully created sandwich board: {args.outfile or 'default location'}")
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
