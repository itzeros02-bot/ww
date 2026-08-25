@echo off
REM 智能数据库查询工具 - GitHub推送脚本
REM 使用方法：双击运行此脚本

echo ========================================
echo 智能数据库查询工具 - GitHub推送脚本
echo ========================================
echo.

REM 检查Git是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：系统未安装Git
    echo.
    echo 请按以下步骤安装Git：
    echo 1. 访问 https://git-scm.com/download/win
    echo 2. 下载并安装Git for Windows
    echo 3. 安装完成后重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo ✅ Git已安装
echo.

REM 设置项目路径
set PROJECT_PATH=e:\kevin\作业\db_query

REM 切换到项目目录
cd /d "%PROJECT_PATH%"

echo 📁 项目目录: %PROJECT_PATH%
echo.

REM 配置Git用户信息
echo 🔧 配置Git用户信息...
git config --global user.name "itzeros02-bot"
git config --global user.email "itzeros02-bot@users.noreply.github.com"

REM 创建.gitignore文件
echo 📝 创建.gitignore文件...
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo MANIFEST
echo.
echo # Virtual environments
echo venv/
echo ENV/
echo env/
echo .venv
echo.
echo # Node
echo node_modules/
echo npm-debug.log*
echo yarn-debug.log*
echo yarn-error.log*
echo .pnpm-debug.log*
echo.
echo # Vite
echo dist/
echo dist-ssr/
echo *.local
echo.
echo # Editor
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Database
echo *.db
echo *.sqlite
echo *.sqlite3
echo.
echo # Logs
echo logs/
echo *.log
echo.
echo # Export files
echo exports/*.csv
echo exports/*.json
echo exports/*.xlsx
echo !exports/.gitkeep
echo.
echo # Environment
echo .env
echo .env.local
echo .env.*.local
) > .gitignore

REM 初始化Git仓库
echo 🔄 初始化Git仓库...
if not exist ".git" (
    git init
    echo ✅ Git仓库初始化完成
) else (
    echo ℹ️  Git仓库已存在
)

REM 添加所有文件
echo ➕ 添加文件到Git...
git add .

REM 查看状态
echo 📋 Git状态:
git status --short

REM 创建提交
echo 📝 创建提交...
git commit -m "🎉 初始提交：智能数据库查询工具

功能特性：
- ✅ 数据库连接管理
- ✅ SQL查询执行
- ✅ 数据导出功能 (CSV, JSON, Excel)
- ✅ 智能自动化分析
- ✅ AI助手建议系统
- ✅ 一键查询+导出
- ✅ 前端React界面
- ✅ 后端FastAPI服务

技术栈：
- 后端：FastAPI + Python 3.9 + MySQL
- 前端：React + TypeScript + Ant Design + Vite
- AI工具：Claude Code

项目状态：✅ 完成并测试通过
"

REM 添加远程仓库
echo 🔗 连接到GitHub仓库...
git remote add origin https://github.com/itzeros02-bot/ww.git 2>nul
git remote set-url origin https://github.com/itzeros02-bot/ww.git

REM 设置主分支
git branch -M main

REM 推送到GitHub
echo 🚀 推送到GitHub...
echo.
echo ⚠️  如果需要认证，请输入：
echo    用户名：itzeros02-bot
echo    密码：[GitHub Personal Access Token]
echo.
echo 💡 获取Token：https://github.com/settings/tokens
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 推送成功！
    echo ========================================
    echo.
    echo 🌐 访问仓库：https://github.com/itzeros02-bot/ww
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ 推送失败
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. GitHub Token无效或过期
    echo 2. 网络连接问题
    echo 3. 仓库权限问题
    echo.
    echo 解决方法：
    echo 1. 生成新的GitHub Token
    echo 2. 检查网络连接
    echo 3. 确认仓库权限
    echo.
)

pause