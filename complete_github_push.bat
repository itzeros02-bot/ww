@echo off
REM GitHub推送完成脚本 - 使用Token认证

echo ========================================
echo GitHub推送完成脚本
echo ========================================
echo.

echo ✅ 前期工作已完成：
echo    - Git仓库初始化
echo    - 所有文件已提交
echo    - 远程仓库已配置
echo.

echo 🔑 现在需要GitHub Token完成最后一步
echo.

REM 检查是否在正确的目录
cd /d "e:\kevin\作业\db_query"

if not exist ".git" (
    echo ❌ 错误：不是Git仓库目录
    pause
    exit /b 1
)

echo 📋 请按以下步骤操作：
echo.
echo 1. 访问GitHub Token页面：
echo    https://github.com/settings/tokens
echo.
echo 2. 点击 "Generate new token (classic)"
echo.
echo 3. 选择权限：repo (完整仓库访问权限)
echo.
echo 4. 点击 "Generate token" 并复制Token
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

set /p TOKEN="请粘贴您的GitHub Token: "

if "%TOKEN%"=="" (
    echo ❌ Token不能为空
    pause
    exit /b 1
)

echo.
echo 🔧 配置Git使用Token认证...

REM 使用Token设置远程URL
git remote set-url origin https://%TOKEN%@github.com/itzeros02-bot/ww.git

echo ✅ 远程URL已配置
echo.

echo 🚀 开始推送到GitHub...
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 推送成功！
    echo ========================================
    echo.
    echo 🌊 访问仓库：https://github.com/itzeros02-bot/ww
    echo.
    echo 🎉 智能数据库查询工具已成功推送到GitHub！
    echo.
    echo 📊 仓库包含：
    echo    - 完整后端服务代码
    echo    - 完整前端界面代码
    echo    - 所有功能文档
    echo    - 自动化脚本
    echo.

    REM 重置远程URL为标准格式（移除Token）
    git remote set-url origin https://github.com/itzeros02-bot/ww.git
    echo 🔒 远程URL已重置为安全格式

) else (
    echo.
    echo ========================================
    echo ❌ 推送失败
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. Token无效或过期
    echo 2. 网络连接问题
    echo 3. 仓库权限问题
    echo.
    echo 解决方法：
    echo 1. 检查Token是否正确复制
    echo 2. 重新生成Token：https://github.com/settings/tokens
    echo 3. 确认仓库地址：https://github.com/itzeros02-bot/ww.git
    echo.

    REM 重置远程URL
    git remote set-url origin https://github.com/itzeros02-bot/ww.git
)

echo.
pause