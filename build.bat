@echo off
echo "What do you want to do?"
echo "1 = Remove file"
echo "2 = Build"
echo "3 = Rebuild"
set /p answer=
if "%answer%"=="1" (
    echo "Removing files..."
    del bbrweb.spec
    rmdir dist /s /q
    rmdir build /s /q
    echo "Removed files."
)
if "%answer%"=="2" (
    echo "Building..."
    python -m PyInstaller --noconfirm --onefile --console --name "bbrweb" "D:\Desktop\bbrweb\main.py"
    echo "Builded"
)
if "%answer%"=="3" (
    echo "Rebuilding..."
    echo "Removing files..."
    del bbrweb.spec
    rmdir dist /s /q
    rmdir build /s /q
    echo "Removed files. Building..."
    python -m PyInstaller --noconfirm --onefile --console --name "bbrweb" "D:\Desktop\bbrweb\main.py"
    echo "Builded"
)
