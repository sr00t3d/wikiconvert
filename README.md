# WikiConvert 📄➡️📝

Readme: [Português](README.pt-br.md)

<img src="https://github.com/user-attachments/assets/f3ba2f1b-75ea-4905-8935-2e9690822062" width="700">

![License](https://img.shields.io/github/license/sr00t3d/bindfilter)
![Python Script](https://img.shields.io/badge/python-script-green)

**WikiConvert** is a robust tool developed in Python to convert **Microsoft Word (.docx, .doc)** documents to **Markdown (.md)** format. It is ideal for developers and technical writers who need to migrate offline documentation to Git repositories, blogs, or static documentation systems.

## ✨ Features

- **Text Extraction**: Converts Word paragraphs while preserving the basic plain text structure.
- **Image Management**: Automatically extracts inline or embedded images in the document, saving them as .png files.**
- **Smart Organization**: Creates a structured output directory with the formatted content and a dedicated folder for visual assets.
- **Debug Logs**: Integrated logging system to track progress and identify potential errors in complex documents.

## 🚀 How to Use

1 Installation:

```bash
git clone https://github.com/sr00t3d/wikiconvert/
cd wikiconvert
```
2 Requirements: Install the `python-docx` library (required to read Word files):

```bash
pip install python-docx
```
3 Execution:

Place your `.docx` file in the script folder and run the converter:

```bash
python3 wikiconvert.py
```

## 📂 Output Structure

When converting a file, the script generates:

- A `.md` file with the processed content.
- An `/images` folder containing all figures extracted from the original document.

## ⚠️ Disclaimer

> [!WARNING]
> This software is provided "as is". Always make sure to perform testing in a development environment first. The author is not responsible for any misuse, legal consequences, or data impact caused by this tool.

## 📚 Detailed Tutorial

For a complete, step-by-step guide on how to convert the files, check out my full article:

👉 [**Converting DOC and DOCX to MarkDown**](https://perciocastelo.com.br/blog/converting-doc-and-docx-to-markdown.html)

## License 📄

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for more details.
