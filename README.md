# Association-Rule-Learning-Recommender

Sepet aşamasında kullanıcılara ürün önerisinde bulunmak.


Birliktelik kurallarından APRİORİ algortiması kullanılmıştır.Birliktelik kuramındaki 3 önemli kavram = "SUPPORT"," CONFİDENCE" VE "LİFT"

SUPPORT= a ve b ürünleri hangi sıklıkla beraber görüntülenir-->Support(a,b)=frequence(a,b)/N


CONFİDENCE=a ürününü alan bir müşterinin b ürününü alma ihtimali-->Confidence(a,b)=frequence(a,b)/frequence(a)



LiFT=müşteri a ürününü aldığında b ürününün satışı ne kadar artıyor.-->Lift(a,b)=support(a,b)/(support(a)*support(b))

 "Online Retail II" isimli veri setimiz İngiltere merkezli online bir satış mağazasının 01/12/2009 -09/12/2011 tarihleri arasındaki satışlarını içeriyor.
YIL=2010-1011
COUNTRY=Almanya  baz alınmıştır.


 Veri setimize ait değişkenler:

InvoiceNo–Fatura Numarası Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder.

StockCode–Ürün kodu Her bir ürün için eşsiz numara.

Description–Ürün ismi

InvoiceDate–Fatura tarihi

UnitPrice–Fatura fiyatı (Sterlin)

CustomerID–Eşsiz müşteri numarası

Country–Ülke ismi
