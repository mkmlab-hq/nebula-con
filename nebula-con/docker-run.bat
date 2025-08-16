@echo off
chcp 65001 >nul
echo 🚀 NebulaCon 도커 환경을 시작합니다...

echo 📦 도커 이미지를 빌드합니다...
docker-compose build

echo 🔧 개발 서비스를 시작합니다...
docker-compose up -d nebula-con

echo 📊 Jupyter 노트북을 시작합니다...
docker-compose up -d jupyter

echo ✅ 모든 서비스가 시작되었습니다!
echo.
echo 🌐 개발 서버: http://localhost:8000
echo 📊 Jupyter 노트북: http://localhost:8888
echo.
echo 📝 컨테이너에 접속하려면:
echo    docker exec -it nebula-con-dev bash
echo.
echo 🛑 서비스를 중지하려면:
echo    docker-compose down
echo.
echo 📋 실행 중인 서비스 확인:
echo    docker-compose ps
echo.
pause 