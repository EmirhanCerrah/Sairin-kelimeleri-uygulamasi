from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
import datafonksiyon  # Veri çekme fonksiyonunuzu çağırıyor
import calculations  # calculate_option1 ve calculate_option2 fonksiyonlarını içeriyor
import os

# Dosyadan veri yükleme
datafonksiyon.dosyadan_veri_cek("1M_ortadaki_kelimeler.txt")  # Dosya yolunu düzenleyin

def kelime_bulma_tum(cumle, aranan_kelime, son_hece=None):
    """
        Belirtilen bir cümlede, aranan kelimenin etrafındaki kelimeleri ve belirli bir son heceyi bulur.

        Args:
            cumle (str): İçinde arama yapılacak metin.
            aranan_kelime (str): Aranacak olan kelime.
            son_hece (str, optional): Aranan kelimenin sonrasındaki kelimenin son hecesi. Varsayılan değeri None'dur.

        Returns:
            list: Her eşleşme için (önceki kelime, bulunan kelime, sonraki kelime, sonraki kelimenin son hecesi) tuple'larını içeren bir liste.

        Notes:
            - Küçük/büyük harf duyarlılığı yoktur, yani aranan kelime ve metin karşılaştırılmadan önce her ikisi de küçük harfe dönüştürülür.
            - Eğer son_hece belirtilmemişse, sonraki kelimenin son iki harfi dikkate alınır.
            - Eğer cümlede aranan kelime bulunursa, etrafındaki kelimeler ve son hecesi döndürülür.
    """
    kelimeler = cumle.split()
    sonuc = []
    son_hece_uzunlugu = len(son_hece) if son_hece else 2  # Eğer son_hece belirtilmişse onun uzunluğu, yoksa varsayılan 2

    for index, kelime in enumerate(kelimeler):
        if kelime.lower() == aranan_kelime.lower():  # Küçük/büyük harf duyarlılığı kontrolü
            onceki_kelime = kelimeler[index - 1] if index > 0 else "Başlangıç yok"
            sonraki_kelime = kelimeler[index + 1] if index < len(kelimeler) - 1 else "Son yok"

            if sonraki_kelime != "Son yok":
                kelimenin_son_hecesi = sonraki_kelime[-son_hece_uzunlugu:]  # Girilen uzunluğa göre son harfleri al
                if son_hece is None or kelimenin_son_hecesi == son_hece:
                    sonuc.append((onceki_kelime, kelime, sonraki_kelime, kelimenin_son_hecesi))
    return sonuc


def show_popup_with_images(title="Popup Başlığı", message="Mesaj yok"):
    """
        Resimli bir popup penceresi gösterir. Popup içerisinde metin ve resimler yer alır.
        Kullanıcıya adım adım talimatlar verir.

        Args:
            title (str): Popup başlığı.
            message (str): Popup içerisinde gösterilecek ana mesaj.

        Returns:
            None: Fonksiyon, popup penceresini açmak için bir işlem başlatır.

        Notes:
            - Popup, içerisinde resim ve metin barındıran bir yapıdan oluşur.
            - Resimler ve metinler sırasıyla gösterilir.
            - Popup içerisinde "Kapat" butonu yer alır, bu butona basıldığında popup kapanır.
    """
    layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

    # Resimler ve metin için yatay bir BoxLayout
    image_layout = BoxLayout(orientation="horizontal", spacing=10)

    # Resim ve metinleri eklemek için liste
    images_and_texts = [
        ("ipucu1.png", "Yazdığın şiirden bir kelime seç."),
        ("sagyon.png", ""),
        ("secilen.png", "Seçtiğin kelimeden sonra gelecek olan kelimenin hangi eki almasını istiyorsan yaz."),
        ("sagyon.png", ""),
        ("diger.png", "Eğer sonuç çıkmazsa diğer adımlara bakabilirsin.")
    ]

    for image_file, text in images_and_texts:
        # Her bir resim ve metin için bir dikey BoxLayout
        item_layout = BoxLayout(orientation="vertical", spacing=5)

        # Resim - Daha büyük boyutlar için `size_hint` ve `size` değerlerini artırıyoruz
        img = Image(source=image_file, size_hint=(None, None), size=(240, 240))  # Resim boyutlarını artırdık
        item_layout.add_widget(img)

        # Metin
        label = Label(
            text=text,
            size_hint_y=None,
            height=180,
            text_size=(300, None),  # Metin boyutunu ayarlayın
            halign='left',  # Yatayda ortala
            valign='middle',  # Dikeyde ortala
            padding=(10, 10)  # Dolguları ayarlayın
        )  # Boyutları resme uygun hale getirdik
        item_layout.add_widget(label)

        # Resim ve metin layout'unu ana yatay layout'a ekle
        image_layout.add_widget(item_layout)

    # Ana layout'a mesajı ekle
    message_label = Label(text=message, size_hint_y=0.2, text_size=(600, None), halign='center')
    layout.add_widget(message_label)

    # Resimlerin eklendiği yatay düzeni ana layout'a ekleyin
    layout.add_widget(image_layout)

    # Kapat butonu
    close_button = Button(text="Kapat", size_hint=(1, 0.2))
    layout.add_widget(close_button)

    # Popup
    popup = Popup(title=title, content=layout, size_hint=(0.8, 0.6), auto_dismiss=False)
    close_button.bind(on_press=popup.dismiss)
    popup.open()



