import pdfplumber
import os
import pytesseract


def extract_text_from_pdf(pdf_path, txt_path=None):
    """
    Извлекает текст из PDF-файла и сохраняет его в текстовый файл.

    :param pdf_path: Путь к PDF-файлу.
    :param txt_path: Путь для сохранения текстового файла. Если не указан,
                     будет использовано то же имя файла с расширением .txt.
    :return: Извлечённый текст из PDF.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"Файл {pdf_path} не найден.")

    # Если имя текстового файла не указано, сформируем его на основе имени PDF
    if txt_path is None:
        base, _ = os.path.splitext(pdf_path)
        txt_path = f"{base}.txt"

    extracted_text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
                else:
                    print(f"Предупреждение: Текст не найден на странице {page_number}.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при обработке PDF-файла: {e}")

    try:
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(extracted_text)
        print(f"Текст успешно сохранён в {txt_path}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при сохранении текстового файла: {e}")

    return extracted_text


def extract_text_from_pdf_with_ocr(pdf_path, txt_path=None):
    """
    Извлекает текст из PDF-файла, включая сканированные изображения, и сохраняет его в текстовый файл.

    :param pdf_path: Путь к PDF-файлу.
    :param txt_path: Путь для сохранения текстового файла. Если не указан,
                     будет использовано то же имя файла с расширением .txt.
    :return: Извлечённый текст из PDF.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"Файл {pdf_path} не найден.")

    if txt_path is None:
        base, _ = os.path.splitext(pdf_path)
        txt_path = f"{base}.txt"

    extracted_text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
                else:
                    # Если на странице нет текста, попробуем извлечь изображение и применить OCR
                    print(f"Текст не найден на странице {page_number}. Применение OCR...")
                    im = page.to_image(resolution=300)
                    pil_image = im.original
                    ocr_text = pytesseract.image_to_string(pil_image, lang='rus')  # Укажите нужный язык
                    extracted_text += ocr_text + "\n"
    except Exception as e:
        raise RuntimeError(f"Ошибка при обработке PDF-файла: {e}")

    try:
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(extracted_text)
        print(f"Текст успешно сохранён в {txt_path}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при сохранении текстового файла: {e}")

    return extracted_text