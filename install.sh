#!/bin/bash

# Hata durumunda dur
set -e

echo "Pardus/Linux için Ders Takip Kurulumu"
echo "-------------------------------------"

# 1. Sistem paketlerini güncelle ve gerekli bağımlılıkları yükle
echo "[1/3] Sistem paketleri yükleniyor..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-tk python3-venv
else
    echo "UYARI: 'apt-get' bulunamadı. Gerekli paketlerin (python3, python3-tk, python3-venv) kurulu olduğundan emin olun."
fi

# 2. Sanal ortam (virtual environment) oluştur
echo "[2/3] Python sanal ortamı oluşturuluyor..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Sanal ortam 'venv' klasöründe oluşturuldu."
else
    echo "Sanal ortam zaten mevcut."
fi

# 3. Python kütüphanelerini yükle
echo "[3/3] Python kütüphaneleri yükleniyor..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install pandas openpyxl

echo "-------------------------------------"
echo "Kurulum tamamlandı!"
echo "Çalıştırmak için ./run.sh komutunu kullanabilirsiniz."
