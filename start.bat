@echo off
chcp 65001 >nul
title 实习报告系统 - 后端服务

cd /d "%~dp0"

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请安装 Python 并加入 PATH
    pause
    exit /b 1
)

:: 检查 Django 是否安装
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
    echo [完成] 依赖安装成功
    echo.
)

:: 检查数据库，不存在则初始化
if not exist "db.sqlite3" (
    echo [初始化] 数据库不存在，正在初始化...
    python init_data.py
    if errorlevel 1 (
        echo [错误] 数据初始化失败
        pause
        exit /b 1
    )
    echo [完成] 数据初始化成功
    echo.
)

:: 启动 Django 开发服务器
echo.
echo ====================================
echo  专业实习报告系统
echo.
echo  访问地址: http://127.0.0.1:8000
echo  管理员账号: admin / admin123
echo.
echo  按 Ctrl+C 停止服务
echo ====================================
echo.

python manage.py runserver 0.0.0.0:8000

echo.
echo [提示] 服务已停止
pause
