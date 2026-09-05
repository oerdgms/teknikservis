#define MyAppName "Teknik Servis Pro"
#define MyAppVersion "2.6.4.1"
#define MyAppPublisher "Teknik Servis Pro"
#define MyAppExeName "TeknikServisPro.exe"

[Setup]
AppId={{E1239C99-6B63-4B71-A1E5-12395B9E2200}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\TeknikServisPro
DefaultGroupName={#MyAppName}
OutputDir=release
OutputBaseFilename=TeknikServisPro_v2_6_4_Setup
SetupIconFile=app\assets\TeknikServisPro.ico
UninstallDisplayIcon={app}\TeknikServisPro.exe
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Files]
; v2.6.4 Hotfix3: Canlı veritabanı kurulum klasöründe değildir.
; PyInstaller onedir çıktısının tamamını (_internal içindeki seed db.json dahil) kopyala.
; Kullanıcı verisi %LOCALAPPDATA%\TeknikServisPro\Data altında korunur.
Source: "dist\TeknikServisPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\Teknik Servis Pro"; Filename: "{app}\TeknikServisPro.exe"; WorkingDir: "{app}"
Name: "{userprograms}\Teknik Servis Pro"; Filename: "{app}\TeknikServisPro.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\TeknikServisPro.exe"; Description: "Teknik Servis Pro'yu başlat"; Flags: nowait postinstall skipifsilent

[Code]
function IsPortOpen: Boolean;
var
  ResultCode: Integer;
  PS: String;
begin
  { Yalnızca localhost health endpoint'ini kontrol eder. }
  PS := '-NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "try { $r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 http://127.0.0.1:8972/api/health; if($r.StatusCode -eq 200){exit 0}else{exit 1} } catch { exit 1 }"';
  Result := Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'), PS, '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
end;

procedure RequestGracefulShutdown;
var
  ResultCode: Integer;
  PS: String;
begin
  { taskkill yok: çalışan uygulamanın kendi localhost shutdown API'sine kontrollü istek. }
  PS := '-NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -UseBasicParsing -Method POST -ContentType ''application/json'' -Body ''{}'' -TimeoutSec 2 http://127.0.0.1:8972/api/shutdown | Out-Null } catch {}"';
  Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'), PS, '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  I: Integer;
begin
  Result := '';
  if IsPortOpen then
  begin
    WizardForm.StatusLabel.Caption := 'Çalışan Teknik Servis Pro güvenli şekilde kapatılıyor...';
    RequestGracefulShutdown;
    for I := 1 to 24 do
    begin
      Sleep(500);
      if not IsPortOpen then
      begin
        Result := '';
        exit;
      end;
    end;
    Result := 'Teknik Servis Pro halen çalışıyor. Programı ve açık Teknik Servis Pro pencerelerini kapatıp kurulumu yeniden başlatın. Verileriniz korunmuştur.';
  end;
end;
