@echo off
REM Инициализация git-репозитория, первый коммит и публикация на GitHub

REM 1. Инициализация git-репозитория (если не был инициализирован)
git init

REM 2. Добавление всех файлов
git add .

REM 3. Первый коммит
git commit -m "Initial public release: JustAnime Django project"

REM 4. Запросить у пользователя ссылку на репозиторий GitHub
set /p repo_url=Введите ссылку на ваш новый репозиторий GitHub (например, https://github.com/yourname/justAnime.git):

git remote add origin %repo_url%
git branch -M main
git push -u origin main

pause
