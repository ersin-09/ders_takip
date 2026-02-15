import pandas as pd
import datetime
import json
import tkinter as tk
from tkinter import font as tkfont, messagebox, colorchooser, simpledialog
from tkinter import filedialog
import sys
import os
import platform
from pathlib import Path
import threading
import time

# ==============================
# 1. AYARLAR VE SABİTLER
# ==============================


# Mevcut çalışma dizinini belirle (Linux'ta .desktop dosyasından çalıştırıldığında önemli olabilir)
CWD = Path(__file__).parent.absolute()
VARSAYILAN_EXCEL_ADI = str(CWD / 'ders_saatleri.xlsx')

SAAT_FORMATI = "%H:%M:%S"


def uygulama_veri_dosya_yolu(dosya_adi):
    """Uygulama verileri için platforma uygun dizini oluşturup dosya yolunu döndürür."""
    try:
        if platform.system() == "Windows":
            base_dir = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        elif platform.system() == "Darwin":
            base_dir = Path.home() / "Library" / "Application Support"
        else:
            base_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

        app_dir = base_dir / "DersTakip"
        app_dir.mkdir(parents=True, exist_ok=True)
        return app_dir / dosya_adi
    except Exception:
        # Dizin oluşturulamazsa mevcut çalışma dizinini kullan
        return Path(dosya_adi)


APP_DATA_FILE = uygulama_veri_dosya_yolu('ders_takip_verileri.json')

# Önceki sürümlerde uygulama dizinine yazılan verileri yeni dizine taşı
ESKI_APP_DATA_FILE = Path('ders_takip_verileri.json')
if ESKI_APP_DATA_FILE.exists() and not APP_DATA_FILE.exists():
    try:
        APP_DATA_FILE.write_bytes(ESKI_APP_DATA_FILE.read_bytes())
    except Exception:
        pass

# Uygulama Varsayılan Ayarları
VARSAYILAN_AYARLAR = {
    'kritik_sure': 180, # Saniye (3 dakika)
    'sayaç_boyutu': 40, # Sayaç font boyutu
    'saat_araligi_boyutu': 12 # Başlangıç/Bitiş saati font boyutu
}

# Varsayılan arayüz renkleri
VARSAYILAN_RENK = {
    'arka_plan': '#252526',
    'alt_yazi': '#999999',
    'uyari_arka_plan': '#990000', # Kritik süre arka plan rengi
    'ders_baslik': '#004080',     
    'teneffus_baslik': '#006600', 
    'ders_sayac': '#00CCFF',      
    'teneffus_sayac': '#CCFF00'   
}

