using System.Drawing;
using System.Windows.Forms;

namespace DersTakipWin;

partial class SettingsForm
{
    private System.ComponentModel.IContainer? components = null;
    private NumericUpDown numericKritikSure;
    private NumericUpDown numericSayacFont;
    private NumericUpDown numericSaatFont;
    private Button buttonDersSayacRenk;
    private Button buttonTeneffusSayacRenk;
    private Button buttonArkaPlanRenk;
    private Button buttonKaydet;
    private Button buttonIptal;
    private Label labelKritikSure;
    private Label labelSayacFont;
    private Label labelSaatFont;
    private FlowLayoutPanel renkPaneli;

    protected override void Dispose(bool disposing)
    {
        if (disposing && (components != null))
        {
            components.Dispose();
        }
        base.Dispose(disposing);
    }

    private void InitializeComponent()
    {
        components = new System.ComponentModel.Container();
        numericKritikSure = new NumericUpDown();
        numericSayacFont = new NumericUpDown();
        numericSaatFont = new NumericUpDown();
        buttonDersSayacRenk = new Button();
        buttonTeneffusSayacRenk = new Button();
        buttonArkaPlanRenk = new Button();
        buttonKaydet = new Button();
        buttonIptal = new Button();
        labelKritikSure = new Label();
        labelSayacFont = new Label();
        labelSaatFont = new Label();
        renkPaneli = new FlowLayoutPanel();
        ((System.ComponentModel.ISupportInitialize)numericKritikSure).BeginInit();
        ((System.ComponentModel.ISupportInitialize)numericSayacFont).BeginInit();
        ((System.ComponentModel.ISupportInitialize)numericSaatFont).BeginInit();
        SuspendLayout();
        // 
        // numericKritikSure
        // 
        numericKritikSure.Location = new Point(200, 18);
        numericKritikSure.Maximum = new decimal(new int[] { 900, 0, 0, 0 });
        numericKritikSure.Minimum = new decimal(new int[] { 30, 0, 0, 0 });
        numericKritikSure.Name = "numericKritikSure";
        numericKritikSure.Size = new Size(120, 23);
        numericKritikSure.TabIndex = 0;
        numericKritikSure.Value = new decimal(new int[] { 180, 0, 0, 0 });
        // 
        // numericSayacFont
        // 
        numericSayacFont.Location = new Point(200, 58);
        numericSayacFont.Maximum = new decimal(new int[] { 96, 0, 0, 0 });
        numericSayacFont.Minimum = new decimal(new int[] { 16, 0, 0, 0 });
        numericSayacFont.Name = "numericSayacFont";
        numericSayacFont.Size = new Size(120, 23);
        numericSayacFont.TabIndex = 1;
        numericSayacFont.Value = new decimal(new int[] { 40, 0, 0, 0 });
        // 
        // numericSaatFont
        // 
        numericSaatFont.Location = new Point(200, 98);
        numericSaatFont.Maximum = new decimal(new int[] { 32, 0, 0, 0 });
        numericSaatFont.Minimum = new decimal(new int[] { 10, 0, 0, 0 });
        numericSaatFont.Name = "numericSaatFont";
        numericSaatFont.Size = new Size(120, 23);
        numericSaatFont.TabIndex = 2;
        numericSaatFont.Value = new decimal(new int[] { 12, 0, 0, 0 });
        // 
        // buttonDersSayacRenk
        // 
        buttonDersSayacRenk.Location = new Point(3, 3);
        buttonDersSayacRenk.Name = "buttonDersSayacRenk";
        buttonDersSayacRenk.Size = new Size(180, 32);
        buttonDersSayacRenk.TabIndex = 3;
        buttonDersSayacRenk.Text = "Ders Sayacı Rengi";
        buttonDersSayacRenk.UseVisualStyleBackColor = true;
        buttonDersSayacRenk.Click += renkButonunaTiklandi;
        // 
        // buttonTeneffusSayacRenk
        // 
        buttonTeneffusSayacRenk.Location = new Point(3, 41);
        buttonTeneffusSayacRenk.Name = "buttonTeneffusSayacRenk";
        buttonTeneffusSayacRenk.Size = new Size(180, 32);
        buttonTeneffusSayacRenk.TabIndex = 4;
        buttonTeneffusSayacRenk.Text = "Teneffüs Sayacı Rengi";
        buttonTeneffusSayacRenk.UseVisualStyleBackColor = true;
        buttonTeneffusSayacRenk.Click += renkButonunaTiklandi;
        // 
        // buttonArkaPlanRenk
        // 
        buttonArkaPlanRenk.Location = new Point(3, 79);
        buttonArkaPlanRenk.Name = "buttonArkaPlanRenk";
        buttonArkaPlanRenk.Size = new Size(180, 32);
        buttonArkaPlanRenk.TabIndex = 5;
        buttonArkaPlanRenk.Text = "Arka Plan Rengi";
        buttonArkaPlanRenk.UseVisualStyleBackColor = true;
        buttonArkaPlanRenk.Click += renkButonunaTiklandi;
        // 
        // buttonKaydet
        // 
        buttonKaydet.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
        buttonKaydet.Location = new Point(164, 296);
        buttonKaydet.Name = "buttonKaydet";
        buttonKaydet.Size = new Size(96, 32);
        buttonKaydet.TabIndex = 6;
        buttonKaydet.Text = "Kaydet";
        buttonKaydet.UseVisualStyleBackColor = true;
        buttonKaydet.Click += buttonKaydet_Click;
        // 
        // buttonIptal
        // 
        buttonIptal.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
        buttonIptal.Location = new Point(266, 296);
        buttonIptal.Name = "buttonIptal";
        buttonIptal.Size = new Size(96, 32);
        buttonIptal.TabIndex = 7;
        buttonIptal.Text = "İptal";
        buttonIptal.UseVisualStyleBackColor = true;
        buttonIptal.Click += buttonIptal_Click;
        // 
        // labelKritikSure
        // 
        labelKritikSure.AutoSize = true;
        labelKritikSure.Location = new Point(24, 20);
        labelKritikSure.Name = "labelKritikSure";
        labelKritikSure.Size = new Size(170, 15);
        labelKritikSure.TabIndex = 8;
        labelKritikSure.Text = "Kritik süre (saniye, uyarı sınırı)";
        // 
        // labelSayacFont
        // 
        labelSayacFont.AutoSize = true;
        labelSayacFont.Location = new Point(24, 60);
        labelSayacFont.Name = "labelSayacFont";
        labelSayacFont.Size = new Size(119, 15);
        labelSayacFont.TabIndex = 9;
        labelSayacFont.Text = "Sayaç font boyutu";
        // 
        // labelSaatFont
        // 
        labelSaatFont.AutoSize = true;
        labelSaatFont.Location = new Point(24, 100);
        labelSaatFont.Name = "labelSaatFont";
        labelSaatFont.Size = new Size(150, 15);
        labelSaatFont.TabIndex = 10;
        labelSaatFont.Text = "Saat aralığı font boyutu";
        // 
        // renkPaneli
        // 
        renkPaneli.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
        renkPaneli.FlowDirection = FlowDirection.TopDown;
        renkPaneli.Location = new Point(24, 138);
        renkPaneli.Name = "renkPaneli";
        renkPaneli.Size = new Size(338, 132);
        renkPaneli.WrapContents = false;
        renkPaneli.TabIndex = 11;
        renkPaneli.Controls.Add(buttonDersSayacRenk);
        renkPaneli.Controls.Add(buttonTeneffusSayacRenk);
        renkPaneli.Controls.Add(buttonArkaPlanRenk);
        // 
        // SettingsForm
        // 
        AutoScaleDimensions = new SizeF(7F, 15F);
        AutoScaleMode = AutoScaleMode.Font;
        ClientSize = new Size(384, 351);
        AcceptButton = buttonKaydet;
        CancelButton = buttonIptal;
        Controls.Add(renkPaneli);
        Controls.Add(labelSaatFont);
        Controls.Add(labelSayacFont);
        Controls.Add(labelKritikSure);
        Controls.Add(buttonIptal);
        Controls.Add(buttonKaydet);
        Controls.Add(numericSaatFont);
        Controls.Add(numericSayacFont);
        Controls.Add(numericKritikSure);
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        MinimizeBox = false;
        Name = "SettingsForm";
        ShowIcon = false;
        StartPosition = FormStartPosition.CenterParent;
        Text = "Ayarlar";
        ((System.ComponentModel.ISupportInitialize)numericKritikSure).EndInit();
        ((System.ComponentModel.ISupportInitialize)numericSayacFont).EndInit();
        ((System.ComponentModel.ISupportInitialize)numericSaatFont).EndInit();
        ResumeLayout(false);
        PerformLayout();
    }
}
