@echo off
echo ===================================
echo 🚀 AI Landing Page Generator 시작
echo ===================================

REM .env 파일 체크
if not exist ".env" (
    echo ⚠️ .env 파일이 없습니다. 생성합니다...
    copy .env.example .env
    echo ❗ .env 파일에 ANTHROPIC_API_KEY를 설정해주세요!
    pause
    exit /b
)

REM 백엔드 의존성 설치
echo 📦 백엔드 패키지 확인 중...
cd backend
if not exist "node_modules" (
    echo 백엔드 패키지 설치 중...
    call npm install
) else (
    echo 백엔드 패키지 이미 설치됨 ✓
)

REM 프론트엔드 의존성 설치
echo 📦 프론트엔드 패키지 확인 중...
cd ..\frontend
if not exist "node_modules" (
    echo 프론트엔드 패키지 설치 중...
    call npm install
) else (
    echo 프론트엔드 패키지 이미 설치됨 ✓
)

REM 서버 시작
echo ===================================
echo 🔥 서버를 시작합니다...
echo ===================================

REM 백엔드 시작 (새 창에서)
cd ..\backend
start "Backend Server" cmd /k npm run dev

REM 3초 대기
timeout /t 3 /nobreak > nul

REM 프론트엔드 시작 (새 창에서)
cd ..\frontend
start "Frontend Server" cmd /k npm run dev

echo ===================================
echo ✅ 모든 서버가 시작되었습니다!
echo ===================================
echo.
echo 🌐 프론트엔드: http://localhost:5173
echo 🔧 백엔드 API: http://localhost:3001
echo.
echo 브라우저에서 http://localhost:5173 을 열어주세요.
echo.
pause