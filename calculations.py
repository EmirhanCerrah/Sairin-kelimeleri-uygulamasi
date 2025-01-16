import datafonksiyon

def calculate_option1(self, instance):
    """
        Kullanıcı tarafından girilen seçeneklere göre kelimeler üzerinde filtreleme yapar.
        Kullanıcı "evet", "hayır" veya "diğer" seçeneklerinden birini seçebilir.

        Args:
            self: Uygulamanın mevcut durumu ve arayüz bileşenlerine erişimi sağlar.
            instance: Bu parametre, kivy'deki widget olaylarını temsil eder.

        Returns:
            None: Fonksiyon, filtrelenmiş sonuçları gösteren yeni bir sayfa açar.

        Notes:
            - "Evet" seçeneği, girilen kelimenin uzunluğu ve harfleri ile eşleşen kelimeleri filtreler.
            - "Hayır" seçeneği, girilen harfleri içeren kelimeleri ve belirtilen uzunluktaki kelimeleri filtreler.
            - "Diğer" seçeneği, belirtilen ek veya son hece, kelime uzunluğu veya ünlü sayısına göre filtreleme yapar.
    """
    vowels = {"a", "e", "ı", "i", "o", "ö", "u", "ü"}
    choice = self.spinner_choice.text.lower()

    results = datafonksiyon.tum_kelimeler

    if choice == "evet":
        word = self.input_word.text.lower()
        if word:
            length = len(word)
            results = [
                w for w in results if len(w) == length and set(w) == set(word)
            ]

    elif choice == "hayır":
        chars = self.input_word.text.lower()
        if chars:
            results = [
                w for w in results if all(char in w for char in chars)
            ]
        if self.input_length.text.isdigit():
            length = int(self.input_length.text)
            results = [
                w for w in results if len(w) == length
            ]

    elif choice == "diğer":
        known = self.input_known.text.lower()
        if known:
            results = [
                w for w in results if w.endswith(known)
            ]
        if self.input_length.text.isdigit():
            length = int(self.input_length.text)
            results = [
                w for w in results if len(w) == length
            ]
        if self.input_vowel_count.text.isdigit():
            vowel_count = int(self.input_vowel_count.text)
            results = [
                w for w in results if sum(1 for char in w if char in vowels) == vowel_count
            ]

    # Tekrar eden kelimeleri kaldırma
    results = list(set(results))
    # Sonuçları yeni sayfada göstermek için çağır
    self.show_results_page(results)


def kelime_bulma_tum(cumle, aranan_kelime, son_hece=None):
    """
        Verilen bir cümlede, aranan kelimenin etrafındaki kelimeleri ve son hecesini bulur.

        Args:
            cumle (str): İçinde arama yapılacak cümle.
            aranan_kelime (str): Aranacak olan kelime.
            son_hece (str, optional): Aranacak kelimenin sonrasındaki kelimenin son hecesi. Varsayılan değeri None'dur.

        Returns:
            list: Eşleşen kelimelerle birlikte, önceki kelime, aranan kelime, sonraki kelime ve sonraki kelimenin son hecesi bilgilerini içeren bir liste.

        Notes:
            - Küçük/büyük harf duyarlılığına dikkat edilmez.
            - Eğer son_hece belirtilmişse, sonraki kelimenin son hecesi kontrol edilir.
            - Eğer sonrasında kelime yoksa, "Son yok" değeri döndürülür.
    """
    kelimeler = cumle.split()
    sonuc = []
    son_hece_uzunlugu = len(son_hece) if son_hece else 2  # Eğer son_hece belirtilmişse onun uzunluğu, yoksa varsayılan 2

    for index, kelime in enumerate(kelimeler):
        if kelime == aranan_kelime:
            onceki_kelime = kelimeler[index - 1] if index > 0 else "Başlangıç yok"
            sonraki_kelime = kelimeler[index + 1] if index < len(kelimeler) - 1 else "Son yok"

            # Eğer sonrasında bir kelime varsa, onun dinamik son hecesini kontrol et
            if sonraki_kelime != "Son yok":
                kelimenin_son_hecesi = sonraki_kelime[-son_hece_uzunlugu:]  # Girilen uzunluğa göre son harfleri al
                if son_hece is None or kelimenin_son_hecesi == son_hece:
                    sonuc.append((onceki_kelime, kelime, sonraki_kelime, kelimenin_son_hecesi))
    return sonuc

