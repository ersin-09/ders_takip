using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace DersTakipWin;

public record DersKaydi
{
    public string Ad { get; init; } = string.Empty;
    public string Baslangic { get; init; } = "00:00:00";
    public string Bitis { get; init; } = "00:00:00";

    [JsonIgnore]
    public TimeSpan BaslangicZaman => TimeSpan.ParseExact(Baslangic, "hh\:mm\:ss", null);

    [JsonIgnore]
    public TimeSpan BitisZaman => TimeSpan.ParseExact(Bitis, "hh\:mm\:ss", null);
}

public record RenkAyar
{
    public string ArkaPlan { get; init; } = "#252526";
    public string AltYazi { get; init; } = "#999999";
    public string UyariArkaPlan { get; init; } = "#990000";
    public string DersBaslik { get; init; } = "#004080";
    public string TeneffusBaslik { get; init; } = "#006600";
    public string DersSayac { get; init; } = "#00CCFF";
    public string TeneffusSayac { get; init; } = "#CCFF00";

    public static RenkAyar Varsayilan() => new();
}

public record UygulamaAyar
{
    public int KritikSure { get; init; } = 180;
    public int SayacFontBoyutu { get; init; } = 40;
    public int SaatAraligiFontBoyutu { get; init; } = 12;

    public static UygulamaAyar Varsayilan() => new();
}

public record UygulamaVeri
{
    public List<DersKaydi> Program { get; init; } = new();
    public RenkAyar Renkler { get; init; } = RenkAyar.Varsayilan();
    public UygulamaAyar Ayarlar { get; init; } = UygulamaAyar.Varsayilan();
}
