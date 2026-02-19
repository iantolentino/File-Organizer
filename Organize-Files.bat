@echo off
setlocal EnableDelayedExpansion

echo ================================
echo   FILE ORGANIZER - AUTO MODE
echo ================================
echo.

cd /d "%~dp0"

:: Create folders
for %%d in (Images Documents Videos Audio Archives Scripts Others) do (
    if not exist "%%d" mkdir "%%d"
)

echo Organizing files...
echo.

:: Process files safely
for /f "delims=" %%F in ('dir /b /a-d') do (

    :: Skip the script itself
    if /I not "%%F"=="%~nx0" (

        set "ext=%%~xF"
        set "dest=Others"

        :: IMAGES
        if /I "!ext!"==".jpg"  set dest=Images
        if /I "!ext!"==".jpeg" set dest=Images
        if /I "!ext!"==".png"  set dest=Images
        if /I "!ext!"==".gif"  set dest=Images
        if /I "!ext!"==".bmp"  set dest=Images
        if /I "!ext!"==".webp" set dest=Images

        :: DOCUMENTS
        if /I "!ext!"==".pdf"  set dest=Documents
        if /I "!ext!"==".doc"  set dest=Documents
        if /I "!ext!"==".docx" set dest=Documents
        if /I "!ext!"==".xls"  set dest=Documents
        if /I "!ext!"==".xlsx" set dest=Documents
        if /I "!ext!"==".txt"  set dest=Documents
        if /I "!ext!"==".csv"  set dest=Documents

        :: VIDEOS
        if /I "!ext!"==".mp4" set dest=Videos
        if /I "!ext!"==".mkv" set dest=Videos
        if /I "!ext!"==".avi" set dest=Videos

        :: AUDIO
        if /I "!ext!"==".mp3" set dest=Audio
        if /I "!ext!"==".wav" set dest=Audio

        :: ARCHIVES
        if /I "!ext!"==".zip" set dest=Archives
        if /I "!ext!"==".rar" set dest=Archives
        if /I "!ext!"==".7z"  set dest=Archives

        :: SCRIPTS
        if /I "!ext!"==".py"   set dest=Scripts
        if /I "!ext!"==".js"   set dest=Scripts
        if /I "!ext!"==".html" set dest=Scripts
        if /I "!ext!"==".css"  set dest=Scripts
        if /I "!ext!"==".bat"  set dest=Scripts

        move "%%F" "!dest!\" >nul

        echo Moved: %%F → !dest!

    )
)

echo.
echo ✅ ALL FILES ORGANIZED SUCCESSFULLY!
echo.
pause
