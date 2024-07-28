@echo off
echo "What do you want to do?"
echo "1 = Remove file"
echo "2"
set /p answer=
if "%answer%"=="y" (
    del bbrweb.spec
    echo "bbrweb.spec removed"
    rmdir dist /s /q
    echo "dist removed"
    rmdir build /s /q
    echo "build removed"
    echo "=============================="
    echo "Removed!"
)

python -m PyInstaller --noconfirm --onefile --console --name "bbrweb" "D:\Desktop\bbrweb\main.py"
pause
