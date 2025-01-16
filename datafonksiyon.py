# datafonksiyon.py
n = []
tum_kelimeler = []

def dosyadan_veri_cek(dosya_adi):
    """
        Verilen dosya adından verileri okuyarak, dosyadaki tüm satırları küçük harfe dönüştürüp bir listeye kaydeder.
        Ayrıca, okunan verilerin bir kopyasını `tum_kelimeler` listesine de atar.

        Args:
            dosya_adi (str): Okunacak dosyanın adı.

        Returns:
            None: Fonksiyon, yalnızca veriyi dosyadan çeker ve küresel değişkenlere kaydeder.

        Raises:
            FileNotFoundError: Eğer belirtilen dosya bulunamazsa, bir hata mesajı basılır.

        Notes:
            - Dosyadaki her satır, baştaki ve sondaki boşluklardan arındırılır ve küçük harfe dönüştürülür.
            - Okunan veriler, küresel değişkenlere (`n` ve `tum_kelimeler`) kaydedilir.
    """
    global n, tum_kelimeler
    try:
        with open(dosya_adi, 'r', encoding='utf-8') as dosya:
            n = [satir.strip().lower() for satir in dosya.readlines()]
            tum_kelimeler = n.copy()  # n'nin bir kopyasını tum_kelimeler olarak kaydediyoruz
    except FileNotFoundError:
        print(f"{dosya_adi} bulunamadı. Lütfen doğru dosya adı belirtin.")
