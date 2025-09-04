#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🚀 Claude Code SDK 랜딩페이지 생성기     ║${NC}"
echo -e "${BLUE}║   API 키 없이 로컬 실행                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Python 체크
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python 3가 설치되어 있지 않습니다.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Claude Code SDK 모드로 실행합니다 (API 키 불필요)${NC}"
echo ""

# 1. Python SDK 서버 시작 (Claude Code 버전)
echo -e "${GREEN}1️⃣ Claude Code SDK 서버 시작...${NC}"
cd sdk-server

# 가상환경이 없으면 생성
if [ ! -d "venv" ]; then
    echo "Python 가상환경 생성 중..."
    python3 -m venv venv
fi

# 가상환경 활성화 및 패키지 설치
source venv/bin/activate
pip install -q flask flask-cors beautifulsoup4 lxml

# Claude Code SDK 서버 실행 (백그라운드)
python generator_claude_code.py &
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
echo -e "🤖 Claude Code SDK: ${BLUE}http://localhost:5001${NC}"
echo -e "📁 생성된 페이지: ${BLUE}http://localhost:8080${NC}"
echo ""
echo -e "${YELLOW}ℹ️  API 키 없이 Claude Code SDK로 실행 중${NC}"
echo -e "${YELLOW}종료하려면 Ctrl+C를 누르세요.${NC}"
echo ""

# 종료 시그널 처리
trap "echo -e '\n${YELLOW}서버 종료 중...${NC}'; kill $SDK_PID $STATIC_PID $WEB_PID 2>/dev/null; exit" INT

# 프로세스 대기
wait