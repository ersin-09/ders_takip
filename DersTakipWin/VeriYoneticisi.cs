using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

namespace DersTakipWin;

public static class VeriYoneticisi
{
    private const string DosyaAdi = "ders_takip_verileri.json";

    public static string VeriKlasoru()
    {
        try
        {
            var basePath = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            if (string.IsNullOrWhiteSpace(basePath))
            {
                basePath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            }

            var klasor = Path.Combine(basePath, "DersTakip");
            Directory.CreateDirectory(klasor);
            return klasor;
        }
        catch
        {
            return AppContext.BaseDirectory;
        }
    }

    public static string VeriDosyasiYolu() => Path.Combine(VeriKlasoru(), DosyaAdi);

    public static UygulamaVeri VerileriYukle()
    {
        var yol = VeriDosyasiYolu();
        if (!File.Exists(yol))
        {
            return new UygulamaVeri();
        }

        try
        {
            var json = File.ReadAllText(yol);
            var veri = JsonSerializer.Deserialize<UygulamaVeri>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (veri == null)
            {
                return new UygulamaVeri();
            }

            // Eksik alanlar için varsayılanları tamamla
            return veri with
            {
                Program = veri.Program ?? new List<DersKaydi>(),
                Renkler = veri.Renkler ?? RenkAyar.Varsayilan(),
                Ayarlar = veri.Ayarlar ?? UygulamaAyar.Varsayilan()
            };
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"Veriler okunamadı: {ex.Message}", ex);
        }
    }

    public static void VerileriKaydet(UygulamaVeri veri)
    {
        var yol = VeriDosyasiYolu();
        var klasor = Path.GetDirectoryName(yol);
        if (!string.IsNullOrEmpty(klasor))
        {
            Directory.CreateDirectory(klasor);
        }

        var json = JsonSerializer.Serialize(veri, new JsonSerializerOptions
        {
            WriteIndented = true
        });

        File.WriteAllText(yol, json);
    }
}
