@echo off
REM 智能数据库查询工具 - 完整Git安装和推送脚本
REM 此脚本将自动安装Git并推送代码到GitHub

echo ========================================
echo 智能数据库查询工具 - GitHub推送工具
echo ========================================
echo.

REM 检查Git是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔧 检测到Git未安装，开始自动安装...
    echo.

    REM 检查是否有 Chocolatey
    choco --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ 使用Chocolatey安装Git...
        choco install git -y
    ) else (
        echo 📥 正在下载Git安装程序...
        powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/latest/download/Git-for-Windows-Setup.exe' -OutFile '%TEMP%\git-installer.exe'"
        echo 🚀 启动Git安装程序...
        start /wait %TEMP%\git-installer.exe
    )

    echo.
    echo ✅ Git安装完成，请重新运行此脚本
    pause
    exit /b 0
)

echo ✅ Git已安装
git --version
echo.

REM 设置项目路径
set PROJECT_PATH=e:\kevin\作业\db_query

REM 切换到项目目录
cd /d "%PROJECT_PATH%"

if not exist "%PROJECT_PATH%" (
    echo ❌ 错误：项目目录不存在: %PROJECT_PATH%
    pause
    exit /b 1
)

echo 📁 项目目录: %PROJECT_PATH%
echo.

REM 配置Git用户信息
echo 🔧 配置Git用户信息...
git config --global user.name "itzeros02-bot"
git config --global user.email "itzeros02-bot@users.noreply.github.com"
git config --global init.defaultbranch main
git config --global core.autocrlf false

echo ✅ Git配置完成
echo.

REM 创建.gitignore文件
echo 📝 创建.gitignore文件...
if exist .gitignore (
    echo ℹ️  .gitignore文件已存在
) else (
    (
echo # Python
echo __pycache__/
echo *.py[cod]
echo *.so
echo *.pyo
echo *.pyd
echo Python
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
echo env.bak/
echo venv.bak/
echo.
echo # Node modules
echo node_modules/
echo npm-debug.log*
echo yarn-debug.log*
echo yarn-error.log*
echo pnpm-debug.log*
echo lerna-debug.log*
echo.
echo # React build
echo dist/
echo dist-ssr/
echo *.local
echo.
echo # Editor directories and files
echo .vscode/*
echo !.vscode/extensions.json
echo .idea
echo .DS_Store
echo *.suo
echo *.ntvs*
echo *.njsproj
echo *.sln
echo *.sw?
echo.
echo # OS
echo Thumbs.db
echo.
echo # Database files
echo *.db
echo *.sqlite
echo *.sqlite3
echo.
echo # Logs
echo logs/
echo *.log
echo npm-debug.log*
echo yarn-debug.log*
echo yarn-error.log*
echo pnpm-debug.log*
echo lerna-debug.log*
echo.
echo # Export files (临时文件，不需要版本控制)
echo exports/*.csv
echo exports/*.json
echo exports/*.xlsx
echo exports/*.xls
echo !exports/.gitkeep
echo.
echo # Environment variables
echo .env
echo .env.local
echo .env.development.local
echo .env.test.local
echo .env.production.local
echo.
echo # IDE
echo .code-workspace
echo *.code-workspace
    ) > .gitignore
    echo ✅ .gitignore文件创建完成
)

echo.
echo 🔄 初始化Git仓库...
if not exist ".git" (
    git init
    echo ✅ Git仓库初始化完成
) else (
    echo ℹ️  Git仓库已存在
)

echo.
echo ➕ 添加文件到Git...
git add .

echo.
echo 📋 Git状态预览:
git status --short

echo.
echo 📝 创建提交...
git commit -m "🎉 初始提交：智能数据库查询工具

功能特性：
- ✅ 数据库连接管理 (支持MySQL、PostgreSQL)
- ✅ SQL查询执行与结果展示
- ✅ 数据导出功能 (CSV、JSON、Excel格式)
- ✅ 智能自动化分析系统
- ✅ AI助手主动建议功能
- ✅ 一键查询+导出工作流
- ✅ 前端React界面 (TypeScript + Ant Design)
- ✅ 后端FastAPI服务 (Python 3.9)
- ✅ 自然语言转SQL功能
- ✅ 查询历史管理

技术栈：
- 后端：FastAPI + SQLModel + MySQL Connector
- 前端：React + TypeScript + Ant Design + Vite
- 数据库：MySQL + SQLite
- AI工具：Claude Code

核心创新：
- 🤖 AI助手主动询问：'需要将这次查询结果导出为 CSV 或 JSON 文件吗？'
- ⚡ 一键操作：查询+导出+自动下载
- 🧠 智能分析：查询特征识别和格式推荐
- 🎯 用户体验：加载反馈、成功提示、自动文件下载

项目状态：✅ 完成并测试通过
所有功能正常运行，可投入使用。

文档完善：
- FEATURE_EXPORT.md (功能设计文档)
- PROJECT_STRUCTURE.md (项目结构说明)
- GITHUB_PUSH_GUIDE.md (推送指南)
- AUTOMATION_SUMMARY.md (自动化功能总结)
- AI_ASSISTANT_TEST_GUIDE.md (AI助手测试指南)
"

if %errorlevel% neq 0 (
    echo.
    echo ❌ 提交创建失败，请检查是否有文件冲突
    echo.
    echo 尝试解决冲突：
    git status
    pause
    exit /b 1
)

echo ✅ 提交创建完成
echo.

echo 🔗 连接到GitHub仓库...
REM 删除现有远程仓库（如果存在）
git remote remove origin >nul 2>&1
REM 添加新的远程仓库
git remote add origin https://github.com/itzeros02-bot/ww.git

REM 验证远程仓库
git remote -v

echo.
echo 🚀 推送到GitHub...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ⚠️  认证信息说明
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo GitHub现在需要个人访问令牌(Personal Access Token)
echo.
echo 获取Token步骤：
echo 1. 访问：https://github.com/settings/tokens
echo 2. 点击："Generate new token (classic)"
echo 3. 选择权限：repo (完整仓库访问权限)
echo 4. 点击："Generate token"
echo 5. 复制生成的token (只显示一次！)
echo.
echo 推送时输入：
echo   用户名：itzeros02-bot
echo   密码：[粘贴你的GitHub Token]
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM 设置主分支名称
git branch -M main

REM 推送到GitHub
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 推送成功！
    echo ========================================
    echo.
    echo 🌊 访问仓库：https://github.com/itzeros02-bot/ww
    echo.
    echo 📊 仓库内容：
    echo    - 完整的后端服务代码
    echo    - 完整的前端界面代码
    echo    - 所有功能文档和说明
    echo    - 自动化脚本和配置文件
    echo.
    echo 🎉 智能数据库查询工具已成功推送到GitHub！
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
    echo 4. 认证信息输入错误
    echo.
    echo 解决方法：
    echo 1. 重新生成GitHub Token：https://github.com/settings/tokens
    echo 2. 检查网络连接
    echo 3. 确认仓库地址正确：https://github.com/itzeros02-bot/ww.git
    echo 4. 重新运行此脚本
    echo.
    echo 如需查看详细状态，运行：git status
)

echo.
pause