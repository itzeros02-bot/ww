# 🚀 GitHub仓库推送指南

## 📋 项目信息

**项目名称**: 智能数据库查询工具
**项目路径**: `e:\kevin\作业\db_query\`
**目标仓库**: https://github.com/itzeros02-bot/ww.git

---

## 🔧 第一步：安装Git

### Windows系统安装Git

#### 方法一：下载安装（推荐）
1. **访问Git官网**: https://git-scm.com/download/win
2. **下载安装程序**: 点击下载Windows版本
3. **运行安装程序**:
   - 双击下载的 `.exe` 文件
   - 选择默认设置（推荐）
   - 点击"Install"安装
   - 完成后重启命令行

#### 方法二：使用包管理器
```powershell
# 使用Chocolatey安装
choco install git

# 或使用Scoop安装
scoop install git
```

### 验证安装
```powershell
git --version
# 应该显示: git version 2.x.x.x
```

---

## 🌐 第二步：配置Git

### 设置用户信息
```powershell
cd "e:\kevin\作业\db_query"
git config --global user.name "itzeros02-bot"
git config --global user.email "itzeros02-bot@users.noreply.github.com"
```

### 验证配置
```powershell
git config --list
```

---

## 📁 第三步：初始化Git仓库

### 创建.gitignore文件
```powershell
cd "e:\kevin\作业\db_query"

# 创建.gitignore文件
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
ENV/
env/
.venv

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Vite
dist/
dist-ssr/
*.local

# Editor
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log

# Export files (optional - remove if you want to track exports)
exports/*.csv
exports/*.json
exports/*.xlsx
!exports/.gitkeep

# Environment
.env
.env.local
.env.*.local
"@ | Out-File -FilePath .gitignore -Encoding utf8
```

### 初始化仓库
```powershell
cd "e:\kevin\作业\db_query"
git init
```

---

## ➕ 第四步：添加文件到Git

### 添加所有文件
```powershell
cd "e:\kevin\作业\db_query"
git add .
```

### 查看状态
```powershell
git status
```

### 查看将要提交的文件
```powershell
git diff --cached --name-only
```

---

## 📝 第五步：创建首次提交

### 创建提交
```powershell
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
```

---

## 🌐 第六步：连接到GitHub仓库

### 添加远程仓库
```powershell
cd "e:\kevin\作业\db_query"
git remote add origin https://github.com/itzeros02-bot/ww.git
```

### 验证远程仓库
```powershell
git remote -v
```

### 如果远程仓库已存在，先删除
```powershell
git remote remove origin
git remote add origin https://github.com/itzeros02-bot/ww.git
```

---

## 🚀 第七步：推送到GitHub

### 推送到主分支
```powershell
cd "e:\kevin\作业\db_query"
git branch -M main
git push -u origin main
```

### 如果遇到认证问题
GitHub现在需要个人访问令牌(Personal Access Token)：

1. **生成GitHub Token**:
   - 访问：https://github.com/settings/tokens
   - 点击"Generate new token (classic)"
   - 选择权限：`repo` (完整仓库访问权限)
   - 点击"Generate token"
   - 复制生成的token

2. **使用Token推送**:
```powershell
# 推送时会提示输入用户名和密码
# 用户名：itzeros02-bot
# 密码：[粘贴你的GitHub Token]
```

---

## 🔄 第八步：验证推送成功

### 检查GitHub仓库
访问：https://github.com/itzeros02-bot/ww

### 查看提交历史
```powershell
git log --oneline
```

### 查看远程分支
```powershell
git branch -r
```

---

## 📋 完整操作脚本

### 一键执行脚本
```powershell
# 设置项目路径
$projectPath = "e:\kevin\作业\db_query"

# 切换到项目目录
cd $projectPath

# 1. 配置Git
git config --global user.name "itzeros02-bot"
git config --global user.email "itzeros02-bot@users.noreply.github.com"

# 2. 创建.gitignore
@"
__pycache__/
*.py[cod]
*.so
node_modules/
dist/
*.log
.DS_Store
*.db
exports/
.env
"@ | Out-File -FilePath .gitignore -Encoding utf8

# 3. 初始化仓库
git init

# 4. 添加所有文件
git add .

# 5. 创建提交
git commit -m "🎉 初始提交：智能数据库查询工具

- 数据库连接管理
- SQL查询执行与导出
- 智能自动化分析
- AI助手建议系统
- React前端 + FastAPI后端
"

# 6. 添加远程仓库
git remote add origin https://github.com/itzeros02-bot/ww.git

# 7. 推送到GitHub
git branch -M main
git push -u origin main

Write-Host "✅ 推送完成！"
```

---

## 🛠️ 常见问题解决

### 问题1：SSL证书错误
```powershell
# 临时禁用SSL验证（不推荐生产环境）
git config --global http.sslVerify false
```

### 问题2：代理设置
```powershell
# 如果使用代理
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy http://proxy.example.com:8080
```

### 问题3：远程仓库已存在
```powershell
# 强制推送（谨慎使用）
git push -u origin main --force
```

### 问题4：大文件推送失败
```powershell
# 安装Git Large File Storage
# 下载：https://git-lfs.github.com/
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"
```

---

## 🎯 后续操作指南

### 日常开发流程
```powershell
# 1. 修改文件后查看状态
git status

# 2. 添加修改的文件
git add .
# 或添加特定文件
git add specific_file.py

# 3. 提交修改
git commit -m "描述你的修改"

# 4. 推送到GitHub
git push
```

### 创建新分支
```powershell
# 创建并切换到新分支
git checkout -b feature/new-feature

# 在新分支上工作...
git add .
git commit -m "Add new feature"

# 推送新分支
git push -u origin feature/new-feature
```

### 拉取最新代码
```powershell
# 从远程拉取最新代码
git pull origin main
```

---

## 📊 项目文件清单

### 后端文件
- backend/app/services/export.py (导出服务)
- backend/app/services/automation.py (自动化服务)
- backend/app/api/v1/automation.py (自动化API)
- backend/app/api/v1/queries.py (查询API - 已扩展)
- backend/app/main.py (应用入口 - 已修改)

### 前端文件
- frontend/src/pages/queries/execute.tsx (查询页面 - 已扩展)

### 文档文件
- FEATURE_EXPORT.md (功能设计文档)
- PROJECT_STRUCTURE.md (项目结构说明)
- AUTOMATION_SUMMARY.md (自动化功能总结)
- AI_ASSISTANT_TEST_GUIDE.md (AI助手测试指南)
- EXPORT_FUNCTIONALITY_FIXED.md (导出功能修复说明)

---

## 🎊 推送完成后检查清单

- [ ] 访问 https://github.com/itzeros02-bot/ww 确认仓库已创建
- [ ] 检查所有文件是否已上传
- [ ] 验证README.md是否显示正确
- [ ] 确认提交历史完整
- [ ] 测试仓库克隆功能

---

*按照本指南操作完成后，您的智能数据库查询工具项目将成功推送到GitHub仓库！*