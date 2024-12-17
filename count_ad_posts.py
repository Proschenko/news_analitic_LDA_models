import csv
import re

def count_ad_posts(file_path):
    """
    Подсчитывает количество постов реклама в указанном CSV-файле.
    :param file_path: Путь к CSV-файлу с постами.
    :return: Количество постов с рекламой
    """
    ad_count = 0

    with open(file_path, 'r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            text = row.get('text', '')
            if re.search(r'реклама', text, re.IGNORECASE):
                ad_count += 1

    return ad_count

# Пример использования
if __name__ == "__main__":
    input_file = r'C:\Users\Prosc\PycharmProjects\tg_channel_parser\telegram_posts_2024.csv'
    ad_posts_count = count_ad_posts(input_file)
    print(f"Количество постов рекламой {ad_posts_count}")