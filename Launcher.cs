using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

internal static class Program
{
    [STAThread]
    private static void Main()
    {
        try
        {
            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            string script = Path.Combine(baseDir, "launcher.ps1");
            if (!File.Exists(script))
            {
                MessageBox.Show("Başlatma dosyası bulunamadı. Kurulumu yeniden yapın.", "Teknik Servis Pro", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            var psi = new ProcessStartInfo
            {
                FileName = "powershell.exe",
                Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"" + script + "\"",
                WorkingDirectory = baseDir,
                UseShellExecute = false,
                CreateNoWindow = true,
                WindowStyle = ProcessWindowStyle.Hidden
            };
            Process.Start(psi);
        }
        catch (Exception ex)
        {
            MessageBox.Show("Teknik Servis Pro başlatılamadı.\n\n" + ex.Message, "Teknik Servis Pro", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