# ==============================
# 2. VERİ YÖNETİMİ VE YARDIMCI FONKSİYONLAR
# ==============================
def tum_verileri_yukle():
    """Tüm program verisini, uygulama ayarlarını ve renkleri tek dosyadan yükler."""
    try:
        with open(APP_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            program = data.get('program', None)
            
            # Ayarları yükle ve varsayılanlarla birleştir
            yuklenen_ayarlar = data.get('ayarlar', {}).copy()
            tamamlanmis_ayarlar = VARSAYILAN_AYARLAR.copy()
            tamamlanmis_ayarlar.update(yuklenen_ayarlar)
            
            # Renkleri yükle ve varsayılanlarla birleştir
            yuklenen_renkler = data.get('renkler', {}).copy() 
            tamamlanmis_renkler = VARSAYILAN_RENK.copy()
            tamamlanmis_renkler.update(yuklenen_renkler)
            
            return program, tamamlanmis_renkler, tamamlanmis_ayarlar
            
    except (FileNotFoundError, json.JSONDecodeError):
        # Dosya yoksa veya bozuksa varsayılanları döndür
        return None, VARSAYILAN_RENK, VARSAYILAN_AYARLAR

def tum_verileri_kaydet(program_verisi, renkler, ayarlar):
    """Tüm program verisini, uygulama ayarlarını ve renkleri tek dosyaya kaydeder."""
    data = {
        'program': program_verisi,
        'renkler': renkler,
        'ayarlar': ayarlar
    }
    try:
        APP_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(APP_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        messagebox.showerror("Kayıt Hatası", f"Veri kaydedilemedi: {e}")
        return False

def parse_time(time_str):
    """Farklı formatlardaki saat verisini dener (HH:MM:SS veya HH:MM)."""
    formats = ["%H:%M:%S", "%H:%M"]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(time_str, fmt).time()
        except ValueError:
            pass
    raise ValueError(f"Saat formatı geçersiz: {time_str}")

def excel_to_memory(dosya_yolu):
    """Belirtilen Excel dosyasından ders saatlerini okur ve listeye dönüştürür."""
    try:
        df = pd.read_excel(dosya_yolu, header=0, engine='openpyxl', dtype=str)
        if df.shape[1] < 3:
            raise ValueError("Excel dosyasında en az 3 sütun (Ders Adı, Başlangıç, Bitiş) olmalıdır.")
        df = df.iloc[:, 0:3]
        df.columns = ['Ad', 'Baslangic', 'Bitis']
        program = []
        for index, row in df.iterrows():
            baslangic_str = str(row['Baslangic']).strip()
            bitis_str = str(row['Bitis']).strip()
            
            # Eğer excel'den gelen veri "09:00:00" yerine "09:00" ise veya saniye yoksa düzelt
            # Ancak en temiz yol parse_time fonksiyonu kullanmak
            try:
                t_bas = parse_time(baslangic_str)
                t_bit = parse_time(bitis_str)
                
                # Standart formata çevirip (HH:MM:SS) kaydedelim ki hesaplamada sorun çıkmasın
                baslangic_str = t_bas.strftime(SAAT_FORMATI)
                bitis_str = t_bit.strftime(SAAT_FORMATI)
                
            except ValueError:
                 # Belki boş satırdır veya başlık tekrarıdır, geç
                 # Ancak hata verip kullanıcıyı uyarmak daha güvenli
                 if not baslangic_str or not bitis_str or baslangic_str.lower() == 'nan':
                     continue
                 raise ValueError(f"'{row['Ad']}' satırındaki saat verisi hatalı: {baslangic_str} - {bitis_str}")

            program.append({'Ad': str(row['Ad']), 'Baslangic': baslangic_str, 'Bitis': bitis_str})
        if not program:
             raise ValueError("Excel dosyasında ders verisi bulunamadı.")
        return program
    except Exception as e:
        messagebox.showerror("Hata", f"Veri yüklenemedi: {e}")
        return None

def kalan_süre_hesapla(program_str):
    """Mevcut duruma göre kalan süreyi hesaplar ve başlangıç/bitiş saatlerini döndürür."""
    program = []
    for ders in program_str:
        try:
            # Buradaki veriler artık standart formata (HH:MM:SS) çevrilmiş olmalı
            # Ama yine de parse_time kullanalım garanti olsun
            baslangic_time = parse_time(ders['Baslangic'])
            bitis_time = parse_time(ders['Bitis'])
            program.append({'Ad': ders['Ad'], 'Baslangic': baslangic_time, 'Bitis': bitis_time, 'Baslangic_Str': ders['Baslangic'], 'Bitis_Str': ders['Bitis']})
        except ValueError:
            continue
            
    simdi = datetime.datetime.now().time()
    bugun = datetime.datetime.now().date()
    simdi_dt = datetime.datetime.combine(bugun, simdi)
    
    for i in range(len(program)):
        ders = program[i]
        ders_baslangic_dt = datetime.datetime.combine(bugun, ders['Baslangic'])
        ders_bitis_dt = datetime.datetime.combine(bugun, ders['Bitis'])
        
        if ders_baslangic_dt <= simdi_dt < ders_bitis_dt:
            kalan = ders_bitis_dt - simdi_dt
            saniye = int(kalan.total_seconds())
            return {
                'Type': "DERS", 
                'Ad': ders['Ad'], 
                'Kalan_Saniye': saniye,
                'Baslangic_Str': ders['Baslangic_Str'], 
                'Bitis_Str': ders['Bitis_Str']          
            }
        
        if i < len(program) - 1:
            sonraki_ders = program[i+1]
            teneffus_baslangic_dt = ders_bitis_dt
            teneffus_bitis_dt = datetime.datetime.combine(bugun, sonraki_ders['Baslangic'])
            
            if teneffus_baslangic_dt <= simdi_dt < teneffus_bitis_dt:
                kalan = teneffus_bitis_dt - simdi_dt
                saniye = int(kalan.total_seconds())
                return {
                    'Type': "TENEFFÜS", 
                    'Ad': None, 
                    'Kalan_Saniye': saniye,
                    'Baslangic_Str': ders['Bitis_Str'],                 
                    'Bitis_Str': sonraki_ders['Baslangic_Str']          
                }

    # Eğer bir ders/teneffüs aralığında değilse
    bos_veri = {'Type': None, 'Ad': None, 'Kalan_Saniye': 0, 'Baslangic_Str': None, 'Bitis_Str': None}
    
    if len(program) > 0 and simdi >= program[-1]['Bitis']:
        bos_veri['Type'] = "GÜN SONU"
        return bos_veri
    
    if len(program) > 0 and simdi < program[0]['Baslangic']:
        bos_veri['Type'] = "GÜN BAŞLAMADI"
        return bos_veri
        
    return bos_veri


# ==============================
# 3. TKINTER ARAYÜZÜ VE GÜNCELLEME 
# ==============================

class DersTakipUygulamasi:
    def __init__(self, master):
        # Ayarları yükle:
        self.program_verisi, self.renkler, self.ayarlar = tum_verileri_yukle() 
        
        # Eğer kayıtlı veri yoksa ve varsayılan Excel dosyası mevcutsa, onu yüklemeyi dene
        if self.program_verisi is None:
            if os.path.exists(VARSAYILAN_EXCEL_ADI):
                print(f"Varsayılan Excel Dosyası Bulundu: {VARSAYILAN_EXCEL_ADI}")
                # Hata durumunda mesaj kutusu göstermemesi için try-except bloğuna alalım
                # excel_to_memory normalde messagebox gösteriyor, bu yüzden startup'ta 
                # kullanıcıyı hemen hatayla karşılamamak için dikkatli olmalıyız.
                # Ancak kullanıcı excel dosyasını koyduysa yüklenmesini bekler, hata varsa görmeli.
                self.program_verisi = excel_to_memory(VARSAYILAN_EXCEL_ADI)
                
                if self.program_verisi:
                    # Başarılı yükleme sonrası verileri kaydet
                    tum_verileri_kaydet(self.program_verisi, self.renkler, self.ayarlar)
        self.master = master
        self.guncelle_job = None 
        
        # --- Pencere Ayarları ---
        self.master.title("Ders Takip")
        self.master.attributes('-topmost', True) 
        self.master.resizable(False, False)
        self.master.configure(bg=self.renkler['arka_plan']) 

        # --- Font Ayarları ---
        # İşletim sistemine göre font ailesi seçimi
        if platform.system() == "Windows":
            baslik_font_family = "Segoe UI"
            sayac_font_family = "Consolas"
            saat_font_family = "Segoe UI"
        else:
            # Linux/Pardus için yaygın fontlar
            baslik_font_family = "DejaVu Sans"
            sayac_font_family = "DejaVu Sans Mono"
            saat_font_family = "DejaVu Sans"

        self.baslik_font = tkfont.Font(family=baslik_font_family, size=13, weight="normal")
        
        # Sayaç Fontu
        sayaç_boyutu = self.ayarlar.get('sayaç_boyutu', VARSAYILAN_AYARLAR['sayaç_boyutu'])
        self.sure_font = tkfont.Font(family=sayac_font_family, size=sayaç_boyutu, weight="bold")
        self.unlem_font = tkfont.Font(family=sayac_font_family, size=int(sayaç_boyutu * 0.6), weight="bold")
        
        # Saat Aralığı Fontu
        saat_araligi_boyutu = self.ayarlar.get('saat_araligi_boyutu', VARSAYILAN_AYARLAR['saat_araligi_boyutu'])
        self.saat_araligi_font = tkfont.Font(family=saat_font_family, size=saat_araligi_boyutu, weight="normal")
        
        # Diğer Fontlar
        self.info_font = tkfont.Font(family=baslik_font_family, size=9)


        # Ana konteyner
        self.main_frame = tk.Frame(master, bg=self.renkler['arka_plan'])
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        # 1. Durum Etiketi
        ilk_sayac_renk = self.renkler.get('ders_sayac', VARSAYILAN_RENK['ders_sayac']) 
        
        self.durum_label = tk.Label(self.main_frame, text="", font=self.baslik_font, 
                                    fg='#D4D4D4', bg=self.renkler['arka_plan'], anchor='center', height=1)
        self.durum_label.pack(fill='x', pady=(0, 2)) 
        
        # Sayaç ve Ünlem için Frame 
        self.sayaç_frame = tk.Frame(self.main_frame, bg=self.renkler['arka_plan'])
        # VEYİS: Sayaç çerçevesi altındaki boşluk azaltıldı 
        self.sayaç_frame.pack(fill='x', pady=(0, 2))
        
        # 2a. Sol Ünlem Etiketi 
        self.sol_unlem_label = tk.Label(self.sayaç_frame, text="", font=self.unlem_font, 
                                     fg=self.renkler['uyari_arka_plan'], bg=self.renkler['arka_plan'])
        self.sol_unlem_label.pack(side='left', padx=(5, 5)) 
        
        # 2b. Kalan Süre Etiketi
        self.kalan_süre_label = tk.Label(self.sayaç_frame, text="00:00:00", 
                                        font=self.sure_font, fg=ilk_sayac_renk, 
                                        bg=self.renkler['arka_plan'], relief='flat', bd=0)
        self.kalan_süre_label.pack(side='left', expand=True) 
        
        # 2c. Sağ Ünlem Etiketi 
        self.sag_unlem_label = tk.Label(self.sayaç_frame, text="", font=self.unlem_font, 
                                     fg=self.renkler['uyari_arka_plan'], bg=self.renkler['arka_plan'])
        self.sag_unlem_label.pack(side='right', padx=(5, 5))
        
        # 3. Saat Aralığı Etiketi
        self.saat_araligi_label = tk.Label(self.main_frame, text="", font=self.saat_araligi_font, 
                                            fg=self.renkler['alt_yazi'], bg=self.renkler['arka_plan'])
        # VEYİS: Saat aralığı altındaki boşluk azaltıldı 
        self.saat_araligi_label.pack(fill='x', pady=(0, 2)) 
        
        # 4. Bilgilendirme Etiketi
        self.info_label = tk.Label(self.main_frame, text="", font=self.info_font, fg=self.renkler['alt_yazi'], bg=self.renkler['arka_plan'])
        self.info_label.pack(fill='x')
        
        self.menu_bar_olustur()
        
        # Pencereyi içeriğine göre boyutlandır
        self.master.update_idletasks()
        width = self.master.winfo_reqwidth()
        height = self.master.winfo_reqheight()
        self.master.geometry(f'{width+10}x{height+10}') 

        self.guncelle(anlik=True) 
        self.guncelle_job = self.master.after(1000, self.guncelle) 
        
        if self.program_verisi is None:
             self.info_label.config(text="Excel yüklemek için 'Ayarlar' menüsünü kullanın.", fg='#FFFF00') 
             
        master.protocol("WM_DELETE_WINDOW", self.on_kapat) 

    def on_kapat(self):
        """Pencere kapatıldığında çağrılır."""
        if self.guncelle_job:
            self.master.after_cancel(self.guncelle_job)
        
        self.master.destroy()
        sys.exit()

    def menu_bar_olustur(self):
        """Menü barı oluşturur ve tüm seçenekleri Ayarlar menüsü altına toplar."""
        self.menubar = tk.Menu(self.master)
        self.gizle_job = None

        def menuyu_goster(event):
            if self.gizle_job:
                self.master.after_cancel(self.gizle_job)
                self.gizle_job = None
            self.master.config(menu=self.menubar)

        def menuyu_gizle_gecikmeli(event):
            # Alt menülere geçişte kapanmaması için süreyi uzattık (3 saniye)
            if self.gizle_job:
                self.master.after_cancel(self.gizle_job)
            self.gizle_job = self.master.after(3000, lambda: self.master.config(menu=""))

        # Fare pencere üzerine gelince menüyü göster, ayrılınca gizle
        self.master.bind('<Enter>', menuyu_goster)
        self.master.bind('<Leave>', menuyu_gizle_gecikmeli)

        # --- 1. AYARLAR MENÜSÜ (Tüm seçenekleri toplar) ---
        ayarlar_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ayarlar", menu=ayarlar_menu)
        
        # Menü barın kendisine de olay ekleyelim ki fare üzerindeyken kapanmasın
        self.menubar.bind('<Enter>', menuyu_goster)
        self.menubar.bind('<Leave>', menuyu_gizle_gecikmeli)

        # 1.1. Program Ayarları
        program_ayarlari_menu = tk.Menu(ayarlar_menu, tearoff=0)
        ayarlar_menu.add_cascade(label="Program ve Veri Ayarları", menu=program_ayarlari_menu)
        program_ayarlari_menu.add_command(
            label="Excel'den Program Yükle/Güncelle...", 
            command=self.excel_den_yukle_ve_kaydet
        )
        program_ayarlari_menu.add_command(
            label="Kritik Süre (sn) Ayarla...", 
            command=self.kritik_sure_ayarla
        )

        # 1.2. Görünüm Ayarları
        gorunum_ayarlari_menu = tk.Menu(ayarlar_menu, tearoff=0)
        ayarlar_menu.add_separator()
        ayarlar_menu.add_cascade(label="Görünüm ve Renk Ayarları", menu=gorunum_ayarlari_menu)
        
        # Font Boyutu Ayarları 
        gorunum_ayarlari_menu.add_command(
            label="Sayaç Yazı Boyutunu Ayarla...", 
            command=self.sayac_boyutu_ayarla
        )
        gorunum_ayarlari_menu.add_command(
            label="Saat Aralığı Yazı Boyutunu Ayarla...",
            command=self.saat_araligi_boyutu_ayarla
        )
        gorunum_ayarlari_menu.add_separator()

        # Renk Ayarları
        gorunum_ayarlari_menu.add_command(
            label="Genel Arka Plan Rengi Seç...", 
            command=lambda: self.renk_sec("arka_plan")
        )
        gorunum_ayarlari_menu.add_command(
            label="Uyarı Arka Plan Rengi Seç...", 
            command=lambda: self.renk_sec("uyari_arka_plan")
        )
        gorunum_ayarlari_menu.add_separator()
        gorunum_ayarlari_menu.add_command(
            label="Ders Sayaç Yazı Rengi...", 
            command=lambda: self.renk_sec("ders_sayac")
        )
        gorunum_ayarlari_menu.add_command(
            label="Teneffüs Sayaç Yazı Rengi...", 
            command=lambda: self.renk_sec("teneffus_sayac")
        )
        gorunum_ayarlari_menu.add_separator()
        gorunum_ayarlari_menu.add_command(
            label="Ders Başlık Rengi...", 
            command=lambda: self.renk_sec("ders_baslik")
        )
        gorunum_ayarlari_menu.add_command(
            label="Teneffüs Başlık Rengi...", 
            command=lambda: self.renk_sec("teneffus_baslik")
        )

        # 1.3. Çıkış
        ayarlar_menu.add_separator()
        ayarlar_menu.add_command(label="Çıkış", command=self.on_kapat)
        
    def saniyeden_saate_cevir(self, saniye):
        """Saniyeyi HH:MM:SS formatına çevirir."""
        saat = saniye // 3600
        dakika = (saniye % 3600) // 60
        saniye = saniye % 60
        return f"{saat:02}:{dakika:02}:{saniye:02}"

    def excel_den_yukle_ve_kaydet(self):
        """Kullanıcının Excel dosyasını seçmesini sağlar, yükler ve tüm veriyi kaydeder."""
        dosya_yolu = filedialog.askopenfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Dosyaları", "*.xlsx"), ("Tüm Dosyalar", "*.*")],
            title="Ders Programı Excel Dosyasını Seçin"
        )
        
        if dosya_yolu:
            yeni_program = excel_to_memory(dosya_yolu)
            
            if yeni_program is not None:
                self.program_verisi = yeni_program
                if tum_verileri_kaydet(self.program_verisi, self.renkler, self.ayarlar):
                    mesaj = f"Veri '{len(yeni_program)} ders' ile yüklendi ve kaydedildi! (Konum: {APP_DATA_FILE})"
                    renk = '#60BB60' # Yeşil
                else:
                    mesaj = "Veri yüklendi, ancak KAYIT BAŞARISIZ oldu."
                    renk = 'orange'
                
                self.info_label.config(text=mesaj, fg=renk)
                self.guncelle(anlik=True)
            else:
                self.info_label.config(text="Yükleme Başarısız. Hata mesajını kontrol edin.", fg=self.renkler['uyari_arka_plan'])

    def kritik_sure_ayarla(self):
        """Kullanıcının kritik uyarı süresini girmesini sağlar ve kaydeder."""
        
        mevcut_sure = self.ayarlar.get('kritik_sure', VARSAYILAN_AYARLAR['kritik_sure'])
        
        yeni_sure_s = simpledialog.askinteger(
            "Kritik Süre Ayarı", 
            f"Ders bitimine kaç saniye kala uyarı başlasın? (Mevcut: {mevcut_sure} sn)", 
            initialvalue=mevcut_sure,
            minvalue=10, 
            maxvalue=3600 
        )
        
        if yeni_sure_s is not None:
            self.ayarlar['kritik_sure'] = yeni_sure_s
            
            if tum_verileri_kaydet(self.program_verisi, self.renkler, self.ayarlar):
                mesaj = f"Kritik süre {yeni_sure_s} saniye olarak ayarlandı ve kaydedildi. (Konum: {APP_DATA_FILE})"
                renk = '#60BB60'
            else:
                mesaj = "Kritik süre güncellendi ancak KAYIT BAŞARISIZ oldu."
                renk = 'orange'
                
            self.info_label.config(text=mesaj, fg=renk)
            self.guncelle(anlik=True)

    def sayac_boyutu_ayarla(self):
        """Kullanıcının sayaç font boyutunu girmesini sağlar ve kaydeder/uygular."""
        
        mevcut_boyut = self.ayarlar.get('sayaç_boyutu', VARSAYILAN_AYARLAR['sayaç_boyutu'])
        
        yeni_boyut = simpledialog.askinteger(
            "Sayaç Boyutu Ayarı", 
            f"Sayaç yazı boyutunu (font size) girin. (Mevcut: {mevcut_boyut})", 
            initialvalue=mevcut_boyut,
            minvalue=16, 
            maxvalue=100 
        )
        
        if yeni_boyut is not None:
            self.ayarlar['sayaç_boyutu'] = yeni_boyut
            
            # Font nesnelerini güncelleyelim
            self.sure_font.config(size=yeni_boyut)
            self.unlem_font.config(size=int(yeni_boyut * 0.6))
            
            self._yeniden_boyutlandir_ve_kaydet(f"Sayaç boyutu {yeni_boyut} olarak ayarlandı ve kaydedildi.")

    def saat_araligi_boyutu_ayarla(self):
        """Kullanıcının saat aralığı font boyutunu girmesini sağlar ve kaydeder/uygular."""
        
        mevcut_boyut = self.ayarlar.get('saat_araligi_boyutu', VARSAYILAN_AYARLAR['saat_araligi_boyutu'])
        
        yeni_boyut = simpledialog.askinteger(
            "Saat Aralığı Boyutu Ayarı", 
            f"Saat aralığı yazı boyutunu (font size) girin. (Mevcut: {mevcut_boyut})", 
            initialvalue=mevcut_boyut,
            minvalue=8, 
            maxvalue=40 
        )
        
        if yeni_boyut is not None:
            self.ayarlar['saat_araligi_boyutu'] = yeni_boyut
            
            # Font nesnesini güncelleyelim
            self.saat_araligi_font.config(size=yeni_boyut)
            
            self._yeniden_boyutlandir_ve_kaydet(f"Saat aralığı boyutu {yeni_boyut} olarak ayarlandı ve kaydedildi.")

    def _yeniden_boyutlandir_ve_kaydet(self, basari_mesaji):
        """Ayarları kaydeder ve pencereyi içeriğe göre yeniden boyutlandırır."""
        
        if tum_verileri_kaydet(self.program_verisi, self.renkler, self.ayarlar):
            mesaj = f"{basari_mesaji} (Konum: {APP_DATA_FILE})"
            renk = '#60BB60'
        else:
            mesaj = "Görünüm güncellendi ancak KAYIT BAŞARISIZ oldu."
            renk = 'orange'
            
        # Pencereyi içeriğe göre yeniden boyutlandıralım
        self.master.update_idletasks()
        width = self.master.winfo_reqwidth()
        height = self.master.winfo_reqheight()
        self.master.geometry(f'{width+10}x{height+10}') 

        self.info_label.config(text=mesaj, fg=renk)
        self.guncelle(anlik=True)


    def arayuzu_guncelle(self):
        """Tüm arayüz elementlerinin renklerini günceller."""
        arka_plan = self.renkler['arka_plan']
        
        # Tüm ana bileşenlerin arka plan rengini güncelle
        self.master.configure(bg=arka_plan)
        self.main_frame.configure(bg=arka_plan)
        self.sayaç_frame.configure(bg=arka_plan)
        self.kalan_süre_label.configure(bg=arka_plan) 
        
        # Saat aralığı etiketinin arka planını güncelle
        self.saat_araligi_label.configure(bg=arka_plan, fg=self.renkler['alt_yazi']) 
        
        # Ünlemlerin ön planını uyarı rengiyle, arka planını ana arka planla güncelle
        self.sol_unlem_label.configure(bg=arka_plan, fg=self.renkler['uyari_arka_plan']) 
        self.sag_unlem_label.configure(bg=arka_plan, fg=self.renkler['uyari_arka_plan']) 
        
        self.info_label.configure(bg=arka_plan, fg=self.renkler['alt_yazi'])
        
        self.guncelle(anlik=True) 

    def renk_sec(self, tip_key):
        """Renk seçiciyi açar ve seçilen rengi kaydeder/uygular."""
        
        metin_haritasi = {
            'arka_plan': "Arka Plan", 'ders_sayac': "Ders Sayaç Yazı Rengi", 
            'teneffus_sayac': "Teneffüs Sayaç Yazı Rengi", 'ders_baslik': "Ders Başlık Rengi", 
            'teneffus_baslik': "Teneffüs Başlık Rengi", 'uyari_arka_plan': "Uyarı Arka Plan Rengi"
        }
        metin = metin_haritasi.get(tip_key, "Renk Seçimi")
            
        yeni_renk_kodu = colorchooser.askcolor(title=f"{metin} Seç")[1]
        
        if yeni_renk_kodu:
            self.renkler[tip_key] = yeni_renk_kodu
            
            tum_verileri_kaydet(self.program_verisi, self.renkler, self.ayarlar)
            self.arayuzu_guncelle()
            

    def guncelle(self, anlik=False):
        """Her saniye arayüzü ve hesaplamaları günceller."""
        
        if self.guncelle_job and not anlik:
            self.master.after_cancel(self.guncelle_job)
        
        if self.program_verisi is None:
            self._uyari_gorselini_sıfırla()
            self.saat_araligi_label.config(text="") 
            self.durum_label.config(text="PROGRAM YÜKLENMEDİ", bg='#400000', fg='#FFCCCC') 
            self.kalan_süre_label.config(text="---", fg=self.renkler['alt_yazi'], bg=self.renkler['arka_plan'])
            self.info_label.config(text="Excel yüklemek için 'Ayarlar' menüsünü kullanın.", fg='#FFFF00')
            self.guncelle_job = self.master.after(1000, self.guncelle) 
            return

        sonuc = kalan_süre_hesapla(self.program_verisi)
        
        # Kritik süreyi ayarlar dosyasından oku
        KRITIK_SURE_ANLIK = self.ayarlar.get('kritik_sure', VARSAYILAN_AYARLAR['kritik_sure'])
            
        # --- DURUM VE RENK AYARLAMA ---
        sayac_ana_renk = self.renkler['alt_yazi'] 
        durum_bg_renk = self.renkler['arka_plan']
        uyari_yapilmali = False
        saat_araligi_metni = "" 
        
        if sonuc['Type'] == "DERS":
            ders_adi_buyuk = sonuc['Ad'].upper().strip() 
            durum_metni = "ÖĞLE ARASININ BİTMESİNE" if ders_adi_buyuk == "ÖĞLE ARASI" else f"{ders_adi_buyuk} DERSİNİN BİTMESİNE"
            durum_bg_renk = self.renkler['ders_baslik'] 
            sayac_ana_renk = self.renkler['ders_sayac'] 
            
            # Saat aralığı metnini oluştur (HH:MM formatında, saniye kaldırıldı)
            saat_araligi_metni = f"({sonuc['Baslangic_Str'][:-3]} - {sonuc['Bitis_Str'][:-3]})"
            
            if sonuc['Kalan_Saniye'] <= KRITIK_SURE_ANLIK: 
                uyari_yapilmali = True 
            
        elif sonuc['Type'] == "TENEFFÜS":
            durum_metni = "TENEFFÜSÜN BİTMESİNE"
            durum_bg_renk = self.renkler['teneffus_baslik']
            sayac_ana_renk = self.renkler['teneffus_sayac'] 
            
            # Saat aralığı metnini oluştur
            saat_araligi_metni = f"({sonuc['Baslangic_Str'][:-3]} - {sonuc['Bitis_Str'][:-3]})"
            
            uyari_yapilmali = False 
            
        else: # GÜN SONU / BAŞLAMADI / BELİRSİZ
            self._uyari_gorselini_sıfırla()
            if sonuc['Type'] == "GÜN SONU":
                durum_metni = "GÜN SONU (PROGRAM BİTTİ)"
                durum_bg_renk = '#804000' 
            elif sonuc['Type'] == "GÜN BAŞLAMADI":
                durum_metni = "GÜN BAŞLAMADI (BEKLEMEDE)"
                durum_bg_renk = '#808000' 
            else:
                durum_metni = "DURUM BELİRSİZ"
            saat_araligi_metni = "" 
            
        # Başlık Etiketini her zaman hesaplanan ders/teneffüs rengiyle ayarla
        self.durum_label.config(text=durum_metni, bg=durum_bg_renk, fg='#FFFFFF')
        
        
        # --- UYARI GÖRSELİ UYGULAMA ---
        if uyari_yapilmali:
            # Sadece ana bileşenlerin arka planını uyarı rengine ayarla (Başlık Hariç)
            uyari_bg = self.renkler['uyari_arka_plan']
            
            self.master.configure(bg=uyari_bg) 
            self.main_frame.configure(bg=uyari_bg) 
            self.sayaç_frame.configure(bg=uyari_bg) 
            
            # Etiketlerin arka planlarını uyarı rengine ayarla
            self.kalan_süre_label.config(bg=uyari_bg)
            self.sol_unlem_label.config(bg=uyari_bg)
            self.sag_unlem_label.config(bg=uyari_bg)
            self.info_label.config(bg=uyari_bg) 
            self.saat_araligi_label.config(bg=uyari_bg, fg='#FFFFFF') 
            
            # Ünlemleri göster
            self.sol_unlem_label.config(text="!", fg='#FFFFFF', bg=uyari_bg)
            self.sag_unlem_label.config(text="!", fg='#FFFFFF', bg=uyari_bg)

        else:
            # Normal renklere dön 
            self._uyari_gorselini_sıfırla()
            
            # Tüm ana bileşenlerin arka planını normal arka plan rengine geri ayarla
            normal_bg = self.renkler['arka_plan']
            self.master.configure(bg=normal_bg) 
            self.main_frame.configure(bg=normal_bg)
            self.sayaç_frame.configure(bg=normal_bg)
            
            # Etiket arka planlarını normal arka plan rengine geri ayarla
            self.kalan_süre_label.config(bg=normal_bg) 
            self.sol_unlem_label.config(bg=normal_bg)
            self.sag_unlem_label.config(bg=normal_bg)
            self.info_label.config(bg=normal_bg)
            self.saat_araligi_label.config(bg=normal_bg, fg=self.renkler['alt_yazi'])
            
            # self.durum_label satırı yukarı taşındığı için buradan kaldırıldı.
        
        
        # --- Kalan Süre ve Saat Aralığı Güncelleme ---
        if sonuc['Kalan_Saniye'] > 0:
            kalan_süre_text = self.saniyeden_saate_cevir(sonuc['Kalan_Saniye'])
            
            self.kalan_süre_label.config(text=kalan_süre_text, fg=sayac_ana_renk)
            self.saat_araligi_label.config(text=saat_araligi_metni) 
            self.info_label.config(text="") 
            
        else:
            self._uyari_gorselini_sıfırla() 
            
            # Gün Sonu / Başlamadı durumunda arka planları normal renge çevir
            normal_bg = self.renkler['arka_plan']
            self.master.configure(bg=normal_bg) 
            self.main_frame.configure(bg=normal_bg)
            self.sayaç_frame.configure(bg=normal_bg)
            self.kalan_süre_label.config(bg=normal_bg) 
            self.info_label.config(bg=normal_bg)
            self.saat_araligi_label.config(bg=normal_bg, text="") 
            
            self.kalan_süre_label.config(text="BİTTİ", fg=self.renkler['alt_yazi'])
            self.info_label.config(text="", fg=self.renkler['alt_yazi'])
        
        # 1 saniyelik döngüyü yeniden planla
        self.guncelle_job = self.master.after(1000, self.guncelle)

    def _uyari_gorselini_sıfırla(self):
        """Ünlem işaretlerini gizler."""
        self.sol_unlem_label.config(text="")
        self.sag_unlem_label.config(text="")


# ==============================
# 4. PROGRAMI BAŞLATMA
# ==============================

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = DersTakipUygulamasi(root)
        root.mainloop()
    except Exception as e:
        mesaj = f"Program başlatılırken kritik bir hata oluştu: {e}\n\n"
        mesaj += "Eğer doğrudan Python ile çalıştırıyorsanız, 'pip install pandas openpyxl' komutunu çalıştırdığınızdan emin olun.\n"
        mesaj += "Eğer EXE dosyasını çalıştırıyorsanız, eksik bağımlılıklar olabilir. Tekrar PyInstaller komutunu çalıştırın.\n\n"
        mesaj += f"Veri dosyası konumu: {APP_DATA_FILE}"
        messagebox.showerror("Kritik Hata", mesaj)
        sys.exit(1)
