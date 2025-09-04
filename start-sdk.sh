#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🚀 SDK 기반 랜딩페이지 생성기           ║${NC}"
echo -e "${BLUE}║   로컬 파일 시스템 기반 동작               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# .env 파일 체크
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env 파일이 없습니다. .env.example에서 복사합니다...${NC}"
    cp .env.example .env
    echo -e "${RED}❗ .env 파일에 ANTHROPIC_API_KEY를 설정해주세요!${NC}"
    echo "설정 후 다시 실행해주세요."
    exit 1
fi

# API 키 체크
if grep -q "your-api-key-here" .env; then
    echo -e "${RED}❗ .env 파일에 실제 API 키를 입력해주세요!${NC}"
    exit 1
fi

# Python 체크
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3가 설치되어 있지 않습니다.${NC}"
    exit 1
fi

# 1. Python SDK 서버 시작
echo -e "${GREEN}1️⃣ Python SDK 서버 시작...${NC}"
cd sdk-server

# 가상환경이 없으면 생성
if [ ! -d "venv" ]; then
    echo "Python 가상환경 생성 중..."
    python3 -m venv venv
fi

# 가상환경 활성화 및 패키지 설치
source venv/bin/activate
pip install -q -r requirements.txt

# SDK 서버 실행 (백그라운드)
python generator.py &
SDK_PID=$!
cd ..
sleep 3

# 2. 정적 파일 서버 시작
echo -e "${GREEN}2️⃣ 정적 파일 서버 시작...${NC}"
cd static-server

# 패키지 설치
if [ ! -d "node_modules" ]; then
    npm install --silent
fi

# 정적 서버 실행 (백그라운드)
npm start &
STATIC_PID=$!
cd ..
sleep 2

# 3. 웹 인터페이스 시작
echo -e "${GREEN}3️⃣ 웹 인터페이스 시작...${NC}"
cd web-interface

# 패키지 설치
if [ ! -d "node_modules" ]; then
    npm install --silent
fi

# 웹 인터페이스 실행 (백그라운드)
npm run dev &
WEB_PID=$!
cd ..

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ 모든 서버가 시작되었습니다!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo -e "🌐 웹 인터페이스: ${BLUE}http://localhost:5173${NC}"
echo -e "🐍 SDK 서버: ${BLUE}http://localhost:5000${NC}"
echo -e "📁 정적 파일 서버: ${BLUE}http://localhost:8080${NC}"
echo ""
echo -e "${YELLOW}종료하려면 Ctrl+C를 누르세요.${NC}"
echo ""

# 종료 시그널 처리
trap "echo -e '\n${YELLOW}서버 종료 중...${NC}'; kill $SDK_PID $STATIC_PID $WEB_PID 2>/dev/null; exit" INT

# 프로세스 대기
wait