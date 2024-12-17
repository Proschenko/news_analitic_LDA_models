import csv
import re
import logging

def clean_text_and_extract_hashtags(text):
    """
    Удаляет хэштеги из текста и возвращает их в отдельный список.
    :param text: Исходный текст сообщения.
    :return: Очищенный текст и список хэштегов.
    """
    hashtags = re.findall(r"#\w+", text)
    text_without_hashtags = re.sub(r"#\w+", "", text)
    return text_without_hashtags.strip(), hashtags

def clean_text_advanced(text):
    """
    Дополнительная очистка текста (эмодзи, ссылки, упоминания и медиа-обозначения).
    :param text: Исходный текст.
    :return: Очищенный текст.
    """
    text = re.sub(r"@\w+", "", text)  # Удаление упоминаний
    text = re.sub(r'https?://\S+|www\.\S+', "", text)  # Удаление ссылок
    text = re.sub(r"\[.*?\]", "", text)  # Удаление медиа-обозначений

    # Удаление эмодзи (включая ⏱, ⏺, ⌛ и другие символы)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Смайлики
        "\U0001F300-\U0001F5FF"  # Символы и пиктограммы
        "\U0001F680-\U0001F6FF"  # Транспорт
        "\U0001F700-\U0001FAFF"  # Алхимические, игровые и другие символы
        "\U00002700-\U000027BF"  # Дополнительные символы (⏱, ⏺, ⌛)
        "\U00002600-\U000026FF"  # Различные символы (например, ☀, ☂)
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)

    text = re.sub(r"\s+", " ", text).strip()  # Удаление лишних пробелов
    return text

def process_csv_clean(input_file, output_file):
    """
    Обрабатывает CSV-файл, очищает текст, извлекает хэштеги и сохраняет результат в новый файл.
    :param input_file: Входной CSV файл.
    :param output_file: Выходной CSV файл.
    """
    with open(input_file, 'r', encoding='utf-8-sig') as infile, \
         open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['hashtags']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            text = row['text']
            cleaned_text, hashtags = clean_text_and_extract_hashtags(text)
            cleaned_text = clean_text_advanced(cleaned_text)
            row['text'] = cleaned_text
            row['hashtags'] = ', '.join(hashtags)
            writer.writerow(row)

def remove_ad_posts(input_file, output_file, log_file):
    """
    Удаляет записи, связанные с рекламой, из CSV файла и пишет логи в файл.
    :param input_file: Входной CSV файл.
    :param output_file: Выходной CSV файл.
    :param log_file: Файл для записи логов.
    """
    ad_keywords = ['реклама', 'Реклама', '#реклама']
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    with open(input_file, 'r', encoding='utf-8-sig') as infile, \
         open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            text = row.get('text', '')
            if any(keyword in text for keyword in ad_keywords):
                logging.info(f"Removed post: {text}")
            else:
                writer.writerow(row)

def preprocess_csv(input_file, output_file):
    """
    Препроцессинг текста: приведение к нижнему регистру и удаление спецсимволов.
    :param input_file: Входной CSV файл.
    :param output_file: Выходной CSV файл.
    """
    with open(input_file, 'r', encoding='utf-8-sig') as infile, \
         open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            text = row.get('text', '').lower()  # Приведение текста к нижнему регистру
            text = re.sub(r"[^а-яa-z0-9\s]", "", text)  # Удаление спецсимволов
            row['text'] = text.strip()
            writer.writerow(row)

if __name__ == "__main__":
    # Шаг 1: Очистка текста и извлечение хэштегов
    process_csv_clean('input.csv', 'cleaned.csv')

    # Шаг 2: Удаление записей, связанных с рекламой
    remove_ad_posts('cleaned.csv', 'no_ads.csv', 'removed_ads.log')

    # Шаг 3: Препроцессинг текста
    preprocess_csv('no_ads.csv', 'preprocessed.csv')
