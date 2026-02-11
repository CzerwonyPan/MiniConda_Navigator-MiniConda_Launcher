!include "MUI2.nsh"

Name "MiniConda Navigator"
OutFile "MiniConda_Navigator_Setup.exe"
InstallDir "$PROGRAMFILES\MiniConda Navigator"
RequestExecutionLevel admin

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Polish"

Section "Main"
    SetOutPath "$INSTDIR"
    
    ; Pliki aplikacji
    File "dist\MiniConda_Navigator.exe"
    File "miniconda_settings.json"
    
    ; Utwórz skróty
    CreateDirectory "$SMPROGRAMS\MiniConda Navigator"
    CreateShortCut "$SMPROGRAMS\MiniConda Navigator\MiniConda Navigator.lnk" "$INSTDIR\MiniConda_Navigator.exe"
    CreateShortCut "$DESKTOP\MiniConda Navigator.lnk" "$INSTDIR\MiniConda_Navigator.exe"
    
    ; Zapisz do rejestru dla odinstalowania
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MiniCondaNavigator" \
        "DisplayName" "MiniConda Navigator"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MiniCondaNavigator" \
        "UninstallString" '"$INSTDIR\Uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MiniCondaNavigator" \
        "Publisher" "MiniConda Project"
    
    ; Utwórz uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    ; Usuń pliki
    Delete "$INSTDIR\MiniConda_Navigator.exe"
    Delete "$INSTDIR\miniconda_settings.json"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Usuń skróty
    Delete "$SMPROGRAMS\MiniConda Navigator\MiniConda Navigator.lnk"
    Delete "$DESKTOP\MiniConda Navigator.lnk"
    RMDir "$SMPROGRAMS\MiniConda Navigator"
    
    ; Usuń z rejestru
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MiniCondaNavigator"
    
    ; Usuń folder jeśli pusty
    RMDir "$INSTDIR"
SectionEnd