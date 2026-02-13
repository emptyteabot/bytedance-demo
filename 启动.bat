@echo off
echo ========================================
echo   Project Aegis - 启动脚本
echo   TikTok Shop 风控中台 MVP
echo ========================================
echo.

echo [1/3] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/3] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告: 部分依赖安装失败，尝试继续运行...
)
echo.

echo [3/3] 启动 Streamlit 应用...
echo.
echo ========================================
echo   应用将在浏览器中自动打开
echo   访问地址: http://localhost:8501
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

streamlit run app.py

pause
