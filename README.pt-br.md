# WikiConvert 📄➡️📝

Readme: [English](README.md)

<img src="https://github.com/user-attachments/assets/f3ba2f1b-75ea-4905-8935-2e9690822062" width="700">

![License](https://img.shields.io/github/license/sr00t3d/bindfilter)
![Python Script](https://img.shields.io/badge/python-script-green)

**WikiConvert** é uma ferramenta robusta desenvolvida em Python para converter documentos **Microsoft Word (.docx, .doc)** para o formato **Markdown (.md)**. Ele é ideal para desenvolvedores e escritores técnicos que precisam migrar documentações offline para repositórios Git, blogs ou sistemas de documentação estática.

## ✨ Funcionalidades

- **Extração de Texto**: Converte parágrafos do Word preservando a estrutura básica de texto puro.
- **Gestão de Imagens**: Extrai automaticamente imagens inline ou embutidas no documento, salvando-as como arquivos .png.**
- **Organização Inteligente**: Cria um diretório de saída estruturado com o conteúdo formatado e uma pasta dedicada para os ativos visuais.
- **Logs de Depuração**: Sistema de logs integrado para acompanhar o progresso e identificar eventuais erros em documentos complexos.

## 🚀 Como Usar

1 Instalação:

```bash
git clone https://github.com/sr00t3d/wikiconvert/
cd wikiconvert
```
2 Requisitos: Instale a biblioteca `python-docx` (necessária para ler os arquivos do Word):

```bash
pip install python-docx
```
3 Execução:

Coloque seu arquivo `.docx` na pasta do script e execute o conversor:

```bash
python3 wikiconvert.py
```

## 📂 Estrutura de Saída

Ao converter um arquivo, o script gera:

- Um arquivo `.md` com o conteúdo processado.
- Uma pasta `/images` contendo todas as figuras extraídas do documento original.

## ⚠️ Disclaimer

> [!WARNING]
> Este software é fornecido "tal como está". Certifique-se sempre realizar testes em ambiente de desenvolvimento antes. O autor não se responsabiliza por qualquer uso indevido, consequências legais ou impacto nos dados causados ​​por esta ferramenta.

## 📚 Tutorial Detalhado

Para um guia completo, passo a passo, sobre como converter os arquivos, confira meu artigo completo:

👉 [**Converting DOC and DOCX to MarkDown**](https://perciocastelo.com.br/blog/converting-doc-and-docx-to-markdown.html)

## Licença 📄

Este projeto está licenciado sob a **GNU General Public License v3.0**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
