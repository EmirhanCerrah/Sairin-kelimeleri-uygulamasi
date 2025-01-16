"""
Bu modül, Antoloji.com'dan şiirleri çekmek ve işlemek için kullanılabilir.
Şiirler, belirtilen URL'den başlar ve ilişkili bağlantılar üzerinden taranır.
Şiir metinleri işlenir, noktalama işaretlerinden arındırılır ve baş harflerden önce boşluk eklenir.
Elde edilen şiirler, bir dosyaya düzenlenmiş biçimde kaydedilir.

Modülün temel işlevleri:
- Şiir bağlantılarını taramak.
- Şiir içeriklerini işlemek ve biçimlendirmek.
- Şiirleri belirtilen bir dosyaya kaydetmek.

Kullanım:
    initial_url = "https://www.antoloji.com/siir/"
    visited_urls = set()
    processed_sentences = set()
    with open("siirler.txt", "w", encoding="utf-8") as file:
        scrape_top500_poems(initial_url, visited_urls, processed_sentences, file)
"""

import requests
from bs4 import BeautifulSoup
import re

def add_space_before_capitals(text):
    """
    Büyük harflerden önce boşluk ekler.

    Args:
        text (str): İşlenecek metin.

    Returns:
        str: Büyük harflerden önce boşluk eklenmiş metin.
    """
    return re.sub(r'(?<!\s)(?=[A-ZÇĞİÖŞÜ])', ' ', text)

def remove_punctuation(text):
    """
    Metinden tüm noktalama işaretlerini kaldırır.

    Args:
        text (str): İşlenecek metin.

    Returns:
        str: Noktalama işaretlerinden arındırılmış metin.
    """
    return re.sub(r'[^\w\sçğıöüş]', '', text)

def process_text(text):
    """
    Metni işler: noktalama işaretlerini kaldırır ve büyük harflerden önce boşluk ekler.

    Args:
        text (str): İşlenecek metin.

    Returns:
        str: İşlenmiş metin.
    """
    text_without_punctuation = remove_punctuation(text)
    words = text_without_punctuation.split()
    processed_words = [add_space_before_capitals(word) for word in words]
    return ' '.join(processed_words)

def scrape_poem_content(poem_url, processed_sentences, file):
    """
    Belirtilen URL'deki şiir içeriğini çeker, işler ve dosyaya kaydeder.

    Args:
        poem_url (str): Şiir URL'si.
        processed_sentences (set): Daha önce işlenmiş cümlelerin kümesi (tekrarları önlemek için).
        file (TextIOWrapper): Şiirlerin kaydedileceği dosya nesnesi.
    """
    poem_response = requests.get(poem_url)
    if poem_response.status_code == 200:
        poem_soup = BeautifulSoup(poem_response.content, "html.parser")
        poem_content = poem_soup.find("div", class_="pd-text")

        if poem_content:
            poem_text = ""
            for element in poem_content.descendants:
                if element.name == "br" or element.name == "p":
                    poem_text += "\n"
                elif isinstance(element, str):
                    poem_text += element

            sentences = poem_text.split('\n')
            for sentence in sentences:
                formatted_text = process_text(sentence)
                if formatted_text and formatted_text not in processed_sentences:
                    file.write(formatted_text + "\n")
                    processed_sentences.add(formatted_text)
        else:
            print(f"Şiir içeriği bulunamadı: {poem_url}")
    else:
        print(f"Şiir içeriği çekilemedi: {poem_url}, HTTP Durum Kodu: {poem_response.status_code}")

def scrape_top500_poems(url, visited_urls, processed_sentences, file):
    """
    Belirtilen URL'den başlayarak şiirleri tarar ve içeriklerini çeker.

    Args:
        url (str): Başlangıç URL'si.
        visited_urls (set): Daha önce ziyaret edilmiş URL'lerin kümesi (tekrarları önlemek için).
        processed_sentences (set): Daha önce işlenmiş cümlelerin kümesi.
        file (TextIOWrapper): Şiirlerin kaydedileceği dosya nesnesi.
    """
    if url in visited_urls:
        return
    visited_urls.add(url)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        poem_links = soup.find_all("div", class_="poem-list")
        urls = set()

        for link in poem_links:
            title_tag = link.find("a")
            if title_tag:
                poem_url = title_tag['href']
                full_poem_url = f"https://www.antoloji.com{poem_url}"
                urls.add(full_poem_url)

        for poem_url in urls:
            scrape_poem_content(poem_url, processed_sentences, file)
            scrape_top500_poems(poem_url, visited_urls, processed_sentences, file)
    else:
        print(f"Veri çekme başarısız oldu: {url}, HTTP Durum Kodu: {response.status_code}")

# Örnek kullanım
if __name__ == "__main__":
    initial_url = "https://www.antoloji.com/siir/"
    visited_urls = set()
    processed_sentences = set()

    with open("siirler.txt", "w", encoding="utf-8") as file:
        scrape_top500_poems(initial_url, visited_urls, processed_sentences, file)

    print("Şiirler 'siirler.txt' dosyasına kaydedildi.")
