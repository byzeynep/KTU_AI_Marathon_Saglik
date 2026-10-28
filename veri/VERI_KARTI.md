# Sağlık v2 veri kartı

Kaynak: RSNA-STR 2018 / NIH ChestX-ray.
Çözünürlük: 256x256 gri tonlu PNG.
Sınıf 0: normal. Sınıf 1: pneumonia_like_opacity (pnömoniyle uyumlu opasite).

Eğitim: 11624 görüntü. Doğrulama: 2771 görüntü. Test: 2501 görüntü (etiketsiz).

Train ve val etiketleri yarışmacı paketindedir. Test görüntüleri pakettedir, test etiketleri organizatörde kalır. Organizatör teslim edilen modeli yeniden çalıştırarak test tahminlerini doğrular.

Aynı kaynak hastası yalnızca bir bölümdedir. Tam piksel kopyaları elendi. Test, RSNA içinden ayrılmış yeni bir hasta grubu holdout kümesidir; yeni eğitim kaynağına dış bir klinik veri seti değildir. Önceki PneumoniaMNIST kaynağı bu pakete karıştırılmadı.

Kaynak herkese açıktır; etiketlerin kaynaklardan bulunma riski tamamen ortadan kalkmaz. Kaynaktan etiket aramak yasaktır; organizatör modelleri yeniden çalıştırır ve kodu inceler.

Sayılar, sınıf dağılımı ve sınırlılıklar dataset_card.json içindedir. Lisans ve atıflar LICENSE_NOTICE.md içindedir.
