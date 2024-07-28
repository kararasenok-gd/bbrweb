@echo off
echo "What do you want to do?"
echo "1 = Remove file"
echo "2 = Build"
set /p answer=
if "%answer%"=="1" (
    del bbrweb.spec
    rmdir dist /s /q
    rmdir build /s /q
)
if "%answer%"=="2" (
    python -m PyInstaller --noconfirm --onefile --console --name "bbrweb" "D:\Desktop\bbrweb\main.py"
)
pause
