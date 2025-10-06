# pdf-util

PDF utility for splitting and manipulating PDF files.

## Features

- **PDF Splitting**: Split PDF files into multiple chapters by specifying page numbers

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd pdf-util

# Install dependencies with uv
uv sync
```

## Usage

### PDF Splitting

Split a PDF file into multiple chapters by specifying the start page of each chapter:

```bash
# Using the installed command
pdf-split -i input.pdf -o output/ -p 1,10,20,30

# Or run as a module
uv run python -m pdf_util.split -i input.pdf -o output/ -p 1,10,20,30
```

**Arguments:**
- `-i, --input FILE`: Input PDF file path
- `-o, --output DIR`: Output directory path
- `-p, --pages PAGES`: Chapter start page numbers (comma-separated)

**Example:**
```bash
pdf-split -i book.pdf -o chapters/ -p 1,50,100,150
```

This will create:
- `book_chapter01_p1-49.pdf` (pages 1-49)
- `book_chapter02_p50-99.pdf` (pages 50-99)
- `book_chapter03_p100-149.pdf` (pages 100-149)
- `book_chapter04_p150-end.pdf` (pages 150 to the end)

### Help

```bash
pdf-split --help
```

## Requirements

- Python 3.12+
- pypdf 6.1.1+
