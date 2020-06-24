import tkinter as tk #Arayüz için gereken kütüphane
from tkinter import filedialog as fd  # Bilgisayardan dosya açmak için filedialog tkinter kütüphanesinden alınır.
import azure.cognitiveservices.speech as speechsdk # Seslendirme işi azure kütüphanesi tarafından gerçekleşir.
import cv2  #Bu kütüphane görüntü işleme kütüphanesidir.
import pytesseract #Bu kütüphane fotoğrafı yazıya çevirmek için kullanılan kütüphanedir.
from PIL import Image, ImageTk #Bu kütüphane fotoğrafların görüntülenmesi, seçilmesi için kullanılır.

#Projedeki ilk aşamadaki iki tırnak içinde yazılmış program yoluna kurulan tesseract.exe dosyası projeye dahil edilir.
pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

#Bu fonksiyon bilgisayardan fotoğraf seçilmesini ve seçilen fotoğrafın görüntülenmesini sağlamak amacı ile yazılmıştır.
def ResimSecme(): # def fonksiyon demektir.
    global resim #resim değişkeninin global olmasının nedeni bu fonksiyon dışında başka yerlerde de kullanılması gerektiğindendir.
    resim = fd.askopenfilename(initialdir = "/",title="Fotoğraf Seç",filetypes = (("jpeg files","*.jpg"),("png files","*.png"))) #fd filedialog'un yukarıda atanan adıdır. askopenfilename() fonksiyonu ile dosya seçme kısmı açılıyor.
    yukle = Image.open(resim)  # Fotoğrafı açar
    kayit = ImageTk.PhotoImage(yukle)  # Fotoğrafı görüntülemek için kullanılır.
    yeni = tk.Toplevel()# Arayüzde ek(alt)pencere açmak için kullanılır.
    yeni.iconbitmap(r"icon.ico")#İkonu icon.ico yapar.

    yeni.geometry("800x800")  # Ek pencerenin boyutları belirlenir.
    yeni.resizable(width=False, height=False)
    #Ek pencerenin arka planına fotoğraf yükleme kısmı
    yukle1= Image.open(".img\\indir.png")
    kayit1 = ImageTk.PhotoImage(yukle1)
    img1 = tk.Label(yeni,image=kayit1)
    img1.image = kayit1
    img1.place(x=0, y=0)  # Fotoğrafın arayüzdeki konumu belirlendi.
    #Seçilen fotoğrafın ek pencerede gösterilme kısmı

    img = tk.Label(yeni,image=kayit)  # Fotoğrafı arayüze yerleştirir.
    img.image = kayit  # Tip dönüşümü yapılır.
    img.place(x=50, y=50)  # Açılan fotoğrafın arayüzdeki konumunu belirtir.
     #Ek pencerede buton oluşturma
    B1 = tk.Button(yeni, text="Fotoğrafı Seslendir", command=Donustur, width="220", height="80", image=image,
                   compound=tk.CENTER, borderwidth=8)
    B1.config(font=(
    "Comic Sans MS", 15, "bold"))  # Oluşturulan butonun içindeki yazının boyutu, tipi ve kalınlığı belirlendi.
    B1.place(x=380, y=500)  # Butonun arayüzdeki konumu belirlendi.
    #Ek penceredeki ikinci buton
    B2 = tk.Button(yeni, text="Fotoğrafın \n Threshold Hali", command=Threshold, width="220", height="80", image=image,
                   compound=tk.CENTER, borderwidth=8)
    B2.config(font=(
        "Comic Sans MS", 15, "bold"))
    B2.place(x=80, y=500)


