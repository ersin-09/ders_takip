using System.Drawing;
using System.Windows.Forms;

namespace DersTakipWin;

partial class MainForm
{
    /// <summary>
    ///  Required designer variable.
    /// </summary>
    private System.ComponentModel.IContainer? components = null;

    private Label labelBaslik;
    private Label labelDurumBaslik;
    private Label labelDurumIcerik;
    private Label labelKalanSureBaslik;
    private Label labelKalanSureIcerik;
    private ListView listViewProgram;
    private ColumnHeader columnDers;
    private ColumnHeader columnBaslangic;
    private ColumnHeader columnBitis;
    private Button buttonExcelYukle;
    private Button buttonKaydet;
    private Button buttonAyarlar;
    private Timer zamanlayici;
    private StatusStrip statusStrip1;
    private ToolStripStatusLabel toolStripDurum;

    /// <summary>
    ///  Clean up any resources being used.
    /// </summary>
    /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
    protected override void Dispose(bool disposing)
    {
        if (disposing && (components != null))
        {
            components.Dispose();
        }
        base.Dispose(disposing);
    }

    #region Windows Form Designer generated code

    private void InitializeComponent()
    {
        components = new System.ComponentModel.Container();
        labelBaslik = new Label();
        labelDurumBaslik = new Label();
        labelDurumIcerik = new Label();
        labelKalanSureBaslik = new Label();
        labelKalanSureIcerik = new Label();
        listViewProgram = new ListView();
        columnDers = new ColumnHeader();
        columnBaslangic = new ColumnHeader();
        columnBitis = new ColumnHeader();
        buttonExcelYukle = new Button();
        buttonKaydet = new Button();
        buttonAyarlar = new Button();
        zamanlayici = new Timer(components);
        statusStrip1 = new StatusStrip();
        toolStripDurum = new ToolStripStatusLabel();
        statusStrip1.SuspendLayout();
        SuspendLayout();
        // 
        // labelBaslik
        // 
        labelBaslik.AutoSize = true;
        labelBaslik.Font = new Font("Segoe UI", 16F, FontStyle.Bold, GraphicsUnit.Point);
        labelBaslik.ForeColor = Color.White;
        labelBaslik.Location = new Point(24, 20);
        labelBaslik.Name = "labelBaslik";
        labelBaslik.Size = new Size(244, 30);
        labelBaslik.TabIndex = 0;
        labelBaslik.Text = "Ders Takip Uygulaması";
        // 
        // labelDurumBaslik
        // 
        labelDurumBaslik.AutoSize = true;
        labelDurumBaslik.Font = new Font("Segoe UI", 10F, FontStyle.Bold, GraphicsUnit.Point);
        labelDurumBaslik.ForeColor = Color.WhiteSmoke;
        labelDurumBaslik.Location = new Point(26, 74);
        labelDurumBaslik.Name = "labelDurumBaslik";
        labelDurumBaslik.Size = new Size(91, 19);
        labelDurumBaslik.TabIndex = 1;
        labelDurumBaslik.Text = "Aktif Durum";
        // 
        // labelDurumIcerik
        // 
        labelDurumIcerik.AutoSize = true;
        labelDurumIcerik.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
        labelDurumIcerik.ForeColor = Color.FromArgb(0, 204, 255);
        labelDurumIcerik.Location = new Point(26, 100);
        labelDurumIcerik.Name = "labelDurumIcerik";
        labelDurumIcerik.Size = new Size(268, 21);
        labelDurumIcerik.TabIndex = 2;
        labelDurumIcerik.Text = "Herhangi bir ders bilgisi bulunamadı";
        // 
        // labelKalanSureBaslik
        // 
        labelKalanSureBaslik.AutoSize = true;
        labelKalanSureBaslik.Font = new Font("Segoe UI", 10F, FontStyle.Bold, GraphicsUnit.Point);
        labelKalanSureBaslik.ForeColor = Color.WhiteSmoke;
        labelKalanSureBaslik.Location = new Point(26, 138);
        labelKalanSureBaslik.Name = "labelKalanSureBaslik";
        labelKalanSureBaslik.Size = new Size(83, 19);
        labelKalanSureBaslik.TabIndex = 3;
        labelKalanSureBaslik.Text = "Kalan Süre";
        // 
        // labelKalanSureIcerik
        // 
        labelKalanSureIcerik.AutoSize = true;
        labelKalanSureIcerik.Font = new Font("Segoe UI", 24F, FontStyle.Bold, GraphicsUnit.Point);
        labelKalanSureIcerik.ForeColor = Color.FromArgb(204, 255, 0);
        labelKalanSureIcerik.Location = new Point(22, 160);
        labelKalanSureIcerik.Name = "labelKalanSureIcerik";
        labelKalanSureIcerik.Size = new Size(168, 45);
        labelKalanSureIcerik.TabIndex = 4;
        labelKalanSureIcerik.Text = "00:00:00";
        // 
        // listViewProgram
        // 
        listViewProgram.Columns.AddRange(new ColumnHeader[] { columnDers, columnBaslangic, columnBitis });
        listViewProgram.FullRowSelect = true;
        listViewProgram.GridLines = true;
        listViewProgram.HeaderStyle = ColumnHeaderStyle.Nonclickable;
        listViewProgram.HideSelection = false;
        listViewProgram.Location = new Point(24, 224);
        listViewProgram.Name = "listViewProgram";
        listViewProgram.Size = new Size(520, 248);
        listViewProgram.TabIndex = 5;
        listViewProgram.UseCompatibleStateImageBehavior = false;
        listViewProgram.View = View.Details;
        // 
        // columnDers
        // 
        columnDers.Text = "Ders";
        columnDers.Width = 240;
        // 
        // columnBaslangic
        // 
        columnBaslangic.Text = "Başlangıç";
        columnBaslangic.Width = 120;
        // 
        // columnBitis
        // 
        columnBitis.Text = "Bitiş";
        columnBitis.Width = 120;
        // 
        // buttonExcelYukle
        // 
        buttonExcelYukle.Location = new Point(568, 224);
        buttonExcelYukle.Name = "buttonExcelYukle";
        buttonExcelYukle.Size = new Size(160, 40);
        buttonExcelYukle.TabIndex = 6;
        buttonExcelYukle.Text = "Excel'den Yükle";
        buttonExcelYukle.UseVisualStyleBackColor = true;
        buttonExcelYukle.Click += buttonExcelYukle_Click;
        // 
        // buttonKaydet
        // 
        buttonKaydet.Location = new Point(568, 276);
        buttonKaydet.Name = "buttonKaydet";
        buttonKaydet.Size = new Size(160, 40);
        buttonKaydet.TabIndex = 7;
        buttonKaydet.Text = "Programı Kaydet";
        buttonKaydet.UseVisualStyleBackColor = true;
        buttonKaydet.Click += buttonKaydet_Click;
        // 
        // buttonAyarlar
        // 
        buttonAyarlar.Location = new Point(568, 328);
        buttonAyarlar.Name = "buttonAyarlar";
        buttonAyarlar.Size = new Size(160, 40);
        buttonAyarlar.TabIndex = 8;
        buttonAyarlar.Text = "Görsel Ayarlar";
        buttonAyarlar.UseVisualStyleBackColor = true;
        buttonAyarlar.Click += buttonAyarlar_Click;
        // 
        // zamanlayici
        // 
        zamanlayici.Interval = 1000;
        zamanlayici.Tick += zamanlayici_Tick;
        // 
        // statusStrip1
        // 
        statusStrip1.Items.AddRange(new ToolStripItem[] { toolStripDurum });
        statusStrip1.Location = new Point(0, 492);
        statusStrip1.Name = "statusStrip1";
        statusStrip1.Size = new Size(754, 22);
        statusStrip1.SizingGrip = false;
        statusStrip1.TabIndex = 9;
        statusStrip1.Text = "statusStrip1";
        // 
        // toolStripDurum
        // 
        toolStripDurum.Name = "toolStripDurum";
        toolStripDurum.Size = new Size(182, 17);
        toolStripDurum.Text = "Veri dosyası konumu hazırlanıyor";
        // 
        // MainForm
        // 
        AutoScaleDimensions = new SizeF(7F, 15F);
        AutoScaleMode = AutoScaleMode.Font;
        BackColor = Color.FromArgb(37, 37, 38);
        ClientSize = new Size(754, 514);
        Controls.Add(statusStrip1);
        Controls.Add(buttonAyarlar);
        Controls.Add(buttonKaydet);
        Controls.Add(buttonExcelYukle);
        Controls.Add(listViewProgram);
        Controls.Add(labelKalanSureIcerik);
        Controls.Add(labelKalanSureBaslik);
        Controls.Add(labelDurumIcerik);
        Controls.Add(labelDurumBaslik);
        Controls.Add(labelBaslik);
        DoubleBuffered = true;
        FormBorderStyle = FormBorderStyle.FixedSingle;
        MaximizeBox = false;
        Name = "MainForm";
        StartPosition = FormStartPosition.CenterScreen;
        Text = "Ders Takip";
        Load += MainForm_Load;
        statusStrip1.ResumeLayout(false);
        statusStrip1.PerformLayout();
        ResumeLayout(false);
        PerformLayout();
    }

    #endregion
}
