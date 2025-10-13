# Ders Takip Uygulaması (Windows)

Bu depo; ders programı takibini kolaylaştıran, Excel dosyasından ders saatlerini okuyup kalan süreyi gösteren Windows Forms tabanlı bir .NET uygulaması içerir. Python/Tkinter sürümünde yaşanan Windows kaynaklı dosya yazma ve kararlılık sorunlarını azaltmak için uygulama C# dilinde yeniden yazılmıştır.

## Başlangıç

1. [Windows için .NET SDK 8.0](https://dotnet.microsoft.com/en-us/download) kurulu olduğundan emin olun.
2. Depo klasöründe aşağıdaki komutları çalıştırarak NuGet paketlerini yükleyin ve uygulamayı derleyin:

```bash
dotnet restore DersTakipWin\DersTakipWin.csproj
dotnet build DersTakipWin\DersTakipWin.csproj
```

3. Uygulamayı çalıştırmak için:

```bash
dotnet run --project DersTakipWin\DersTakipWin.csproj
```

> Not: Uygulama Windows Forms bileşenleri kullandığı için yalnızca Windows ortamında çalıştırılması önerilir.

## Çalıştırılabilir (.exe) oluşturma

Windows üzerinde bağımsız bir `.exe` dosyası üretmek için .NET'in `publish` komutunu kullanabilirsiniz. Aşağıdaki adımlar, 64 bit Windows için kendinden yeterli (self-contained) tek dosyalık bir paket oluşturur:

```powershell
dotnet publish DersTakipWin\DersTakipWin.csproj `
    -c Release `
    -r win-x64 `
    --self-contained true `
    /p:PublishSingleFile=true
```

Komut tamamlandığında derlenen uygulama `DersTakipWin\bin\Release\net8.0-windows\win-x64\publish\DersTakipWin.exe` yolunda oluşur. İsterseniz `win-x86` gibi farklı bir çalışma zamanı belirterek 32 bit sürüm de üretebilirsiniz. Visual Studio kullanıyorsanız da aynı ayarları **Publish** sihirbazı üzerinden seçerek yayımlama profilini oluşturup tek tıklamayla `.exe` çıktısı alabilirsiniz.

## Temel Özellikler

- **Excel Entegrasyonu:** Ders programını `.xlsx` formatındaki dosyalardan yükler ve hatalı saat formatlarını kullanıcıya bildirir.
- **Kalıcı Ayarlar:** Yerel uygulama verilerini `LocalApplicationData/DersTakip` klasöründe saklar, renk ve sayaç ayarlarını kaydeder.
- **Özelleştirilebilir Arayüz:** Sayaç font boyutu, kritik süre ve renk seçenekleri ayar ekranından değiştirilebilir.
- **Canlı Sayaç:** Aktif ders veya teneffüs süresi geri sayımla izlenir, kritik sürede renk değişimi ile uyarı verir.

## Excel Şablonu

Excel dosyası şu kolonlara sahip olmalıdır:

| Ders Adı | Başlangıç | Bitiş |
|----------|-----------|-------|
| Matematik | 08:30:00 | 09:10:00 |

Başlık satırı ilk satır olmalı, saatler `HH:MM:SS` formatında veya Excel saat biçiminde girilmelidir.
