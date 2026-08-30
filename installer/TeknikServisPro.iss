#define MyAppName "Teknik Servis Pro"
#define MyAppVersion "2.3.1"
#define MyAppPublisher "Teknik Servis Pro"
#define PythonExe "runtime\\py312_231\\pythonw.exe"

[Setup]
AppId={{E1239C99-6B63-4B71-A1E5-12395B9E2200}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\TeknikServisPro
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=..\release
OutputBaseFilename=TeknikServisPro_v2_3_1_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile=..\assets\TeknikServisPro.ico
UninstallDisplayIcon={app}\assets\TeknikServisPro.ico
CloseApplications=yes
RestartApplications=no

[InstallDelete]
; Eski PyInstaller/Node/VBS başlatıcılarını yeni Python runtime sürümünde temizle.
Type: files; Name: "{app}\TeknikServisPro.exe"
Type: files; Name: "{app}\baslat.vbs"
Type: files; Name: "{app}\baslat.cmd"
Type: files; Name: "{app}\start.ps1"
Type: files; Name: "{app}\server.js"
Type: files; Name: "{app}\package.json"
Type: filesandordirs; Name: "{app}\node_modules"

[Files]
Source: "..\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "db.json"
Source: "..\dist\db.json"; DestDir: "{app}"; Flags: onlyifdoesntexist

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayolu oluştur"; GroupDescription: "Ek görevler:"; Flags: checkedonce

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#PythonExe}"; Parameters: """{app}\server.py"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\TeknikServisPro.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#PythonExe}"; Parameters: """{app}\server.py"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\TeknikServisPro.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#PythonExe}"; Parameters: """{app}\server.py"""; WorkingDir: "{app}"; Description: "Teknik Servis Pro'yu başlat"; Flags: nowait postinstall skipifsilent

[Code]
procedure StopOldTechnicalService;
var
  ResultCode: Integer;
begin
  { v2.3.1 ve sonraki sürümler: önce yerel sunucudan temiz kapanış iste. }
  if FileExists(ExpandConstant('{sys}\curl.exe')) then
    Exec(ExpandConstant('{sys}\curl.exe'), '-s -X POST http://127.0.0.1:8972/api/shutdown', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

  Sleep(900);

  { v2.3.0 PyInstaller sürümünden yükseltme için eski uygulamayı kapat. }
  Exec(ExpandConstant('{sys}\taskkill.exe'), '/F /IM TeknikServisPro.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Sleep(500);
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  StopOldTechnicalService;
  Result := '';
end;