def Donustur():

    img = cv2.imread(resim)#global olarak tanımlanan ve bilgisayardan açılan fotoğrafı görüntü işleme için okur.

    ret, thresh2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)#Bir fotoğrafın yazıya çevrilmesi için o fotoğrafın siyah beyaz resme dönüştürülmesi
                                                                      #gerekir. Bu kısım fotoğrafın siyah beyaza çevrilmesini sağlar.
    cv2.imwrite('.img\\temizlenmisResim.png', thresh2) #Siyah beyaza çevrilen fotoğrafı temizlenmisResim.png şeklinde kaydeder.
    metin = pytesseract.image_to_string(Image.open('.img\\temizlenmisResim.png'), lang='tur') #Tesseract'ın kendine ait fonksiyonu ile siyah beyaza çevrilmiş resim
                                                                                       #yazıya dönüştürülür.

    #Bu kısımlar dönüştürülen yazının bir metin dosyasına yazdırılmasını sağlamaktadır.
    with open(".img\\output.txt", mode="w") as file: #yazma modunda output.txt adında bir txt dosyası açılır. Yazma modunda olması demek o txt dosyasının içine
                                               #çevrilen metnin yazılacağı anlamına gelmektedir.
            file.write(metin) #çevrilen metin write ile birlikte output.txt dosyasına yazılır.
            print("")# Boşluk

            print(metin)# Çevrilen metin python dosyasındaki konsol ekranında yazdırılır.

#Bu kısım çevrilen metnin seslendirme kısmıdır. Seslendirme için Azure'ın özel seslendirme teknolojisi kullanılmıştır.
#İlk başta Azure'dan metinden konuşmaya çevirme konusuyla ilgili kayıt yapılmış, bölge ve anahtar alınmıştır.
    anahtar, bolge = "9b5c37e79d784ddd8b55cc51f65eb0b5", "westus2" #Bu kısım o bölge ve anahtarın bir değişkene atandığı kısımdır.
    yapi= speechsdk.SpeechConfig(subscription=anahtar, region=bolge)#Anahtar ve bölge ile konuşmayı birleştirir.

    erisim = speechsdk.SpeechSynthesizer(speech_config=yapi)#Birleştirilen kısım erişim sağlamak amacıyla kullanılır.

    sonuc= erisim.speak_text_async(metin).get()#text değişkeni alınarak yapılandırma erişimi sayesinde metin sese dönüştürülür.

    if sonuc== speechsdk.ResultReason.SynthesizingAudioCompleted: #Konuşmanın bitip bitmediğini kontrol eder.

        print("Metin seslendirme [{}]".format(metin))#Konuşma bittiyse python konsolunda yazılır.


    elif sonuc== speechsdk.ResultReason.Canceled: #Konuşma bir sebepten iptal olduysa
        detay = sonuc.detay
        print("Konuşma iptali: {}".format(detay)) #Konuşma iptalinin nedeni yazılır.
    if detay == speechsdk.CancellationReason.Error: #Konuşmayla ilgili bir hata varsa
        #Hata detaylarını görüntüleme kısmı
        if detay.error_details:
            print("Hata detayları: {}".format(detay.error_details))
            print("Bir anahtara sahip misin?")

    # </code>
def Threshold():
    yeni = tk.Toplevel()#İkinci ek pencere
    yeni.iconbitmap(r"icon.ico")

    yeni.geometry("800x800")  # Pencerenin boyutları belirlenir.
    yeni.resizable(width=False, height=False)
    img = cv2.imread(resim)  # global olarak tanımlanan ve bilgisayardan açılan fotoğrafı görüntü işleme için okur.

    ret, thresh2 = cv2.threshold(img, 127, 255,
                                 cv2.THRESH_BINARY_INV)  # Bir fotoğrafın yazıya çevrilmesi için o fotoğrafın siyah beyaz resme dönüştürülmesi
    # gerekir. Bu kısım fotoğrafın siyah beyaza çevrilmesini sağlar.
    cv2.imwrite('.img\\temizlenmisResim.png', thresh2)
    # İkinci ek pencereye arka plan ekleme
    yukle1 = Image.open(".img\\indir.png")
    kayit1 = ImageTk.PhotoImage(yukle1)
    img1 = tk.Label(yeni, image=kayit1)
    img1.image = kayit1
    img1.place(x=0, y=0)  # Fotoğrafın arayüzdeki konumu belirlendi.
    #temizlenmisResim.png dosyasının ikinci ek pencerede gösterilmesi
    yukle = Image.open(".img\\temizlenmisResim.png")
    kayit = ImageTk.PhotoImage(yukle)
    img = tk.Label(yeni,image=kayit)
    img.image = kayit
    img.place(x=50, y=50)  # Fotoğrafın arayüzdeki konumu belirlendi.

