#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 AI Landing Page Generator 시작 스크립트${NC}"
echo "================================="

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

# 백엔드 의존성 설치
echo -e "${GREEN}📦 백엔드 패키지 설치 중...${NC}"
cd backend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "백엔드 패키지 이미 설치됨 ✓"
fi

# 프론트엔드 의존성 설치
echo -e "${GREEN}📦 프론트엔드 패키지 설치 중...${NC}"
cd ../frontend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "프론트엔드 패키지 이미 설치됨 ✓"
fi

# 서버 시작
echo -e "${GREEN}🔥 서버를 시작합니다...${NC}"
echo "================================="

# 백엔드 시작
cd ../backend
echo -e "${YELLOW}백엔드 서버 시작 (포트 3001)...${NC}"
npm run dev &
BACKEND_PID=$!

# 프론트엔드 시작
cd ../frontend
sleep 3
echo -e "${YELLOW}프론트엔드 서버 시작 (포트 5173)...${NC}"
npm run dev &
FRONTEND_PID=$!

echo "================================="
echo -e "${GREEN}✅ 모든 서버가 시작되었습니다!${NC}"
echo ""
echo "🌐 프론트엔드: http://localhost:5173"
echo "🔧 백엔드 API: http://localhost:3001"
echo ""
echo "종료하려면 Ctrl+C를 누르세요."

# 종료 시그널 처리
trap "echo '서버 종료 중...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# 프로세스 대기
wait