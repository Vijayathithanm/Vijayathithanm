; Inno Setup script for MagnetFlux Studio (Milestone 6).
; Compile with the Inno Setup Compiler (iscc packaging/installer.iss) after
; building the one-folder app with PyInstaller (see packaging/magnetflux.spec).

#define AppName "MagnetFlux Studio"
#define AppVersion "0.6.0"
#define AppPublisher "MagnetFlux"
#define AppExeName "MagnetFluxStudio.exe"

[Setup]
AppId={{7C4E9D2A-3B1F-4E6A-9C8D-MAGNETFLUX01}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=..\dist
OutputBaseFilename=MagnetFluxStudio-{#AppVersion}-setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
; PyInstaller one-folder output goes in dist\MagnetFluxStudio.
Source: "..\dist\MagnetFluxStudio\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent
