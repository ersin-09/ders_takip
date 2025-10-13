using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.Linq;
using System.Windows.Forms;
using ClosedXML.Excel;

namespace DersTakipWin;

public partial class MainForm : Form
{
    private readonly List<DersKaydi> _program = new();
    private RenkAyar _renkler = RenkAyar.Varsayilan();
    private UygulamaAyar _ayarlar = UygulamaAyar.Varsayilan();

    public MainForm()
    {
        InitializeComponent();
    }

    private void MainForm_Load(object? sender, EventArgs e)
    {
        try
        {
            var veri = VeriYoneticisi.VerileriYukle();
            _program.Clear();
            _program.AddRange(veri.Program.OrderBy(p => p.BaslangicZaman));
            _renkler = veri.Renkler ?? RenkAyar.Varsayilan();
            _ayarlar = veri.Ayarlar ?? UygulamaAyar.Varsayilan();
            ProgramListesiniYenile();
            GorselAyarUygula();
            toolStripDurum.Text = $"Veri dosyası: {VeriYoneticisi.VeriDosyasiYolu()}";
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, ex.Message, "Veri Yüklenemedi", MessageBoxButtons.OK, MessageBoxIcon.Error);
            toolStripDurum.Text = ex.Message;
        }

        zamanlayici.Start();
        GuncelDurumuHesapla();
    }

    private void GorselAyarUygula()
    {
        try
        {
            BackColor = ColorTranslator.FromHtml(_renkler.ArkaPlan);
            labelDurumBaslik.ForeColor = ColorTranslator.FromHtml(_renkler.AltYazi);
            labelKalanSureBaslik.ForeColor = ColorTranslator.FromHtml(_renkler.AltYazi);
            labelDurumIcerik.ForeColor = ColorTranslator.FromHtml(_renkler.DersBaslik);
            labelKalanSureIcerik.ForeColor = ColorTranslator.FromHtml(_renkler.DersSayac);
        }
        catch
        {
            // HTML kodu hatalıysa varsayılanları uygula
            _renkler = RenkAyar.Varsayilan();
            BackColor = ColorTranslator.FromHtml(_renkler.ArkaPlan);
        }

        labelKalanSureIcerik.Font = new Font(labelKalanSureIcerik.Font.FontFamily,
            Math.Max(16, _ayarlar.SayacFontBoyutu), FontStyle.Bold);
        listViewProgram.Font = new Font(listViewProgram.Font.FontFamily,
            Math.Max(10, _ayarlar.SaatAraligiFontBoyutu), FontStyle.Regular);
    }

    private void ProgramListesiniYenile()
    {
        listViewProgram.BeginUpdate();
        listViewProgram.Items.Clear();
        foreach (var ders in _program.OrderBy(d => d.BaslangicZaman))
        {
            var item = new ListViewItem(ders.Ad);
            item.SubItems.Add(ders.Baslangic);
            item.SubItems.Add(ders.Bitis);
            listViewProgram.Items.Add(item);
        }

        listViewProgram.EndUpdate();
    }

    private void zamanlayici_Tick(object? sender, EventArgs e)
    {
        GuncelDurumuHesapla();
    }

    private void GuncelDurumuHesapla()
    {
        if (_program.Count == 0)
        {
            labelDurumIcerik.Text = "Program bilgisi bulunamadı";
            labelKalanSureIcerik.Text = "00:00:00";
            labelKalanSureIcerik.ForeColor = ColorTranslator.FromHtml(_renkler.AltYazi);
            return;
        }

        var simdi = DateTime.Now.TimeOfDay;
        DersKaydi? aktif = null;
        DersKaydi? sonraki = null;

        foreach (var ders in _program.OrderBy(d => d.BaslangicZaman))
        {
            if (simdi >= ders.BaslangicZaman && simdi < ders.BitisZaman)
            {
                aktif = ders;
                break;
            }

            if (simdi < ders.BaslangicZaman)
            {
                sonraki ??= ders;
                break;
            }
        }

        listViewProgram.SelectedItems.Clear();
        if (aktif != null)
        {
            labelDurumIcerik.ForeColor = ColorTranslator.FromHtml(_renkler.DersBaslik);
            labelDurumIcerik.Text = $"{aktif.Ad} dersi devam ediyor ({aktif.Baslangic} - {aktif.Bitis})";
            var kalan = aktif.BitisZaman - simdi;
            labelKalanSureIcerik.Text = FormatSure(kalan);
            labelKalanSureIcerik.ForeColor = kalan.TotalSeconds <= _ayarlar.KritikSure
                ? ColorTranslator.FromHtml(_renkler.UyariArkaPlan)
                : ColorTranslator.FromHtml(_renkler.DersSayac);
            ProgramListesindeSec(aktif);
        }
        else if (sonraki != null)
        {
            labelDurumIcerik.ForeColor = ColorTranslator.FromHtml(_renkler.TeneffusBaslik);
            labelDurumIcerik.Text = $"{sonraki.Ad} dersine kadar teneffüs";
            var kalan = sonraki.BaslangicZaman - simdi;
            labelKalanSureIcerik.Text = FormatSure(kalan);
            labelKalanSureIcerik.ForeColor = ColorTranslator.FromHtml(_renkler.TeneffusSayac);
            ProgramListesindeSec(sonraki);
        }
        else
        {
            labelDurumIcerik.ForeColor = ColorTranslator.FromHtml(_renkler.AltYazi);
            labelDurumIcerik.Text = "Program sona erdi";
            labelKalanSureIcerik.ForeColor = ColorTranslator.FromHtml(_renkler.AltYazi);
            labelKalanSureIcerik.Text = "00:00:00";
        }
    }

    private static string FormatSure(TimeSpan sure)
    {
        if (sure < TimeSpan.Zero)
        {
            sure = TimeSpan.Zero;
        }

        return sure.ToString(@"hh\:mm\:ss");
    }

    private void ProgramListesindeSec(DersKaydi ders)
    {
        foreach (ListViewItem item in listViewProgram.Items)
        {
            if (item.Text == ders.Ad &&
                item.SubItems[1].Text == ders.Baslangic &&
                item.SubItems[2].Text == ders.Bitis)
            {
                item.Selected = true;
                item.Focused = true;
                item.EnsureVisible();
                break;
            }
        }
    }

    private void buttonExcelYukle_Click(object? sender, EventArgs e)
    {
        using var dialog = new OpenFileDialog
        {
            Title = "Ders Programı Excel Dosyasını Seçin",
            Filter = "Excel Dosyaları (*.xlsx)|*.xlsx|Tüm Dosyalar (*.*)|*.*",
            Multiselect = false
        };

        if (dialog.ShowDialog(this) != DialogResult.OK)
        {
            return;
        }

        try
        {
            var dersler = ExcelPrograminiOku(dialog.FileName);
            _program.Clear();
            _program.AddRange(dersler.OrderBy(d => d.BaslangicZaman));
            ProgramListesiniYenile();
            GuncelDurumuHesapla();
            toolStripDurum.Text = $"Excel yüklendi: {dialog.FileName}";
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, ex.Message, "Excel Yüklenemedi", MessageBoxButtons.OK, MessageBoxIcon.Error);
            toolStripDurum.Text = ex.Message;
        }
    }

    private static IEnumerable<DersKaydi> ExcelPrograminiOku(string dosyaYolu)
    {
        var dersler = new List<DersKaydi>();

        using var workbook = new XLWorkbook(dosyaYolu);
        var worksheet = workbook.Worksheets.FirstOrDefault();
        if (worksheet == null)
        {
            throw new InvalidOperationException("Excel dosyasında çalışma sayfası bulunamadı.");
        }

        var firstRowUsed = worksheet.FirstRowUsed();
        if (firstRowUsed == null)
        {
            throw new InvalidOperationException("Excel dosyası boş görünüyor.");
        }

        var row = firstRowUsed.RowUsed();
        var firstDataRow = row.RowNumber() + 1; // Başlık satırını atla
        var lastRow = worksheet.LastRowUsed()?.RowNumber() ?? firstDataRow - 1;

        for (var rowIndex = firstDataRow; rowIndex <= lastRow; rowIndex++)
        {
            var currentRow = worksheet.Row(rowIndex);
            if (currentRow == null)
            {
                continue;
            }

            var ad = currentRow.Cell(1).GetValue<string>().Trim();
            var baslangicSaat = HucreyiSaatOlarakAl(currentRow.Cell(2), ad, "Başlangıç");
            var bitisSaat = HucreyiSaatOlarakAl(currentRow.Cell(3), ad, "Bitiş");

            if (string.IsNullOrWhiteSpace(ad))
            {
                continue;
            }

            dersler.Add(new DersKaydi
            {
                Ad = ad,
                Baslangic = baslangicSaat,
                Bitis = bitisSaat
            });
        }

        if (dersler.Count == 0)
        {
            throw new InvalidOperationException("Excel dosyasında ders bilgisi bulunamadı.");
        }

        return dersler;
    }

    private static string HucreyiSaatOlarakAl(IXLCell hucre, string dersAdi, string kolonAdi)
    {
        if (hucre.DataType == XLDataType.DateTime)
        {
            return hucre.GetDateTime().TimeOfDay.ToString(@"hh\:mm\:ss");
        }

        var deger = hucre.GetValue<string>().Trim();
        if (TimeSpan.TryParse(deger, out var sure))
        {
            return sure.ToString(@"hh\:mm\:ss");
        }

        if ((double.TryParse(deger, NumberStyles.Float, CultureInfo.InvariantCulture, out var sayisal) ||
             double.TryParse(deger, NumberStyles.Float, CultureInfo.CurrentCulture, out sayisal)) && sayisal > 0)
        {
            var excelTarih = DateTime.FromOADate(sayisal);
            return excelTarih.TimeOfDay.ToString(@"hh\:mm\:ss");
        }

        throw new InvalidOperationException($"'{dersAdi}' satırında {kolonAdi} sütunu geçersiz: '{deger}'");
    }

    private void buttonKaydet_Click(object? sender, EventArgs e)
    {
        try
        {
            var veri = new UygulamaVeri
            {
                Program = new List<DersKaydi>(_program),
                Renkler = _renkler,
                Ayarlar = _ayarlar
            };

            VeriYoneticisi.VerileriKaydet(veri);
            MessageBox.Show(this, $"Veriler kaydedildi.\n{VeriYoneticisi.VeriDosyasiYolu()}", "Kayıt Başarılı", MessageBoxButtons.OK, MessageBoxIcon.Information);
            toolStripDurum.Text = $"Veriler kaydedildi: {VeriYoneticisi.VeriDosyasiYolu()}";
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, ex.Message, "Kayıt Hatası", MessageBoxButtons.OK, MessageBoxIcon.Error);
            toolStripDurum.Text = ex.Message;
        }
    }

    private void buttonAyarlar_Click(object? sender, EventArgs e)
    {
        using var form = new SettingsForm(_ayarlar, _renkler);
        if (form.ShowDialog(this) == DialogResult.OK)
        {
            _ayarlar = form.GuncelAyarlar;
            _renkler = form.GuncelRenkler;
            GorselAyarUygula();
            GuncelDurumuHesapla();
        }
    }
}