def Hakkinda():
    yeni = tk.Toplevel()#Üçüncü ek pencere
    #Üçüncü ek pencereye arka plan ekleme
    yeni.iconbitmap(r"icon.ico")
    yukle1 = Image.open(".img\\indir.png")
    kayit1 = ImageTk.PhotoImage(yukle1)
    img1 = tk.Label(yeni, image=kayit1)
    img1.image = kayit1
    img1.place(x=0, y=0)
    text1="Bu proje seçilen bir fotoğraftaki metnin yazıya dönüştürülüp seslendirilmesini içermektedir...\n"
    text= \
         "Proje Sivas Cumhuriyet Üniversitesi \n öğrencileri Dilara TOĞAÇAR ve Tuba ALAGÖZ tarafından,\n Dr.Öğr.Üyesi Fırat İSMAİLOĞLU" \
         " danışmanlığında 'Bitirme Projesi' adı altında gerçekleşmiştir.\n"


    yeni.geometry("700x300")  # Pencerenin boyutları belirlenir.
    yeni.resizable(width=False, height=False)
    #Üçüncü ek pencere label ekleme
    tk.Label(yeni,
             text=text1, font=("Helvetica", 10, "bold"),
             bd=1, bg="white", relief="solid", width=80, height=5).place(x=30, y=10)
    tk.Label(yeni,
                         text=text,font=("Helvetica",10,"bold"),
                         bd=1, bg="white", relief="solid", width=80, height=10).place(x=30,y=100)

#Bu kısım arayüz kısmıdır.
Pencere = tk.Tk() #Tkinter kütüphanesi Tk() fonksiyonu ile pencere yapılır.
Pencere.geometry("300x300") #Pencerenin boyutları belirlenir.
Pencere.resizable(width=False, height=False)#Pencerenin fare yardımı ile büyütülüp küçültülmesi engeller.
Pencere.iconbitmap(r"icon.ico")

Pencere.title("BİTİRME ÖDEVİ")#Pencerenin üst kısmına başlık eklenir.

#Arka plan fotoğraf ayarlanır.
yukle= Image.open(".img\\indir.png")
kayit = ImageTk.PhotoImage(yukle)
img = tk.Label(image=kayit)
img.image = kayit
img.place(x=0, y=0)# Fotoğrafın arayüzdeki konumu belirlendi.


image=tk.PhotoImage(file=".img\\1.gif")#1.butona fotoğraf yüklemek için 1.gif dosyası alındı.

image1=tk.PhotoImage(file=".img\\2.gif")#2.butona fotoğraf yüklemek için 2.gif dosyası alındı.

#Buton oluşturuldu.
B = tk.Button(Pencere, text = "Bir Fotoğraf Seç", command = ResimSecme, width="220", height="80", image=image1, compound=tk.CENTER,borderwidth=8)

B1 = tk.Button(Pencere, text = "Proje Hakkında", command = Hakkinda, width="220", height="80", image=image1, compound=tk.CENTER,borderwidth=8)
B.config(font=("Comic Sans MS",15,"bold"))#Oluşturulan butonun içindeki yazının boyutu, tipi ve kalınlığı belirlendi.

B.place(x = 25,y = 150)#Butonun arayüzdeki konumu belirlendi.
B1.config(font=("Comic Sans MS",15,"bold"))#Oluşturulan butonun içindeki yazının boyutu, tipi ve kalınlığı belirlendi.

B1.place(x=25,y=50)

tk.mainloop()#Arayüz döngüsünün sonu
