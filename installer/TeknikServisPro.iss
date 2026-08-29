#define MyAppName "Teknik Servis Pro"
#define MyAppVersion "2.2.2"
#define MyAppPublisher "Teknik Servis Pro"
#define MyAppExeName "TeknikServisPro.exe"

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
OutputBaseFilename=TeknikServisPro_v2_2_2_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile=..\assets\TeknikServisPro.ico
UninstallDisplayIcon={app}\assets\TeknikServisPro.ico

[Files]
Source: "..\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "db.json"
Source: "..\dist\db.json"; DestDir: "{app}"; Flags: onlyifdoesntexist

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayolu oluştur"; GroupDescription: "Ek görevler:"; Flags: checkedonce

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\TeknikServisPro.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\TeknikServisPro.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Teknik Servis Pro'yu başlat"; Flags: nowait postinstall skipifsilent
