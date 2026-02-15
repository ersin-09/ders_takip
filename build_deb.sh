#!/bin/bash
set -e

# Yapılandırma
APP_NAME="ders-takip"
VERSION="1.6"
ARCH="all"
PKG_DIR="${APP_NAME}_${VERSION}_${ARCH}"
OPT_DIR="$PKG_DIR/opt/$APP_NAME"
DESKTOP_SRC="ders_takip.desktop"

echo "Paket dizini oluşturuluyor: $PKG_DIR"
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$OPT_DIR"
mkdir -p "$PKG_DIR/usr/share/applications"
mkdir -p "$PKG_DIR/usr/bin"
mkdir -p "$PKG_DIR/etc/xdg/autostart"

# Dosyaları kopyala
echo "Dosyalar kopyalanıyor..."
cp ders_takip.py "$OPT_DIR/"
cp ders_saatleri.xlsx "$OPT_DIR/"
cp run.sh "$OPT_DIR/"

# run.sh dosyasını paket için uyarla (gerekirse)
# Şimdilik olduğu gibi kopyalıyoruz çünkü run.sh "cd $(dirname "$0")" ile çalışıyor.
chmod +x "$OPT_DIR/run.sh"

# Desktop dosyasını paket için düzenle ve kopyala
echo "Desktop dosyası yapılandırılıyor..."
cat "$DESKTOP_SRC" | sed "s|Exec=.*|Exec=/opt/$APP_NAME/run.sh|" > "$PKG_DIR/usr/share/applications/$APP_NAME.desktop"
# Otomatik başlatma için de aynı desktop dosyasını kopyala
cp "$PKG_DIR/usr/share/applications/$APP_NAME.desktop" "$PKG_DIR/etc/xdg/autostart/"

# /usr/bin için sembolik bağ oluşturma betiği (postinst içinde yapılabilir veya buraya link koyulabilir)
# Ancak en temizi /usr/bin altına bir çalıştırılabilir script koymak
cat <<EOF > "$PKG_DIR/usr/bin/$APP_NAME"
#!/bin/bash
/opt/$APP_NAME/run.sh
EOF
chmod +x "$PKG_DIR/usr/bin/$APP_NAME"

# Control dosyası
echo "DEBIAN/control oluşturuluyor..."
cat <<EOF > "$PKG_DIR/DEBIAN/control"
Package: $APP_NAME
Version: $VERSION
Section: education
Priority: optional
Architecture: $ARCH
Depends: python3, python3-pip, python3-tk, python3-venv
Maintainer: Ersin
Description: Ders Takip Uygulaması
 Akıllı tahtalar için ders süresi ve teneffüs takip programı.
 Python ve Tkinter kullanılarak geliştirilmiştir.
EOF

# Post-installation script (Sanal ortam kurulumu)
echo "DEBIAN/postinst oluşturuluyor..."
cat <<EOF > "$PKG_DIR/DEBIAN/postinst"
#!/bin/bash
set -e

APP_DIR="/opt/$APP_NAME"

echo "Ders Takip: Sanal ortam yapılandırılıyor..."
if [ ! -d "\$APP_DIR/venv" ]; then
    python3 -m venv "\$APP_DIR/venv"
fi

echo "Ders Takip: Bağımlılıklar yükleniyor..."
"\$APP_DIR/venv/bin/pip" install pandas openpyxl

# İzinleri ayarla
chmod -R 755 "\$APP_DIR"
# Veri dosyasının yazılabilmesi için izin vermek gerekebilir, 
# ancak /opt altında genellikle root sahibi olur. 
# Uygulama verileri userspace'de (LocalApplicationData) tuttuğu için sorun olmamalı.

exit 0
EOF
chmod 755 "$PKG_DIR/DEBIAN/postinst"

# Paketi oluştur
echo "Paket oluşturuluyor..."
dpkg-deb --build "$PKG_DIR"

# Geçici derleme klasörünü temizle
echo "Temizlik yapılıyor..."
rm -rf "$PKG_DIR"

echo "Tamamlandı: ${PKG_DIR}.deb"
