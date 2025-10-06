#!/usr/bin/env python3
"""
PDF splitting tool - Split PDF into chapters by specified page numbers

Usage:
    python split_pdf.py -i input.pdf -o output/ -p 1,10,20,30

Example:
    python split_pdf.py -i input.pdf -o output/ -p 1,10,20,30
    → Splits into pages 1-9, 10-19, 20-29, 30-end
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from pypdf import PdfReader, PdfWriter


@dataclass
class SplitConfig:
    """Configuration for PDF splitting"""

    input_pdf: Path
    output_dir: Path
    page_breaks: list[int]

    def __post_init__(self):
        if not self.input_pdf.exists():
            raise FileNotFoundError(f"Input file '{self.input_pdf}' not found")

        if not self.page_breaks:
            raise ValueError("Page list is empty")

        # Sort page numbers in ascending order
        self.page_breaks = sorted(self.page_breaks)


class PdfSplitter:
    """PDF splitter class"""

    def __init__(self, config: SplitConfig):
        self.config = config
        self.reader = PdfReader(config.input_pdf)
        self.total_pages = len(self.reader.pages)

    def split(self) -> int:
        """
        Split PDF by specified page numbers

        Returns:
            Number of files created
        """
        # Create output directory
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        # Get input filename without extension
        input_name = self.config.input_pdf.stem
        files_created = 0

        for i, start_page in enumerate(self.config.page_breaks):
            # Determine end page (next chapter start or last page)
            if i + 1 < len(self.config.page_breaks):
                end_page = self.config.page_breaks[i + 1] - 1
            else:
                end_page = self.total_pages

            # Validate page numbers
            if start_page < 1 or start_page > self.total_pages:
                print(f"Warning: Page {start_page} is out of range. Skipping.")
                continue

            if end_page > self.total_pages:
                end_page = self.total_pages

            # Create PDF writer and add pages
            writer = PdfWriter()
            for page_num in range(start_page - 1, end_page):  # Convert to 0-indexed
                writer.add_page(self.reader.pages[page_num])

            # Generate output filename
            output_filename = (
                self.config.output_dir
                / f"{input_name}_chapter{i+1:02d}_p{start_page}-{end_page}.pdf"
            )

            # Save PDF
            with open(output_filename, "wb") as output_file:
                writer.write(output_file)

            print(f"Created: {output_filename} (pages {start_page}-{end_page})")
            files_created += 1

        return files_created


def parse_page_list(page_str: str) -> list[int]:
    """
    Parse comma-separated page number list

    Args:
        page_str: Comma-separated page number string (e.g., "1,10,20,30")

    Returns:
        List of page numbers

    Raises:
        ValueError: If parsing fails
    """
    try:
        return [int(x.strip()) for x in page_str.split(",")]
    except ValueError as e:
        raise ValueError("Page list must be comma-separated numbers") from e


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split PDF into chapters by specified page numbers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i input.pdf -o output/ -p 1,10,20,30
  %(prog)s --input book.pdf --output chapters/ --pages 1,50,100
        """,
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        metavar="FILE",
        help="Input PDF file path",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        metavar="DIR",
        help="Output directory path",
    )

    parser.add_argument(
        "-p",
        "--pages",
        type=str,
        required=True,
        metavar="PAGES",
        help="Chapter start page numbers (comma-separated, e.g., 1,10,20,30)",
    )

    return parser.parse_args()


def main():
    try:
        args = parse_args()
        page_breaks = parse_page_list(args.pages)

        config = SplitConfig(
            input_pdf=args.input, output_dir=args.output, page_breaks=page_breaks
        )

        splitter = PdfSplitter(config)
        files_created = splitter.split()

        print(f"\nSplit complete: {files_created} file(s) created")

    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
