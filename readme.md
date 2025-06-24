# DOCX Content Extractor

## Features

- Extracts plain text from paragraphs in DOC/DOCX files.
- Extracts inline and embedded images, saving them as PNG files.
- Organizes extracted content into an output directory.
- Logs progress and errors for easy debugging.

## Requirements

- Python 3.6 or higher.
- The following Python libraries:
  - `python-docx`
  - `Pillow`
  - `argparse`

You can install the required libraries using pip:

```bash
pip install python-docx Pillow
```

## Usage

Run the script from the command line with the following syntax:
```bash
python script.py <arquivo> [-o <output_directory>]
```

### Positional Arguments
- `<arquivo>`: Path to the DOC/DOCX file to be processed.

### Optional Arguments
- `-o, --output`: Custom output directory. Defaults to `/home/convert/`.

### Example
```bash
python script.py example.docx -o ./output/
```

This will:
1. Extract text and images from `example.docx`.
2. Save the extracted text as `example_output.txt` in the `./output/example/` directory.
3. Save all extracted images as PNG files in the same directory.

## Output Structure

The extracted content will be organized as follows:

* <output_directory>/
* └── <document_name>/
* ├── <document_name>_output.txt

# Extracted text
* ├── <document_name>_01.png # Extracted images
* ├── <document_name>_02.png
* └── <document_name>_03.png

## Logging

The script logs the extraction process, including:
- Text and image processing progress.
- Saved file paths.
- Errors encountered during execution.

## Error Handling

- Verifies if the input file exists before processing.
- Logs errors when failing to extract or save images.
- Gracefully handles exceptions during the extraction process.

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## Acknowledgments

- [python-docx](https://python-docx.readthedocs.io/) for handling DOCX files.
- [Pillow](https://pillow.readthedocs.io/) for image processing.