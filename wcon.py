#!/usr/bin/env python3
################################################################################
#                                                                              #
#   PROJECT: DOCX Content Extractor                                            #
#   VERSION: 1.1.0                                                             #
#                                                                              #
#   AUTHOR:  Percio Andrade                                                    #
#   CONTACT: percio@evolya.com.br | contato@perciocastelo.com.br               #
#   WEB:     https://perciocastelo.com.br                                      #
#                                                                              #
#   INFO:                                                                      #
#   Extract text and images from DOCX files, preserving order.                 #
#                                                                              #
################################################################################

import os
import sys
import io
import logging
import argparse
import time

# --- DEPENDENCY CHECK ---
try:
    from docx import Document
    from PIL import Image
except ImportError as e:
    print(f"CRITICAL ERROR: Missing dependency. ({e})")
    print("Please run: pip install python-docx Pillow")
    sys.exit(1)

# --- I18N CONFIGURATION ---
system_lang = os.getenv('LANG', 'en')[:2]

if system_lang == 'pt':
    # Portuguese Strings
    MSG_DESC = "Extrai texto e imagens de um arquivo DOCX preservando a ordem."
    MSG_ARG_FILE = "Caminho para o arquivo DOCX."
    MSG_ARG_OUT = "Diretório de saída (Padrão: ./output)."
    MSG_START = "Iniciando extração do documento:"
    MSG_ERR_FILE = "ERRO: O arquivo '{}' não existe."
    MSG_PROC_PARA = "Processando parágrafo {}: Texto extraído, {} imagens encontradas."
    MSG_IMG_SAVED = "Imagem salva:"
    MSG_IMG_ERR = "Erro ao salvar imagem:"
    MSG_DONE_TXT = "Extração concluída. Texto salvo em:"
    MSG_DONE_IMG = "Imagens salvas em:"
    MSG_NO_DOC = "Documento não encontrado."
else:
    # English Strings (Default)
    MSG_DESC = "Extracts text and images from a DOCX file preserving order."
    MSG_ARG_FILE = "Path to the DOCX file."
    MSG_ARG_OUT = "Output directory (Default: ./output)."
    MSG_START = "Starting extraction for document:"
    MSG_ERR_FILE = "ERROR: The file '{}' does not exist."
    MSG_PROC_PARA = "Processing paragraph {}: Text extracted, {} images found."
    MSG_IMG_SAVED = "Image saved:"
    MSG_IMG_ERR = "Error saving image:"
    MSG_DONE_TXT = "Extraction complete. Text saved to:"
    MSG_DONE_IMG = "Images saved to:"
    MSG_NO_DOC = "Document not found."

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_content(doc_path, output_dir):
    """
    Main function to traverse the document and extract content.
    """
    document = Document(doc_path)
    text_content = ""
    image_counter = 1
    
    doc_name = os.path.splitext(os.path.basename(doc_path))[0]
    
    logging.info(f"{MSG_START} {doc_name}")

    for para_index, para in enumerate(document.paragraphs):
        # 1. Extract Text
        text = extract_text(para)
        text_content += text

        # 2. Extract Images (Inline and Anchored)
        # We pass the doc_name to prefix image filenames
        image_paths = extract_images_from_paragraph(para, output_dir, doc_name, image_counter)
        
        for image_path in image_paths:
            image_filename = os.path.basename(image_path)
            # Markdown style embedding reference
            text_content += f"\n![{image_filename}]({image_filename})\n"
            image_counter += 1

        if len(image_paths) > 0:
            logging.info(MSG_PROC_PARA.format(para_index + 1, len(image_paths)))

    return text_content

def extract_text(paragraph):
    """
    Extracts text from a paragraph and adds spacing.
    """
    if paragraph.text.strip():
        return f"{paragraph.text}\n\n"
    return ""

def extract_images_from_paragraph(paragraph, output_dir, doc_name, start_counter):
    """
    Scans a paragraph for images (both standard inline shapes and XML drawingML).
    """
    image_paths = []
    current_counter = start_counter

    for run in paragraph.runs:
        # A) Try extracting standard inline shapes
        if hasattr(run, 'inline_shapes'):
            for shape in run.inline_shapes:
                if shape.type == 3:  # 3 = PICTURE
                    # Accessing internal structure to get the BLIP/Relationship ID
                    try:
                        r_id = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
                        image_path = save_image(r_id, run.part, output_dir, doc_name, current_counter)
                        if image_path:
                            image_paths.append(image_path)
                            current_counter += 1
                    except Exception:
                        pass # Skip if structure is not standard

        # B) Try extracting XML drawings (more robust for some DOCX versions)
        # Namespaces for XML parsing
        ns = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
            'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
        }
        
        # Access the underlying XML element
        if run._element.findall('.//wp:inline', namespaces=ns) or run._element.findall('.//wp:anchor', namespaces=ns):
            for graphic in run._element.findall('.//a:blip', namespaces=ns):
                r_id = graphic.get(f"{{{ns['r']}}}embed")
                if r_id:
                    image_path = save_image(r_id, run.part, output_dir, doc_name, current_counter)
                    if image_path:
                        image_paths.append(image_path)
                        current_counter += 1

    return image_paths

def save_image(rel_id, part, output_dir, doc_name, counter):
    """
    Saves the image binary data to a PNG file.
    """
    try:
        if rel_id not in part.related_parts:
            return None

        image_part = part.related_parts[rel_id]
        image_bytes = image_part.blob
        
        # Convert/Save using Pillow
        image = Image.open(io.BytesIO(image_bytes))
        
        # Define filename
        image_filename = f"{doc_name}_img_{counter:03d}.png"
        image_path = os.path.join(output_dir, image_filename)
        
        # Save as PNG to ensure compatibility
        image.save(image_path, 'PNG')
        
        logging.info(f"{MSG_IMG_SAVED} {image_filename}")
        return image_path

    except Exception as e:
        logging.error(f"{MSG_IMG_ERR} {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description=MSG_DESC)
    parser.add_argument("arquivo", help=MSG_ARG_FILE)
    parser.add_argument("-o", "--output", help=MSG_ARG_OUT, default="./output")
    args = parser.parse_args()

    doc_path = args.arquivo
    base_output_dir = args.output

    if not os.path.exists(doc_path):
        logging.error(MSG_ERR_FILE.format(doc_path))
        sys.exit(1)

    # Create specific folder for this document
    doc_name = os.path.splitext(os.path.basename(doc_path))[0]
    output_dir = os.path.join(base_output_dir, doc_name)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Execute extraction
    text_content = extract_content(doc_path, output_dir)

    # Save text
    output_file = os.path.join(output_dir, f"{doc_name}.md") # Saving as Markdown usually handles images better
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text_content)

    logging.info("-" * 40)
    logging.info(f"{MSG_DONE_TXT} {output_file}")
    logging.info(f"{MSG_DONE_IMG} {output_dir}")
    logging.info("-" * 40)

if __name__ == "__main__":
    main()
