# Sairin-kelimeleri-uygulamasi
Bu uygulama şiir yazarken türkçe kelimeleri doğru bir biçimde kullanmaya yardım eder. Daha önce yazılmış olan şiirlerin cümlelerinde kelimelerin birbiriyle olan ilişkisine bakar. Ayrıca Türkçedeki neredeyse tüm kelimeleri içeren veritabanı sayesinde şiir kelimeleri dışında herhangi bir kelimenin içerdiği harfler, son hecesi, kelimenin uzunluğu gibi kelime özelliklerine göre arama yapmanıza olanak tanır.
Temelde güzel, sağlıklı bir şiir yazmanızı sağlamak için geliştirdim :)

Uygulamanın her adımında dinamik input widget’ları, görsel öğeler ve kullanıcı dostu arayüz ile eşsiz bir deneyim sunmayı hedefledim. Sonuçlar ise benzersiz bir şekilde kullanıcıya sunulur; güçlü ve zayıf sonuçlar arasındaki farklar görsel olarak vurgulanır.

## Bu projede yer alan özellikler:

-Dinamik ve Etkileşimli Arayüz: Kullanıcı tercihlerine göre değişen input alanları ve seçenekler.

-Güçlü Sonuçlar ve Zayıf Sonuçlar: Filtreleme işlemleri ile kullanıcının gereksinimlerine en uygun sonuçlar.

-Esnek ve Kullanıcı Dostu: Farklı kriterlere göre kullanıcıya esneklik sağlamak amacıyla geliştirilen fonksiyonlar.

-Veri Okuma ve Filtreleme: Dosya okuma işlemleriyle kelimeler arasındaki bağlantıları bulma ve analiz etme.

-Kullanıcı Seçimlerine Göre Özelleşmiş Çözümler 🌟

--Uygulamayı kullanırken, sadece kelimeleri değil, sesli harf sayısını, bilinen son harfleri ve kelime uzunluklarını da göz önünde bulundurabilirsiniz. Bu sayede, istediğiniz kriterlere uygun benzersiz sonuçlar elde etmek mümkün. Ayrıca, zayıf ve güçlü sonuçlar arasında geçiş yaparak, daha fazla seçenek ile analizlerinizi derinleştirebilirsiniz.

## Gereksinimler:

Proje çalıştırmak için aşağıdaki Python kütüphanelerine ihtiyaç duyulmaktadır:

#### Kütüphaneler
- Kivy: Kullanıcı arayüzü (UI) oluşturmak için kullanılır.
- KivyMD: Kivy tabanlı malzemeli tasarım bileşenleri sağlar.
- os: Dosya ve sistemle ilgili işlemler için kullanılır.
#### Diğer py dosyaları(Github'a Yüklendi)
- datafonksiyon: Veri çekme ve işleme için özelleştirilmiş fonksiyonlar içerir.
- calculations: Matematiksel ve mantıksal hesaplamalar için fonksiyonlar içerir.

## Kurulum:

Projeyi çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1-Python 3.x ve pip yüklü olduğundan emin olun.

2-Gerekli kütüphaneleri yüklemek için terminal veya komut satırına aşağıdaki komutu girin:
pip install kivy kivymd

3-Projeyi çalıştırmak için, projenin bulunduğu dizinde terminali açın ve şu komutu girin:
python main.py

Bu adımları takip ederek uygulamanızı başarıyla çalıştırabilirsiniz.



## Sonuç Sayfası 📑🔍
Sonuçlar sayfası, her kullanıcı etkileşiminin sonunda gösterilecektir. Eğer kriterlerinize uygun sonuç bulunmazsa, alternatif önerilerle diğer güçlü sonuçlar ve zayıf sonuçlar arasındaki farkları inceleyebilirsiniz. Sonuçlar şık bir şekilde düzenlenmiş olup, her biri kullanıcı dostu ve anlaşılır bir biçimde sunulmuştur.

Bu dinamik, görsel olarak zengin ve işlevsel uygulama ile kullanıcılar, kelimeler üzerinde derinlemesine analiz yapabilir ve kendi belirledikleri kritere göre özelleştirilmiş sonuçlar alabilirler.

## Veritabanı Hakkında
-1M_ortadaki_keliemeler.txt KAYNAK: https://wortschatz.uni-leipzig.de/en/download/Turkish

-siirler.txt dosyasını oluşturmak için vericekme_web.py klasöründen https://www.antoloji.com sitesi kullanılmıştır

## Kullanım
Arayüzde Şiirinizi yazabileceğiniz bir metin kutucuğu bulunur. Burada yazdığınız kelimeleri seçerek bu seçtiğiniz kelimeden sonra gelecek olan kelimeyi daha önce yazılmış şiirleri analiz ederek sizlere sunar. Bu kutucukta yazdıklarınız otomatikmen user_text.txt klasörüne kaydolur, uygulamayı yeniden başlatsanız bile silinmez. 

Metin kutucuğu haricinde Türkçede kelimeleri analiz etmenize yarayacak iki özellik de bulunuyor. Butoonlara tıklayarak özellikleri aktif edebiliyorsunuz. Bunlar ile Türkçede bulunan kelimeleri aramanızı kolaylaştırabilirsiniz.



https://github.com/user-attachments/assets/9169c4b4-853f-4ffe-9efb-2824cd5f7ea4



Basitçe seç ve bul örneğince alttaki görseli örnek veriyorum.

<img width="700" alt="Image" src="https://github.com/user-attachments/assets/ad1b11f3-f626-4345-93c6-3d25475cdf62" />
