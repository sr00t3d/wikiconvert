import os
import sys
from docx import Document
from PIL import Image
import io
import logging
import argparse

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_content(doc_path, output_dir):
    document = Document(doc_path)
    text_content = ""
    image_counter = 1
    
    # Get the base name of the document (without extension)
    doc_name = os.path.splitext(os.path.basename(doc_path))[0]
    
    logging.info(f"Iniciando extração do documento: {doc_name}")

    for para_index, para in enumerate(document.paragraphs):
        # Extract text
        text_content += extract_text(para)

        # Extract images
        image_paths = extract_images(para, output_dir, doc_name, image_counter)
        for image_path in image_paths:
            image_filename = os.path.basename(image_path)
            text_content += f"\n[[{image_filename}]]\n"
            image_counter += 1

        logging.info(f"Processado parágrafo {para_index + 1}: Texto extraído, {len(image_paths)} imagens encontradas")

    return text_content

def extract_text(paragraph):
    return f"{paragraph.text}\n\n"

def extract_images(paragraph, output_dir, doc_name, counter):
    image_paths = []
    for run in paragraph.runs:
        # Tentar extrair imagens inline
        if hasattr(run, 'inline_shapes'):
            for shape in run.inline_shapes:
                if shape.type == 3:  # 3 é o tipo para imagens
                    image_path = save_image(shape._inline.graphic.graphicData.pic.blipFill.blip.embed, 
                                            run.part, output_dir, doc_name, counter)
                    if image_path:
                        image_paths.append(image_path)
                        counter += 1

        # Tentar extrair imagens de desenhos
        if run._element.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}inline'):
            for inline in run._element.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}inline'):
                blip = inline.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
                if blip is not None:
                    image_path = save_image(blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed'),
                                            run.part, output_dir, doc_name, counter)
                    if image_path:
                        image_paths.append(image_path)
                        counter += 1

    return image_paths

def save_image(rel_id, part, output_dir, doc_name, counter):
    try:
        image_part = part.related_parts[rel_id]
        image_bytes = image_part.blob
        
        # Convert image to PNG
        image = Image.open(io.BytesIO(image_bytes))
        image_filename = f"{doc_name}_{counter:02d}.png"
        image_path = os.path.join(output_dir, image_filename)
        image.save(image_path, 'PNG')
        
        logging.info(f"Imagem salva: {image_filename}")
        return image_path
    except Exception as e:
        logging.error(f"Erro ao salvar imagem: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Extrai texto e imagens de um arquivo DOC/DOCX.")
    parser.add_argument("arquivo", help="Caminho para o arquivo DOC/DOCX a ser convertido")
    parser.add_argument("-o", "--output", help="Diretório de saída personalizado", default="/home/convert/")
    args = parser.parse_args()

    doc_path = args.arquivo
    base_output_dir = args.output

    if not os.path.exists(doc_path):
        logging.error(f"O arquivo {doc_path} não existe.")
        sys.exit(1)

    # Criar diretório de saída baseado no nome do arquivo
    doc_name = os.path.splitext(os.path.basename(doc_path))[0]
    output_dir = os.path.join(base_output_dir, doc_name)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    text_content = extract_content(doc_path, output_dir)

    # Save the plain text content
    output_file = os.path.join(output_dir, f"{doc_name}_output.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text_content)

    logging.info(f"Extração concluída. O conteúdo de texto foi salvo em {output_file}")
    logging.info(f"As imagens extraídas foram salvas no diretório: {output_dir}")

if __name__ == "__main__":
    main()