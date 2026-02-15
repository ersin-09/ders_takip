#!/bin/bash

# Betiğin bulunduğu dizine git (önemli: .desktop dosyasından veya başka yerden çağrıldığında)
cd "$(dirname "$0")"

# Sanal ortamın python yorumlayıcısını kullanarak uygulamayı başlat
if [ -f "venv/bin/python3" ]; then
    ./venv/bin/python3 ders_takip.py
else
    echo "HATA: Sanal ortam bulunamadı. Lütfen önce './install.sh' betiğini çalıştırın."
    exit 1
fi
