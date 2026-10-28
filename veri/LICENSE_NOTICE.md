# RSNA-STR 2018 / NIH veri kaynağı ve kullanım koşulları

Bu paketin görüntüleri RSNA-STR Pneumonia Detection Challenge (2018) kaynağından türetilmiştir. NIH Clinical Center özgün görüntü sağlayıcısıdır.

Resmî indirme sayfası:
https://www.rsna.org/artificial-intelligence/ai-image-challenge/RSNA-Pneumonia-Detection-Challenge-2018

Özgün NIH indirme sayfası:
https://nihcc.app.box.com/v/ChestXray-NIHCC

Geçerli veri koşulları: Pneumonia Detection Challenge Terms of Use and Attribution.
https://www.rsna.org/-/media/files/rsna/education/ai-resources-and-training/ai-image-challenge/pneumonia-detection-challenge-terms-of-use-and-attribution.pdf?hash=03B32453B8646245DE131339F09282D1&rev=db1621c90e7d4814b070161153cc600b

Koşulların özeti: Veri akademik araştırma, eğitim ve belirtilen diğer amaçlarla kullanılabilir. Yeniden paylaşımda NIH ve RSNA bağlantıları, sağlayıcı bilgisi ve aşağıdaki yayın atıfları korunmalıdır. Veri öznesi kişileri teşhis etmeye veya onlarla iletişim kurmaya çalışmayın. Koşulların tamamı için resmî metin geçerlidir. Bu veri için CC BY veya MIT lisansı ilan etmiyoruz; yeni kodların lisansı ayrıdır.

Atıflar:
1. Xiaosong Wang, Yifan Peng, Le Lu, Zhiyong Lu, Mohammadhadi Bagheri, Ronald M. Summers. ChestX-ray8: Hospital-scale Chest X-ray Database and Benchmarks on Weakly-Supervised Classification and Localization of Common Thorax Diseases. IEEE CVPR, 2017, pp. 3462-3471.
2. George Shih, Carol C. Wu, Safwan S. Halabi ve diğerleri. Augmenting the National Institutes of Health Chest Radiograph Dataset with Expert Annotations of Possible Pneumonia. Radiology: Artificial Intelligence, 2019. https://doi.org/10.1148/ryai.2019180041

Dönüşüm: uint8 DICOM piksellerinden 256x256 gri tonlu PNG; varsa MONOCHROME1 ters çevirme; LANCZOS yeniden örnekleme. DICOM üstverileri PNG'ye taşınmadı. Tam piksel kopyaları ve aynı piksellere çelişen etiketler elendi. Bölümler NIH hasta kodu üzerinden ayrıldı. Yakın kopya ve klinik etiket denetimi yapılmadı.

Etiketler: Calculated grubundaki final görüntü etiketleri kullanıldı: Normal -> 0, Lung Opacity -> 1. No Lung Opacity / Not Normal sınıfı kullanılmadı. Bireysel okuyucuların veya Adjudication grubunun ham etiketleri final etiket yerine kullanılmadı.

Sınıf 1 kesin klinik zatürre tanısı değildir; pnömoniyle uyumlu opasiteyi temsil eder. Veriler çocuklarla sınırlı değildir. Proje eğitim/araştırma içindir; klinik doğrulama yapılmamıştır.
