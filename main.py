from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import base64

ekran = Tk()
ekran.title("Secret Notes")
ekran.minsize(width=350,height=680)
ekran.config(padx=40,pady=40)
def encode_make(anahtar, temizleme):
    encryption = []
    for i in range(len(temizleme)):
        anahtar_c = anahtar[i % len(anahtar)]
        encryption_c = chr((ord(temizleme[i]) + ord(anahtar_c)) % 256)
        encryption.append(encryption_c)
    return base64.urlsafe_b64encode("".join(encryption).encode()).decode()

def decode_make(anahtar, encryption):
    deccryption = []
    encryption = base64.urlsafe_b64decode(encryption).decode()
    for i in range(len(encryption)):
        anahtar_c = anahtar[i % len(anahtar)]
        deccryption_c = chr((256 + ord(encryption[i]) - ord(anahtar_c)) % 256)
        deccryption.append(deccryption_c)
    return "".join(deccryption)

def text_dosyasi_kaydetme():
    sifre = label3_entry.get()
    baslik= label1_entry.get()
    icerik = label2_text.get("1.0",END)

    if baslik == "" or icerik == "" or sifre == "":
        messagebox.showerror(title="Message",message="Please enter all info")
        return
    else:
        mesaj_encrypted = encode_make(sifre,icerik)
        try:
            with open("secretnotes.txt","a") as dosya:
                dosya.write(f"\n{baslik}\n")
                dosya.write(f"{mesaj_encrypted}\n")
                messagebox.showinfo(title="Mesaj",message="Tebrikler başarıyla kaydedildi.")
        except:
            messagebox.showerror(f"Error!")
        finally:
            label1_entry.delete(0,END)
            label2_text.delete("1.0",END)
            label3_entry.delete(0,END)

def sifre_cozme():
    sifre = label3_entry.get()
    icerik_sifrelenmis = label2_text.get("1.0", END)

    if len(sifre) == 0 or len(icerik_sifrelenmis) == 0:
        messagebox.showerror(title="Error",message="Please enter all info.")
    else:
        try:
            mesaj_decrypted = decode_make(sifre,icerik_sifrelenmis)
            label2_text.delete("1.0",END)
            label2_text.insert("1.0",mesaj_decrypted)
        except:
            messagebox.showwarning(title="Error!",message="Please enter encrypted text")

resim = ImageTk.PhotoImage(Image.open("topsecret.png"))

resim_ekleme=Label(image=resim, padx=30, pady=30)
resim_ekleme.pack()

label_1 = Label(text="Enter your title")
label_1.pack()
label_1.config(padx=10, pady=10, font=("Arial",12,"normal"))

label1_entry = Entry(width=35)
label1_entry.pack()

label_2 = Label(text="Enter your secret")
label_2.pack()
label_2.config(padx=10, pady=10, font=("Arial",12,"normal"))

label2_text = Text(width=35,height=18)
label2_text.pack()

label_3 = Label(text="Enter master key")
label_3.pack()
label_3.config(font=("Arial",12,"normal"))

label3_entry = Entry(width=35)
label3_entry.pack()

button1=Button(text="Save & Encrypt",command=text_dosyasi_kaydetme)
button1.config(padx=7,pady=7)
button1.pack()

button2 = Button(text="Decrypt",command=sifre_cozme)
button2.config(padx=7,pady=7)
button2.pack()

ekran.mainloop()

