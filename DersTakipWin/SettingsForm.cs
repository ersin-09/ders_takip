using System;
using System.Drawing;
using System.Windows.Forms;

namespace DersTakipWin;

public partial class SettingsForm : Form
{
    private RenkAyar _renkler;
    private UygulamaAyar _ayarlar;

    public SettingsForm(UygulamaAyar ayarlar, RenkAyar renkler)
    {
        InitializeComponent();
        _ayarlar = ayarlar;
        _renkler = renkler;
        GuncelAyarlar = ayarlar;
        GuncelRenkler = renkler;

        numericKritikSure.Value = Clamp(ayarlar.KritikSure, (int)numericKritikSure.Minimum, (int)numericKritikSure.Maximum);
        numericSayacFont.Value = Clamp(ayarlar.SayacFontBoyutu, (int)numericSayacFont.Minimum, (int)numericSayacFont.Maximum);
        numericSaatFont.Value = Clamp(ayarlar.SaatAraligiFontBoyutu, (int)numericSaatFont.Minimum, (int)numericSaatFont.Maximum);

        buttonDersSayacRenk.Tag = nameof(RenkAyar.DersSayac);
        buttonTeneffusSayacRenk.Tag = nameof(RenkAyar.TeneffusSayac);
        buttonArkaPlanRenk.Tag = nameof(RenkAyar.ArkaPlan);

        GuncelleButonRenkleri();
    }

    public UygulamaAyar GuncelAyarlar { get; private set; }
    public RenkAyar GuncelRenkler { get; private set; }

    private static int Clamp(int value, int min, int max) => Math.Min(Math.Max(value, min), max);

    private void GuncelleButonRenkleri()
    {
        RenkAyarla(buttonDersSayacRenk, _renkler.DersSayac);
        RenkAyarla(buttonTeneffusSayacRenk, _renkler.TeneffusSayac);
        RenkAyarla(buttonArkaPlanRenk, _renkler.ArkaPlan);
    }

    private static void RenkAyarla(Button button, string hex)
    {
        try
        {
            var renk = ColorTranslator.FromHtml(hex);
            button.BackColor = renk;
            button.ForeColor = RenkKontrast(renk);
        }
        catch
        {
            button.BackColor = SystemColors.Control;
            button.ForeColor = SystemColors.ControlText;
        }
    }

    private static Color RenkKontrast(Color arkaPlan)
    {
        var luminance = (0.299 * arkaPlan.R + 0.587 * arkaPlan.G + 0.114 * arkaPlan.B) / 255;
        return luminance > 0.5 ? Color.Black : Color.White;
    }

    private void renkButonunaTiklandi(object? sender, EventArgs e)
    {
        if (sender is not Button button || button.Tag is not string anahtar)
        {
            return;
        }

        using var dialog = new ColorDialog
        {
            FullOpen = true
        };

        try
        {
            dialog.Color = ColorTranslator.FromHtml(RenkDegeriniOku(anahtar));
        }
        catch
        {
            dialog.Color = button.BackColor;
        }

        if (dialog.ShowDialog(this) != DialogResult.OK)
        {
            return;
        }

        var hex = ColorTranslator.ToHtml(dialog.Color);
        _renkler = anahtar switch
        {
            nameof(RenkAyar.DersSayac) => _renkler with { DersSayac = hex },
            nameof(RenkAyar.TeneffusSayac) => _renkler with { TeneffusSayac = hex },
            nameof(RenkAyar.ArkaPlan) => _renkler with { ArkaPlan = hex },
            _ => _renkler
        };

        GuncelleButonRenkleri();
    }

    private string RenkDegeriniOku(string anahtar) => anahtar switch
    {
        nameof(RenkAyar.DersSayac) => _renkler.DersSayac,
        nameof(RenkAyar.TeneffusSayac) => _renkler.TeneffusSayac,
        nameof(RenkAyar.ArkaPlan) => _renkler.ArkaPlan,
        _ => "#FFFFFF"
    };

    private void buttonKaydet_Click(object? sender, EventArgs e)
    {
        GuncelAyarlar = _ayarlar with
        {
            KritikSure = (int)numericKritikSure.Value,
            SayacFontBoyutu = (int)numericSayacFont.Value,
            SaatAraligiFontBoyutu = (int)numericSaatFont.Value
        };

        GuncelRenkler = _renkler;
        DialogResult = DialogResult.OK;
    }

    private void buttonIptal_Click(object? sender, EventArgs e)
    {
        DialogResult = DialogResult.Cancel;
    }
}