def calculate_option2(self, instance):
    """
        Kullanıcı tarafından girilen kelime ve son heceye göre, bir şiir dosyasındaki cümlelerde eşleşen kelimeleri bulur.

        Args:
            self: Uygulamanın mevcut durumu ve arayüz bileşenlerine erişimi sağlar.
            instance: Bu parametre, kivy'deki widget olaylarını temsil eder.

        Returns:
            None: Fonksiyon, eşleşen kelimeleri ve ilişkili bilgileri yeni bir sayfada gösterir.

        Notes:
            - Şiir dosyasındaki her cümlede, aranan kelimenin etrafındaki kelimeler ve son hecesi görüntülenir.
            - Eğer kullanıcı bir son hece belirtirse, bu son hece kontrol edilir.
            - Eşleşen her kelime için "önceki kelime", "aranan kelime", "sonraki kelime" ve "sonraki kelimenin son hecesi" bilgileri gösterilir.
    """
    aranan_kelime = self.input_word.text.lower()
    son_hece = self.input_hece.text.lower() if self.input_hece.text else None

    with open("şiir ", "r", encoding="utf-8") as file:
        cumleler = file.readlines()

    results = []
    for cumle in cumleler:
        eslesmeler = kelime_bulma_tum(cumle, aranan_kelime, son_hece)
        if eslesmeler:
            for i, (onceki, kelime, sonraki, son_hece_bulunan) in enumerate(eslesmeler, start=1):
                results.append(f"Cümle: {cumle.strip()}")
                results.append(f"Eşleşme {i}:")
                results.append(f"  Önceki Kelime: {onceki}")
                results.append(f"  Aranan Kelime: {kelime}")
                results.append(f"  Sonraki Kelime: {sonraki}")
                results.append(f"  Sonraki Kelimenin Son Hecesi: {son_hece_bulunan}")
            results.append("")
    self.show_results_page(results)


def calculate_diger(self, instance):
    """
        Kullanıcı tarafından girilen seçeneklere göre kelimeleri filtreler ve sonuçları gösterir.
        Bu seçenekler arasında kelime uzunluğu, son hece ve ünlü sayısı bulunur.

        Args:
            self: Uygulamanın mevcut durumu ve arayüz bileşenlerine erişimi sağlar.
            instance: Bu parametre, kivy'deki widget olaylarını temsil eder.

        Returns:
            None: Fonksiyon, filtrelenmiş kelimeleri yeni bir sayfada gösterir.

        Notes:
            - Kullanıcı, kelimenin son hecesini, uzunluğunu veya ünlü sayısını belirleyerek arama yapabilir.
            - Sonuçlar, tekrar eden kelimelerden arındırılır ve eşleşen kelimeler gösterilir.
    """
    vowels = {"a", "e", "ı", "i", "o", "ö", "u", "ü"}

    results = datafonksiyon.tum_kelimeler

    known = self.input_known.text.lower() if hasattr(self, "input_known") else ""
    if known:
        results = [
            w for w in results if w.endswith(known)
        ]
    if hasattr(self, "input_length") and self.input_length.text.isdigit():
        length = int(self.input_length.text)
        results = [
            w for w in results if len(w) == length
        ]
    if hasattr(self, "input_vowel_count") and self.input_vowel_count.text.isdigit():
        vowel_count = int(self.input_vowel_count.text)
        results = [
            w for w in results if sum(1 for char in w if char in vowels) == vowel_count
        ]

    # Tekrar eden kelimeleri kaldırma
    results = list(set(results))
    # Sonuçları yeni sayfada göstermek için çağır
    self.show_results_page(results)
