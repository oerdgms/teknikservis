#define MyAppName "Teknik Servis Pro"
#define MyAppVersion "2.3.6"
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
OutputBaseFilename=TeknikServisPro_v2_3_6_Setup
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
Source: "dist\TeknikServisPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\Teknik Servis Pro"; Filename: "{app}\TeknikServisPro.exe"; WorkingDir: "{app}"
Name: "{userprograms}\Teknik Servis Pro"; Filename: "{app}\TeknikServisPro.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\TeknikServisPro.exe"; Description: "Teknik Servis Pro'yu başlat"; Flags: nowait postinstall skipifsilent
