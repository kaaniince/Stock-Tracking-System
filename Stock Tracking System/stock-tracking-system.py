import tkinter as tk
import dbm
import pickle
urunler_db = dbm.open("urunler.db","c")

class Urun():
    sayac = 0
    def __init__(self, kategori,isim, marka,tanim,stok,fiyat,link):
        self.marka = marka
        self.isim = isim
        self.fiyat = float(fiyat)
        self.link = link
        self.kategori=kategori
        self.stok = int(stok)
        self.tanim = tanim
        self.kimlik="{}".format(Urun.sayac)
        Urun.sayac+=1

class Stokcu():
    def __init__(self,parent):
        self.parent= parent
        self.urunler=[]
        self.listbox_elemanlar=["Yiyecek","İçecek","Giyim","Elektronik","Ev"]
        frame_1=tk.Frame(self.parent,relief=tk.GROOVE,border=10,width=200)
        frame_2=tk.Frame(self.parent,relief=tk.GROOVE,border=10,width=200)
        frame_1.pack(fill=tk.Y,expand=True)
        frame_2.pack(expand=True, fill=tk.X)

        self.init_urun(frame_1)
        self.kategori_listboxi()
        self.init_urun_listele(frame_2)



    def init_urun_listele(self,frame):
        self.listbox_urunler = tk.Listbox(frame)
        self.listbox_urunler.pack(side=tk.LEFT,expand=True, fill=tk.X)
        buton2=tk.Button(frame,command=self.sat_butonu,text="1 Adet Sat")
        buton2.pack(side=tk.LEFT)
        if len(urunler_db.items()) !=0:
            for u in urunler_db.items():
                self.listbox_urunler.insert(int(u[0].decode()),
                                           f" Kategori : {pickle.loads(u[1]).kategori} İsim:{pickle.loads(u[1]).isim} Marka:{pickle.loads(u[1]).marka} Tanım:{pickle.loads(u[1]).tanim} Fiyat:{pickle.loads(u[1]).fiyat},Stok:{pickle.loads(u[1]).stok}")

    def init_urun(self,frame):
        self.listbox_kategori = tk.Listbox(frame,exportselection=0)
        self.listbox_kategori.grid(row=0, column=0, sticky="e",rowspan=3)
        self.isim_var =tk.StringVar()
        self.frame1 = tk.Label(frame,padx=5, pady=5,text="İsim")
        self.entry1 = tk.Entry(frame,textvariable=self.isim_var)
        self.frame1.grid(row = 0, column = 1,sticky="n")
        self.entry1.grid(row=2, column=1,sticky="n",padx=10)

        self.marka_var =tk.StringVar()
        self.frame1 = tk.Label(frame,padx=5, pady=5,text="Marka")
        self.entry2 = tk.Entry(frame,textvariable=self.marka_var)
        self.frame1.grid(row = 0, column = 2,sticky="n")
        self.entry2.grid(row=2, column=2,sticky="n",padx=10)

        self.tanim_var = tk.StringVar()
        self.frame1 = tk.Label(frame, padx=5, pady=5, text="Tanım")
        self.entry3 = tk.Entry(frame, textvariable=self.tanim_var)
        self.frame1.grid(row=0, column=3, sticky="n")
        self.entry3.grid(row=2, column=3, sticky="n",padx=10)

        self.stok_var = tk.IntVar()
        self.frame1 = tk.Label(frame, padx=5, pady=5, text="Stok")
        self.entry4 = tk.Entry(frame, textvariable=self.stok_var)
        self.frame1.grid(row=0, column=4, sticky="n")
        self.entry4.grid(row=2, column=4, sticky="n",padx=10)

        self.fiyat_var = tk.DoubleVar()
        self.frame1 = tk.Label(frame, padx=5, pady=5, text="Fiyat")
        self.entry5 = tk.Entry(frame, textvariable=self.fiyat_var)
        self.frame1.grid(row=0, column=5, sticky="n")
        self.entry5.grid(row=2, column=5, sticky="n",padx=10)

        self.link_var = tk.StringVar()
        self.frame1 = tk.Label(frame, padx=5, pady=5, text="Link")
        self.entry6 = tk.Entry(frame, textvariable=self.link_var)
        self.frame1.grid(row=0, column=6, sticky="n")
        self.entry6.grid(row=2, column=6, sticky="n",padx=10)

        buton = tk.Button(frame,command=self.ekle_butonu,text="Ekle")
        buton.grid(row=1, column=9, sticky="n",rowspan=3,padx=20)


    def kategori_listboxi(self):
        for indeks,harcama in enumerate(self.listbox_elemanlar):
            self.listbox_kategori.insert(indeks,harcama)

    def ekle_butonu(self):
        try:
            self.db_kontrol()
            if self.entry1.get()=="" or self.entry2.get()==""or self.entry3.get()=="" or self.entry4.get()=="" or self.entry5.get()=="" or self.entry6.get()=="":
                print("Eklenmedi! Ürüne eksik veri girdiniz!")
            else:
                urun = Urun(self.listbox_kategori.get(self.listbox_kategori.curselection()),self.isim_var.get(),self.marka_var.get(),self.tanim_var.get(),self.stok_var.get(),self.fiyat_var.get(),self.link_var.get())
                self.urunler.append(urun)
                urunler_db[str(urun.kimlik)] = pickle.dumps(urun)
                self.entry1.delete(0, tk.END)
                self.entry2.delete(0, tk.END)
                self.entry3.delete(0, tk.END)
                self.entry4.delete(0, tk.END)
                self.entry5.delete(0, tk.END)
                self.entry6.delete(0, tk.END)
            if self.listbox_urunler.size() !=0:
                self.listbox_urunler.delete(0, tk.END)
            self.dbyi_listboxa_aktar()
        except tk.TclError:
            print("Eklenemedi! Kategori seçiniz!")

    def db_kontrol(self):
        if len(urunler_db.items()) != 0 and len(self.urunler) == 0:
            for item in urunler_db.items():
                self.urunler.append(
                    Urun(pickle.loads(item[1]).kategori, pickle.loads(item[1]).isim, pickle.loads(item[1]).marka,
                         pickle.loads(item[1]).tanim,
                         pickle.loads(item[1]).stok, pickle.loads(item[1]).fiyat, pickle.loads(item[1]).link))
    def dbyi_listboxa_aktar(self):
        for u in urunler_db.items():
            self.listbox_urunler.insert(int(u[0].decode()),
                                       f" Kategori : {pickle.loads(u[1]).kategori} İsim:{pickle.loads(u[1]).isim} Marka:{pickle.loads(u[1]).marka} Tanım : {pickle.loads(u[1]).tanim} Fiyat:{pickle.loads(u[1]).fiyat} Stok:{pickle.loads(u[1]).stok}")

    def sat_butonu(self):
        try:
            secili_urun=pickle.loads(urunler_db[str(self.listbox_urunler.curselection()[0])])
            if secili_urun.stok>0:
                secili_urun.stok-=1
            else:
                print("Stok yetersiz!")
            urunler_db[str(self.listbox_urunler.curselection()[0])]=pickle.dumps(secili_urun)
            self.db_kontrol()
            self.listbox_urunler.delete(0, tk.END)
            self.dbyi_listboxa_aktar()
            for urun in self.urunler:
                if secili_urun.kimlik == urun.kimlik:
                    urun.stok=secili_urun.stok
        except IndexError:
            print("Silinecek ürünü seçiniz!")

root = tk.Tk()
app = Stokcu(root)
root.mainloop()
urunler_db.close()
