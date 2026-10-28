# Sağlıkta Yapay Zekâ proje ortamı (v2)

Göğüs röntgenlerini **normal (0)** ve **pnömoniyle uyumlu opasite (1)** olmak üzere iki sınıfa ayırın.

**Bu sürüm eski PneumoniaMNIST paketinin yerine geçer.** Eski veri, model, skor ve başlangıç değerleri (B) geçersizdir; eski paketle elde ettiğiniz sonuçları bu pakettekilerle karşılaştırmayın.

Bu klasör yalnızca bu tema (T01) içindir. Önce başlangıç modelini çalıştırın, ardından en az iki kontrollü deney ve bir özgün geliştirme yapıp sonuçlarını başlangıç modeliyle karşılaştırın.

## Veri ve görev

**Veri:** RSNA-STR Pneumonia Detection Challenge 2018 / NIH ChestX-ray · 256×256 piksel, gri tonlu göğüs röntgenleri · 11.624 train · 2.771 val · 2.501 test (etiketsiz)

| No | Sınıf | Anlamı | Görüntüde neye bakılır? |
|---|---|---|---|
| 0 | normal | Akciğerde opasite bulgusu yok | Akciğer alanları koyu ve temiz |
| 1 | pneumonia_like_opacity | Pnömoniyle uyumlu opasite | Akciğerde beyazımsı, bulanık yoğunlaşma alanları |

Sınıf 1 kesin klinik zatürre tanısı değildir. Veri çoğunlukla yetişkinlerden oluşur, çocuklarla sınırlı değildir. Aynı hastanın görüntüleri yalnızca bir bölümdedir (train, val veya test). Train'deki görüntülerin yaklaşık %41'i sınıf 1'dir.

**Zorunlu çıktılar**

- İki sınıfın olasılıkları ve sınıf tahmini
- Sınıf bazlı F1 değerleri
- **En az beş hatalı örneğin** görseli ve olası sebebiyle incelenmesi

**Geliştirme fikirleri** (birini seçip ölçün ya da kendi fikrinizi geliştirin)

- Konumsal bilgi kullanan öznitelikler veya küçük bir CNN
- Önceden eğitilmiş genel amaçlı bir model (ör. ImageNet)
- Olasılık kalibrasyonu (yalnızca val üzerinde)
- Parlaklık ve kontrast değişimine dayanıklılık
- Emin olunmayan tahminleri ayırıp kullanıcıya göstermek

**Sınırlar**

- Bu bir **araştırma ve eğitim prototipidir**. Klinik tanı, tedavi önerisi ve gerçek hasta üzerinde kullanım kapsam dışıdır.
- Modelin güven skoru klinik güvenilirlik anlamına gelmez.
- Bu tema, TEKNOFEST Sağlıkta Yapay Zekâ yarışmasının resmî görevlerinin eşdeğeri değildir; sağlıkta bilgisayarlı görü eğitim temasıdır.

## 1 Kurulum