class MainScreen(BoxLayout):
    """
        Bu sınıf, ana ekranın yapısını tanımlar ve kullanıcı etkileşimlerine göre dinamik olarak
        çeşitli bileşenleri (butonlar, etiketler, giriş alanları) ekler. Kullanıcı yazılarını kaydeder,
        analizler yapar ve popup pencereleri gösterir. Ayrıca, farklı seçeneklerle metin analizi
        yapılmasına olanak tanır.

        Yöntemler:
            __init__: Ana ekranın başlatılmasını sağlar, bileşenleri yerleştirir.
            update_rect: Ekran boyutunda değişiklik olduğunda dikdörtgenin boyutlarını günceller.
            show_popup: İpuçları içeren bir popup penceresi gösterir.
            save_text: Kullanıcının girdiği metni kaydeder ve dosyaya yazar.
            load_text: Önceden kaydedilen metni yükler.
            go_back: Ana ekrana geri dönmek için ekranı temizler ve yeniden başlatır.
            show_option1: Kelime filtreleme seçeneklerini gösterir.
            show_option2: Kelime ve kafiye analizine dair seçenekleri gösterir.
        """
    def __init__(self, **kwargs):
        """
                MainScreen sınıfının başlatılmasını sağlar ve gerekli bileşenleri ekler.
                Ayrıca ekranda gösterilecek içerik, yazı ve butonların yerleştirilmesini sağlar.

                Args:
                    **kwargs: Ana ekranı özelleştirmek için ek parametreler.
                """
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 20

        with self.canvas.before:
            Color(1, 0.992, 0.816, 1)  # Krem rengi (RGBA formatında)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Metni saklamak için bir değişken
        self.saved_text = ""

        # Başlık
        self.add_widget(Label(text="Şiirsel Dokunuş", font_size=50, size_hint=(1, None), height=60, color=(0, 0, 0, 1)))

        # Metin alanı ve kaydetme butonu
        self.text_input = TextInput(
            hint_text="Yazınızı buraya yazın...",
            multiline=True,
            size_hint=(1, 2)
        )
        self.text_input.bind(text=self.save_text)
        self.text_input.bind(on_touch_up=self.on_text_select)
        self.add_widget(self.text_input)

        # Durum mesajı için etiket
        self.label_instruction = Label(text="", font_size=30)
        self.add_widget(self.label_instruction)

        # Butonlar
        self.button_option1 = Button(
            text="Kelime Filtreleme Seçenekleri",
            size_hint=(1, 0.25),
            height=80,
            font_size=50,
            background_color=(1, 1, 1, 1),  # Beyaz
            color=(1, 1, 1, 1),  # Yazı rengi
            on_press=self.show_option1
        )
        self.add_widget(self.button_option1)

        self.button_option2 = Button(
            text="Kelime ve Kafiye Analizi",
            size_hint=(1, 0.25),
            height=80,
            font_size=50,
            background_color=(1, 1, 1, 1),  # Beyaz
            color=(1, 1, 1, 1),  # Yazı rengi
            on_press=self.show_option2
        )
        self.add_widget(self.button_option2)

        # Dinamik içerik için placeholder
        self.dynamic_widgets = BoxLayout(orientation="vertical", spacing=10, size_hint=(1, 1))
        self.add_widget(self.dynamic_widgets)

        # Örnek bir popup düğmesi
        popup_button = Button(
            text="İPUCU AL (?)",
            size_hint=(1, 0.2),
            font_size=30,
            background_color=(0.5, 0.7, 0.9, 0.5)
        )
        popup_button.bind(on_press=lambda x: self.show_popup(message="Şiirinizi yazarken kafiye bulmada zorlanıyorsanız"
                                                                     " alttaki adımları izleyerek işinizi "
                                                                     "kolaylaştırabilirsiniz."))
        self.add_widget(popup_button)

        # Uygulama yüklenirken metni geri yükleme
        self.load_text()
    def update_rect(self, *args):
        """
                Ekranın boyutunda bir değişiklik olduğunda dikdörtgenin boyutlarını ve konumunu günceller.

                Args:
                    *args: Boyut değişikliği ile ilgili parametreler.
                """
        self.rect.size = self.size
        self.rect.pos = self.pos

    def show_popup(self, title="İPUCU", message="Popup mesajı"):
        """
               Kullanıcıya ipucu veya mesaj içeren bir popup penceresi gösterir.

               Args:
                   title (str): Popup başlığı (varsayılan: "İPUCU").
                   message (str): Popup mesajı (varsayılan: "Popup mesajı").
               """
        show_popup_with_images(title=title, message=message)
    def save_text(self, instance, value):
        """
                Kullanıcının girdiği metni kaydeder ve dosyaya yazar. Ayrıca, kaydedildiğine dair bir mesaj gösterir.

                Args:
                    instance: TextInput örneği.
                    value (str): Kullanıcının girdiği metin.
                """
        self.saved_text = self.text_input.text
        with open("user_text.txt", "w", encoding="utf-8") as file:
            file.write(self.saved_text)
        self.label_instruction.text = "[color=ff3333][size=40]Yazınız otomatik olarak kaydoluyor![/size][/color]"
        self.label_instruction.markup = True  # Markup'u etkinleştir

    # Durum mesajını güncelle

    def load_text(self):
        """
                Daha önce kaydedilen metni yükler ve TextInput alanına yerleştirir.
                Eğer dosya mevcut değilse, metin alanı boş olur.
                """
        if os.path.exists("user_text.txt"):
            with open("user_text.txt", "r", encoding="utf-8") as file:
                self.saved_text = file.read()
                self.text_input.text = self.saved_text
        else:
            self.saved_text = ""
            self.text_input.text = ""

    def go_back(self, instance):
        """
        Ekranı temizler ve ana ekrana geri dönmek için yeniden başlatır.

        Args:
            instance: Buton örneği.
        """
        self.clear_widgets()
        self.__init__()

    def show_option1(self, instance):
        """
        Kullanıcıya kelime filtreleme seçeneklerini sunan arayüzü gösterir.

        Args:
            instance: Buton örneği.
        """
        self.saved_text = self.text_input.text
        self.clear_widgets()
        self.add_widget(Label(text="Kelime Filtreleme Seçenekleri", font_size=50, size_hint=(1, None), height=60, color=(0.2, 0.6, 0.8, 1)))

        self.label_instruction = Label(
            text="Kelimenin tüm harflerini yazacaksan 'evet', boyut ve çeşit için 'hayır', diğer için 'diğer':",
            font_size=30,
            size_hint=(1, None),
            height=40,
            color=(0, 0, 0, 1),
        )
        self.add_widget(self.label_instruction)

        self.spinner_choice = Spinner(
            text='Seçiminizi yapın',
            values=('evet', 'hayır', 'diğer'),
            size_hint=(1, None),
            height=60,
            font_size=30
        )
        self.add_widget(self.spinner_choice)

        self.label_description = Label(
            text="Seçim yaparak istediğiniz işlemi gerçekleştirebilirsiniz.",
            font_size=30,
            size_hint=(1, None),
            height=40,
            color=(0, 0, 0, 1),
        )
        self.add_widget(self.label_description)

        self.button_submit = Button(
            text="Gönder",
            size_hint=(1, None),
            height=60,
            font_size=30,
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.8, 1),
            on_press=self.show_inputs_option1,
        )
        self.add_widget(self.button_submit)

        self.button_back = Button(
            text="Geri",
            size_hint=(1, None),
            height=60,
            font_size=30,
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.8, 1),
            on_press=self.go_back,
        )
        self.add_widget(self.button_back)
        self.dynamic_widgets = BoxLayout(orientation="vertical", spacing=10, size_hint=(1, 1))
        self.add_widget(self.dynamic_widgets) #ekledim ve Kelime Filtreleme butonu sonucunda açılan seçeneklerin işlem kısmı gözükür oldu.

    def show_option2(self, instance):
        """
        Kullanıcıya kelime ve kafiye analizi seçeneklerini gösterir. Seçilen metin üzerinde analiz
        yapmak için ilgili giriş alanları ve butonlar sunar.

        Args:
            instance: Buton örneği.
        """
        selected_text = self.text_input.selection_text
        if selected_text:
            self.ask_for_suffix(selected_text)
        else:
            self.saved_text = self.text_input.text
            self.clear_widgets()
            self.add_widget(Label(text="Kelime ve Kafiye Analizi", font_size=50, size_hint=(1, None), height=60, color=(0.2, 0.6, 0.8, 1)))

            self.add_widget(Label(text="Bulmak istediğiniz kelimenin öncesindeki kelimeyi giriniz :", font_size=30, color=(0, 0, 0, 1)))
            self.input_word = TextInput(multiline=False, font_size=30)
            self.add_widget(self.input_word)

            self.add_widget(Label(text="Bulmak istediğiniz kelimenin son hecesi nasıl olsun ? (örn: 'en') veya boş bırakın:", font_size=30, color=(0, 0, 0, 1)))
            self.input_hece = TextInput(multiline=False, font_size=30)
            self.add_widget(self.input_hece)

            self.button_calculate_option2 = Button(
                text="Analizi Yap",
                size_hint=(1, None),
                height=60,
                font_size=30,
                background_color=(1, 1, 1, 1),
                color=(0.2, 0.6, 0.8, 1),
                on_press=self.calculate_option2,
            )
            self.add_widget(self.button_calculate_option2)

            self.button_back = Button(
                text="Geri",
                size_hint=(1, None),
                height=60,
                font_size=30,
                background_color=(1, 1, 1, 1),
                color=(0.2, 0.6, 0.8, 1),
                on_press=self.go_back,
            )
            self.add_widget(self.button_back)

    def show_inputs_option1(self, instance):
        """
            Kullanıcının belirlediği tercihe göre dinamik input widget'ları oluşturur ve ekranın
            uygun bölümüne ekler.

            Bu fonksiyon, spinner_choice üzerinden kullanıcı tercihini kontrol eder ve buna
            göre bir dizi input widget'ı (TextInput ve Label) ekler. Seçilen tercihe göre
            kullanıcıdan farklı bilgilerin girilmesi istenir.

            Args:
                instance: Kivy widget instance'ı. Bu fonksiyon bir event handler olarak
            kullanılır, ancak burada doğrudan kullanılmaz.
        """
        self.dynamic_widgets.clear_widgets()

        choice = self.spinner_choice.text.lower()

        if choice == "evet":
            self.dynamic_widgets.add_widget(Label(text="Tüm harfleri girin:", font_size=30, color=(0, 0, 0, 1)))
            self.input_word = TextInput(multiline=False, font_size=30)
            self.dynamic_widgets.add_widget(self.input_word)

        elif choice == "hayır":
            self.dynamic_widgets.add_widget(Label(text="Harf çeşitlerini girin:", font_size=30, color=(0, 0, 0, 1)))
            self.input_word = TextInput(multiline=False, font_size=30)
            self.dynamic_widgets.add_widget(self.input_word)

            self.dynamic_widgets.add_widget(Label(text="Harf sayısını girin:", font_size=30, color=(0, 0, 0, 1)))
            self.input_length = TextInput(multiline=False, font_size=30)
            self.dynamic_widgets.add_widget(self.input_length)

        elif choice == "diğer":
            self.dynamic_widgets.add_widget(Label(text="Sondan bilinen harfleri yaz (örn: lı):", font_size=30, color=(0, 0, 0, 1)))
            self.input_known = TextInput(multiline=False, font_size=30)
            self.dynamic_widgets.add_widget(self.input_known)

            self.dynamic_widgets.add_widget(Label(text="Kelimenin toplam uzunluğunu yaz:", font_size=30, color=(0, 0, 0, 1)))
            self.input_length = TextInput(multiline=False, font_size=30)
            self.dynamic_widgets.add_widget(self.input_length)

            self.dynamic_widgets.add_widget(Label(text="İstenilen sesli harf sayısını yaz:", font_size=30, color=(0, 0, 0, 1)))
            self.input_vowel_count = TextInput(multiline=False, font_size=30)
            self.dynamic_widgets.add_widget(self.input_vowel_count)

        self.button_calculate_option1 = Button(
            text="Hesapla",
            size_hint=(1, None),
            height=100,
            font_size=30,
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.8, 1),
            on_press=self.calculate_option1,
        )
        self.dynamic_widgets.add_widget(self.button_calculate_option1)

    def calculate_option1(self, instance):
        """
        calculate_option1 fonksiyonu, başka bir modülde tanımlı olan
        `calculate_option1` fonksiyonunu çağırır. Parametre olarak
        aldığı `instance` nesnesini bu fonksiyona ileterek işlevi çalıştırır.

        Args:
        instance: Fonksiyona parametre olarak iletilen nesne.
        """

        calculations.calculate_option1(self, instance)

    def calculate_option2(self, instance):
        """
        Kullanıcıdan alınan kelime ve son hece bilgisi ile, 'siirler.txt' dosyasındaki
        cümleleri analiz eder. Eşleşen kelimeleri ve cümleleri benzersiz şekilde
        bulur ve sonuçları gösterir.

        Args:
        instance: Fonksiyona parametre olarak iletilen nesne.
        """

        aranan_kelime = self.input_word.text.lower()
        self.son_hece = self.input_hece.text.lower() if self.input_hece.text else None
        # aranan_kelime = selected_text.lower()

        with open("siirler.txt", "r", encoding="utf-8") as file:
            cumleler = file.readlines()

        results = set()  # Benzersiz sonuçlar için set kullanıyoruz
        for cumle in cumleler:
            eslesmeler = kelime_bulma_tum(cumle, aranan_kelime, self.son_hece)

            if eslesmeler:
                for onceki, kelime, sonraki, son_hece_bulunan in eslesmeler:
                    result_str = (f"{sonraki}")
                    results.add(result_str)
        results = list(results)
        self.show_results_page(results)


    def on_text_select(self, instance, touch):

        """
        Kullanıcı metni seçtiğinde bu fonksiyon tetiklenir. Seçilen metni alır
        ve `ask_for_suffix` fonksiyonunu çağırarak, sonrasında gelen kelimenin
        son hecesini girmesini ister.

        Args:
        instance: Metni içeren widget.
        touch: Kullanıcının dokunma hareketini içeren nesne.
        """

        if instance.collide_point(*touch.pos):
            selected_text = instance.selection_text
            if selected_text:
                self.ask_for_suffix(selected_text)

    def ask_for_suffix(self, selected_text):
        """
        Kullanıcının seçtiği kelimenin sonrasındaki heceyi girmesini isteyen
        bir arayüz oluşturur. Giriş kutusu ile alınan hece ile birlikte
        `run_analysis` fonksiyonu çağrılır.

        Args:
        selected_text: Kullanıcı tarafından seçilen kelime.
        """

        self.clear_widgets()
        self.add_widget(Label(text=f"Seçilen kelime: {selected_text}", font_size=50, size_hint=(1, None), height=60, color=(0.2, 0.6, 0.8, 1)))
        self.add_widget(
            Label(text="Sonrasında gelen kelimenin son hecesini girin (örn: 'en') veya boş bırakın:", font_size=30, color=(0, 0, 0, 1)))
        self.input_hece = TextInput(multiline=False, font_size=30)
        self.add_widget(self.input_hece)
        self.button_submit_suffix = Button(
            text="Tamam",
            size_hint=(1, None),
            height=60,
            font_size=30,
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.8, 1),
            on_press=lambda instance: self.run_analysis(selected_text),
        )
        self.add_widget(self.button_submit_suffix)

    def run_analysis(self, selected_text):
        """
        Kullanıcının seçtiği kelimenin sonrasındaki heceyi alır ve `siirler.txt`
        dosyasındaki metinleri tarayarak bu kelimenin geçtiği cümleleri bulur.
        Benzersiz sonuçlar elde edilip sonuç sayfasında gösterilir.

        Args:
        selected_text: Kullanıcı tarafından seçilen kelime.
        """

        self.son_hece = self.input_hece.text.lower() if self.input_hece.text else None
        aranan_kelime = selected_text.lower()

        with open("siirler.txt", "r", encoding="utf-8") as file:
            cumleler = file.readlines()

        results = set()  # Benzersiz sonuçlar için set kullanıyoruz
        for cumle in cumleler:
            eslesmeler = kelime_bulma_tum(cumle, aranan_kelime, self.son_hece)

            if eslesmeler:
                for onceki, kelime, sonraki, son_hece_bulunan in eslesmeler:
                    result_str = (f"{sonraki}")
                    results.add(result_str)

        unique_results = list(results)  # Benzersiz sonuçları listeye çeviriyoruz
        self.show_results_page(unique_results)

    def show_results_page(self, results):
        """
        Hesaplanan sonuçları kullanıcıya gösteren bir sayfa oluşturur. Eğer
        sonuçlar bulunmazsa alternatif seçenekler ve butonlar gösterilir.

        Args:
        results: Elde edilen analiz sonuçları.

        """

        self.clear_widgets()
        self.add_widget(Label(text="Sonuçlar", font_size=50, size_hint=(1, None), height=60, color=(0.2, 0.6, 0.8, 1)))

        result_window = ScrollView(size_hint=(1, 1))  # ScrollView burada kullanılıyor
        result_layout = BoxLayout(orientation="vertical", spacing=15, size_hint_y=None)
        result_layout.bind(minimum_height=result_layout.setter("height"))

        if results:
            for res in results:
                label = Label(
                    text=res,
                    size_hint_y=None,
                    height=50,
                    font_size=40,
                    halign="center",
                    valign="middle",
                    text_size=(self.width, None),
                    color=(0, 0, 0, 1)
                )
                label.bind(size=label.setter("text_size"))
                result_layout.add_widget(label)
        else:
            result_layout.add_widget(
                Label(
                    text="Belirttiğiniz kriterlere uygun sonuç bulunamadı. Şunları yapabilirsini:",
                    size_hint_y=None,
                    height=50,
                    font_size=30,
                    halign="center",
                    valign="middle",
                    text_size=(self.width, None),
                    color=(0, 0, 0, 1)
                )
            )

            # Diğer Güçlü Sonuçlar Butonu
            strong_results_button = Button(
                text="Diğer Güçlü Sonuçlar",
                size_hint=(1, None),
                height=100,
                font_size=40,
                background_color=(1, 1, 1, 1),
                color=(0.2, 0.6, 0.8, 1),
                on_press=self.show_strong_results,
            )
            result_layout.add_widget(strong_results_button)

            # Zayıf Sonuçlar Butonu
            weak_results_button = Button(
                text="Zayıf Sonuçlar",
                size_hint=(1, None),
                height=80,
                font_size=30,
                background_color=(1, 1, 1, 1),
                color=(0.2, 0.6, 0.8, 1),
                on_press=self.show_weak_results,
            )
            result_layout.add_widget(weak_results_button)

        result_window.add_widget(result_layout)
        self.add_widget(result_window)

        self.button_back = Button(
            text="Geri",
            size_hint=(1, None),
            height=60,
            font_size=30,
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.8, 1),
            on_press=self.go_back,
        )
        self.add_widget(self.button_back)

    def calculate_diger(self, instance):
        """
            Sesli harf sayısı ve bilinen son harflere göre kelimeleri filtreler.
            Sonuçları benzersiz bir şekilde bulur ve kullanıcıya gösterir.

            Args:
            instance: Fonksiyona parametre olarak iletilen nesne.
        """
        vowels = {"a", "e", "ı", "i", "o", "ö", "u", "ü"}  # Sesli harfler
        results = datafonksiyon.tum_kelimeler  # Datafonksiyon modülünden tüm kelimeler

        # Bilinen son harfleri filtrele
        known = self.input_known.text.lower()
        if known:
            results = [w for w in results if w.endswith(known)]

        # Sesli harf sayısı filtresi
        if self.input_vowel_count.text.isdigit():
            vowel_count = int(self.input_vowel_count.text)
            results = [w for w in results if sum(1 for char in w if char in vowels) == vowel_count]

        # Tekrar eden kelimeleri kaldırma
        results = list(set(results))

        # Sonuçları yeni sayfada göstermek için çağır
        self.show_results_page(results)

    def calculate_digerguclu(self, instance):
        """
            'siirler_kelimeler.txt' dosyasındaki kelimeleri okur, sesli harf sayısı
            ve bilinen son harflere göre filtreleme yapar. Sonuçları benzersiz bir
            şekilde bulur ve kullanıcıya gösterir.

            Args:
            instance: Fonksiyona parametre olarak iletilen nesne.
        """
        vowels = {"a", "e", "ı", "i", "o", "ö", "u", "ü"}  # Sesli harfler
        # siirlerkelimeler.txt dosyasını okuyarak verileri al
        # siirlerkelimeler.txt dosyasını okuyarak her satırdaki kelimeleri tek bir listeye al
        with open("siirler_kelimeler.txt", "r", encoding="utf-8") as file:
            results = [line.strip() for line in file]

        # Datafonksiyon modülünden tüm kelimeler

        # Bilinen son harfleri filtrele
        known = self.input_known.text.lower()
        if known:
            results = [w for w in results if w.endswith(known)]

        # Sesli harf sayısı filtresi
        if self.input_vowel_count.text.isdigit():
            vowel_count = int(self.input_vowel_count.text)
            results = [w for w in results if sum(1 for char in w if char in vowels) == vowel_count]

        # Tekrar eden kelimeleri kaldırma
        results = list(set(results))

        # Sonuçları yeni sayfada göstermek için çağır
        self.show_results_page(results)

    def show_strong_results(self, instance):
        """
            Güçlü sonuçları göstermek için bir sayfa oluşturur. Kullanıcıdan
            bilinen son harfleri ve sesli harf sayısını alarak filtreleme yapar.
            Sonuçlar güçlü bir analizle hesaplanır.

            Args:
                instance: Butona tıklama işlemi.
        """
        self.clear_widgets()

        # Dinamik içerik için placeholder
        self.dynamic_widgets = BoxLayout(orientation="vertical", spacing=10, size_hint=(1, 1))
        self.add_widget(self.dynamic_widgets)

        # "diğer" seçeneği için filtreleme işlemleri
        self.dynamic_widgets.add_widget(
            Label(text="Sondan bilinen harfleri yaz (örn: lı):", font_size=30, color=(0, 0, 0, 1)))
        self.input_known = TextInput(multiline=False, font_size=30, text=self.son_hece if self.son_hece else "")
        self.dynamic_widgets.add_widget(self.input_known)

        # son_hece değerini sıfırlayın
        self.son_hece = None

        self.dynamic_widgets.add_widget(
            Label(text="İstenilen sesli harf sayısını yaz:", font_size=30, color=(0, 0, 0, 1)))
        self.input_vowel_count = TextInput(multiline=False, font_size=30)
        self.dynamic_widgets.add_widget(self.input_vowel_count)

        self.button_calculate_diger = Button(
            text="Hesapla",
            size_hint=(1, None),
            height=100,
            font_size=30,
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.8, 1),
            on_press=self.calculate_digerguclu,  # calculate_diger fonksiyonunu çağırır
        )
        self.dynamic_widgets.add_widget(self.button_calculate_diger)

        self.button_back = Button(
            text="Geri",
            size_hint=(1, None),
            height=60,
            font_size=30,
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.8, 1),
            on_press=self.go_back,
        )
        self.add_widget(self.button_back)

    def show_weak_results(self, instance):
        """
            Zayıf sonuçları göstermek için bir sayfa oluşturur. Kullanıcıdan
            bilinen son harfleri ve sesli harf sayısını alarak filtreleme yapar.
            Sonuçlar zayıf bir analizle hesaplanır.

            Args:
                instance: Butona tıklama işlemi.
        """
        self.clear_widgets()

        # Dinamik içerik için placeholder
        self.dynamic_widgets = BoxLayout(orientation="vertical", spacing=10, size_hint=(1, 1))
        self.add_widget(self.dynamic_widgets)

        # "diğer" seçeneği için filtreleme işlemleri
        self.dynamic_widgets.add_widget(
            Label(text="Sondan bilinen harfleri yaz (örn: lı):", font_size=30, color=(0, 0, 0, 1)))
        self.input_known = TextInput(multiline=False, font_size=30, text=self.son_hece if self.son_hece else "")
        self.dynamic_widgets.add_widget(self.input_known)

        # son_hece değerini sıfırlayın
        self.son_hece = None

        self.dynamic_widgets.add_widget(
            Label(text="İstenilen sesli harf sayısını yaz:", font_size=30, color=(0, 0, 0, 1)))
        self.input_vowel_count = TextInput(multiline=False, font_size=30)
        self.dynamic_widgets.add_widget(self.input_vowel_count)

        self.button_calculate_diger = Button(
            text="Hesapla",
            size_hint=(1, None),
            height=100,
            font_size=30,
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.8, 1),
            on_press=self.calculate_diger,  # calculate_diger fonksiyonunu çağırır
        )
        self.dynamic_widgets.add_widget(self.button_calculate_diger)

        self.button_back = Button(
            text="Geri",
            size_hint=(1, None),
            height=60,
            font_size=30,
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.8, 1),
            on_press=self.go_back,
        )
        self.add_widget(self.button_back)


class TxtUploadApp(MDApp):
    """
        TxtUploadApp, KivyMD framework'ü kullanılarak geliştirilmiş bir uygulama sınıfıdır.
        Bu sınıf, ana ekranı (`MainScreen`) yüklemek için `build` metodunu içerir.
        Uygulama, kullanıcıların metin dosyalarını yüklemeleri ve içerikleriyle etkileşimde bulunmalarını sağlayan bir GUI sunar.

        Methods:
            build: Ana ekranı oluşturur ve döndürür.
    """
    def build(self):
        return MainScreen()



if __name__ == "__main__":
    TxtUploadApp().run()
