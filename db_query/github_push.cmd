@echo off
REM GitHub推送脚本 - CMD版本
REM 此脚本在CMD环境中运行，支持交互式GitHub认证

echo ========================================
echo 智能数据库查询工具 - GitHub推送
echo ========================================
echo.

REM 切换到项目目录
cd /d "e:\kevin\作业\db_query"

echo 📁 项目目录: %CD%
echo.

REM 检查Git状态
echo 📋 当前Git状态:
git status --short
echo.

REM 检查远程仓库
echo 🌐 远程仓库配置:
git remote -v
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🔑 GitHub认证说明
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 推送到GitHub需要认证，请准备：
echo.
echo 📝 获取GitHub Personal Access Token:
echo 1. 访问: https://github.com/settings/tokens
echo 2. 点击: "Generate new token (classic)"
echo 3. 选择权限: repo (完整仓库访问权限)
echo 4. 点击: "Generate token" 并复制
echo.
echo 🔐 推送时将提示输入:
echo    用户名: itzeros02-bot
echo    密码: [粘贴您的GitHub Token]
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

pause

echo.
echo 🚀 开始推送到GitHub...
echo.

REM 推送到GitHub
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 推送成功！
    echo ========================================
    echo.
    echo 🌊 访问您的仓库: https://github.com/itzeros02-bot/ww
    echo.
    echo 🎉 智能数据库查询工具已成功推送到GitHub！
    echo.
    echo 📊 仓库内容：
    echo    - 完整后端服务代码
    echo    - 完整前端界面代码
    echo    - 所有功能文档和说明
    echo    - 自动化脚本和配置文件
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
    echo 1. 重新生成GitHub Token: https://github.com/settings/tokens
    echo 2. 检查网络连接
    echo 3. 确认仓库地址正确: https://github.com/itzeros02-bot/ww.git
    echo 4. 重新运行此脚本
    echo.
)

echo.
pause