**Python 3.12 gereklidir.** Önce `python3 --version` (Windows'ta `python --version`) ile kontrol edin. 3.12 değilse
python.org'dan Python 3.12 kurun ve aşağıdaki komutlarda `python` yerine `python3.12` kullanın. Mac'te hazır gelen
Python genellikle 3.9'dur ve paket kurulumu "No matching distribution found for numpy" hatası verir. GPU gerekmez.

Terminali bu klasörde açın. Windows için:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r baslangic_kodu/requirements.txt
```

Mac/Linux: komutlarda `.venv/bin/python` kullanın.

## 2 İlk modeli çalıştırın

```powershell
.venv\Scripts\python baslangic_kodu/train.py --data veri --output calismalar/model --seed 20261023
.venv\Scripts\python baslangic_kodu/predict.py --data veri --model calismalar/model/model.npz --split val --output calismalar/predictions_val.csv
.venv\Scripts\python baslangic_kodu/evaluate.py --truth veri/val.csv --predictions calismalar/predictions_val.csv --card veri/dataset_card.json
```

Başlangıç modeli bilerek çok basit tutulmuştur: görüntüden yalnızca **ortalama parlaklık ve parlaklığın standart sapmasını** çıkarır ve doğrusal bir sınıflandırıcı eğitir; akciğer yapısına bakmaz. Val macro-F1 değeri **0,669**'dur. Bu, veri setinde ulaşılabilecek en yüksek başarı değil, geliştirmeleriniz için düşük bir başlangıç çizgisidir.

Başarı ölçütünüz **macro-F1**: her sınıfın F1 değeri ayrı hesaplanır ve eşit ağırlıkla ortalanır; accuracy ile aynı şey değildir. Eğitimde train.csv, model seçimi ve karşılaştırmada val.csv kullanın.

## 3 Demoyu açın

```powershell
.venv\Scripts\python baslangic_kodu/demo.py --model referans_model/model.npz
```

Tarayıcıda http://127.0.0.1:8000 açın ve bir görüntü seçin. Kendi eğittiğiniz başlangıç modelini denemek için model yolunu `calismalar/model/model.npz` olarak değiştirin.

**Farklı bir model kullanıyorsanız:** `demo.py` ve `predict.py` yalnızca başlangıç modelinin `model.npz` biçimiyle çalışır. CNN, önceden eğitilmiş bir model veya başka bir yöntem kullanırsanız kendi demo ve tahmin kodunuzu hazırlamanız gerekir. Başlangıç demosunu örnek alabilirsiniz; bu kodlar teslimde `source/` içinde yer almalı ve çalıştırma komutları teslim README dosyasında yazmalıdır.

Çalışan bir demo teslimde zorunludur; yerel tarayıcı demosu yeterlidir, telefon uygulaması veya donanım gerekmez.

## 4 Son tahminleri üretin

Test görüntüleri `veri/images/` içinde, listesi `veri/test.csv` dosyasındadır; **test etiketleri pakette yoktur.** Son modelinizle test tahminlerini üretin:

```powershell
.venv\Scripts\python baslangic_kodu/predict.py --data veri --model calismalar/model/model.npz --split test --output calismalar/predictions.csv
```

Bu komut yalnızca başlangıç modeliyle (`model.npz`) çalışır. Farklı bir model kullanıyorsanız test tahminlerini üreten kendi kodunuzu yazın ve aynı predictions.csv biçimini üretin: `id,prediction,prob_0,prob_1,latency_ms,bytes`. Sınıf sırası: 0: normal; 1: pneumonia_like_opacity. Olasılıklar 0–1 arasında olmalı ve toplamları 1 olmalı; prediction en yüksek olasılıklı sınıfın numarasıdır. latency_ms görüntü başına çıkarım süresi, bytes giriş dosyasının boyutudur. Her test id'si bir kez bulunmalı, fazladan id olmamalı. Biçimi `evaluate.py` ile val tahminleri üzerinde kontrol edin.

## 5 Raporlar ve teslim

Şablonlar `sablonlar/` içindedir. Haftalık raporlar 1–2 sayfadır ve mentörler tarafından okunur: **25 Ekim 18.00** ve **31 Ekim 12.00**. Her biri o hafta yapılan işleri, deneyleri ve val sonuçlarını, sorunları, mentör desteğini, üye katkılarını ve sonraki adımları içerir. İki haftalık rapor da yarışmayı tamamlama koşuludur.

Nihai rapor **3–5 sayfa** (kaynakça hariç), sunum **en fazla 8 slayt** olmalıdır. Veri setini teslim paketine yeniden eklemeyin. Veri lisansı ve atıf bilgisi: `veri/LICENSE_NOTICE.md`. Model dosyası için önerilen sınır 1 GB'tır.

## 6 Program, puanlama ve kurallar

### Program

| Tarih | Ne var? |
|---|---|
| 19 Ekim Pazartesi | Etkinliğin başlangıcı |
| 25 Ekim Pazar | Rapor ve Git/GitHub eğitimi |
| 25 Ekim Pazar 18.00 | 1. haftalık rapor |
| 31 Ekim Cumartesi 12.00 | 2. haftalık rapor ve **nihai proje teslimi** |
| 31 Ekim, teslimden sonra | Organizatör model başarısını ölçer |
| 1 Kasım Pazar | Final: jüri bütün projeleri ve demoları inceler |

### Puanlama (100 puan)

| Kriter | Puan |
|---|---|
| Test başarısı: 15 × test macro-F1 (jüri modelinizi yeniden çalıştırarak ölçer) | 15 |
| Başlangıç modeline göre gelişme: 5 × (F − B) / (1 − B) | 5 |
| Deneyler ve hata analizi | 20 |
| Özgün katkı | 15 |
| Demo ve tekrarlanabilirlik | 10 |
| **Rapor:** nihai rapor ve iki haftalık rapor | **20** |
| **Sunum:** final sunumu ve soru-cevap | **15** |

F sizin, B başlangıç modelinin aynı test kümesindeki macro-F1 değeridir: **B = 0,652**. Gelişme puanı eksiye düşmez. Puanın yalnızca beşte biri skordan gelir; geri kalanı ne denediğinizi, nasıl ölçtüğünüzü ve bunu raporda ve sunumda ne kadar iyi açıkladığınızdan gelir.

### En az şunları yapın

- Başlangıç modelini çalıştırın ve val macro-F1 değerini kaydedin.
- **En az iki kontrollü deney** yapın: her deneyde yalnızca bir şeyi değiştirin ve val üzerinde karşılaştırın.
- Seçtiğiniz geliştirmeyi doğrulayan bir karşılaştırma yapın.
- Hatalı örnekleri inceleyin ve raporlayın.
- Aynı deneyi farklı tohumla tekrarlamak yeni deney veya özgün katkı sayılmaz. Başarıyı yalnızca accuracy ile açıklamayın; bütün sınıfların F1 değerlerini verin.

### Veri ve model kuralları

- Ana model **yalnızca bu paketteki train verisiyle** eğitilir. Dışarıdan veri kullanmak, özellikle **RSNA ve NIH kaynaklarından görüntü veya etiket indirmek yasaktır**; test görüntülerinin etiketleri de bu kaynaklarda bulunur.
- Genel amaçlı önceden eğitilmiş modeller (ör. ImageNet ile eğitilmiş) serbesttir. **RSNA, NIH ChestX-ray veya başka göğüs röntgeni verileriyle eğitilmiş hazır model ağırlıkları yasaktır.**
- Normalizasyon, dengeleme ve veri artırma gibi ayarları yalnızca train verisinden öğrenin. Model seçimi, eşik ve kalibrasyon yalnızca val ile yapılır. **Test üzerinde ayar yapılmaz**; test görüntüleri eğitime katılmaz.
- `dataset_card.json` içindeki test sınıf sayılarını eğitimde, eşik veya kalibrasyon ayarında kullanmak yasaktır.
- Test cevaplarını kaynaktan bulup kullanmak yasaktır. Organizatör modelinizi kontrollü ortamda çalıştırır ve kodunuzu inceler; bu yüzden eğitim kodunuz da `source/` içinde olmalıdır.
- Veri, kod ve model ağırlığı lisanslarını ayrı ayrı kaynak beyanına yazın. Veri kullanım koşulları için `veri/LICENSE_NOTICE.md` dosyasına bakın.

### Yapay zekâ araçları

Yapay zekâ yardımcıları, açık kaynak kod ve dokümantasyon kullanılabilir. Kaynak beyanında hangi aracı, ne amaçla, hangi dosyalarda kullandığınızı ve sonucu nasıl doğruladığınızı yazın. Takım ürettiği kodu açıklayabilmelidir. Kişisel veri, başka takımın kodu veya özel cevap anahtarı dış araçlara gönderilemez. Başka takımın çalışmasını kopyalamak ve kaynak belirtmeden hazır proje teslim etmek yasaktır.

### Haklar

Kodunuzun ve projenizin hakları sizde kalır. Kodu herkese açmak zorunlu değildir; jüri yalnızca değerlendirme için inceler.

## Teslim klasörü

Teslim klasörünüzün adı `BM_TAKIMKODU_T01` olmalıdır; `TAKIMKODU` yerine takımınızın adını boşluksuz ve Türkçe karakter kullanmadan yazın. Klasör şu dosyaları içermelidir:

```text
README.md              kurulum, tahmin üretme ve demo komutları
source/                eğitim ve çıkarım kodunuz
model/                 son model ağırlıklarınız
predictions.csv        test tahminleri
report.pdf             nihai rapor
slides.pdf             sunumun PDF kopyası
haftalik_rapor_1.pdf
haftalik_rapor_2.pdf
kaynak_beyani.md       veri, kod, model ve yapay zekâ aracı beyanı
```

Çalıştırma komutlarını teslim README dosyasında belirtin. Organizatör dosyalarınızı internet erişimi olmayan kontrollü bir ortamda çalıştırır; teslimden önce projenizi başka bir klasöre kopyalayıp README komutlarıyla `predictions.csv` dosyasını baştan üretmeyi deneyin.
