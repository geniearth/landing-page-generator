# 🚀 AI 랜딩페이지 자동 생성기

Claude SDK를 활용하여 컨셉만 입력하면 자동으로 완성도 높은 랜딩페이지를 생성하고, 실시간으로 편집할 수 있는 웹 애플리케이션입니다.

## ✨ 주요 기능

- **🎨 AI 자동 생성**: 업종, 타겟, 톤앤매너만 입력하면 완성된 랜딩페이지 생성
- **📝 실시간 편집**: 생성된 페이지를 클릭하여 즉시 텍스트 수정
- **📱 반응형 미리보기**: 데스크톱/태블릿/모바일 뷰 전환
- **🎯 템플릿 제공**: 보험, 펫케어, 교육 등 업종별 최적화 템플릿
- **💾 다운로드**: 생성된 HTML 파일 즉시 다운로드

## 🛠 기술 스택

### Backend
- Node.js + TypeScript
- Express.js
- Claude SDK (Anthropic)
- Zod (스키마 검증)

### Frontend
- React 18 + TypeScript
- Vite (빌드 도구)
- Tailwind CSS
- Zustand (상태 관리)
- Axios

## 📦 설치 방법

### 1. 필수 요구사항

- Node.js 18.0 이상
- npm 또는 yarn
- Claude API Key (https://console.anthropic.com 에서 발급)

### 2. 프로젝트 클론

```bash
cd landing-page-generator
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 API 키를 설정합니다:

```bash
cp .env.example .env
```

`.env` 파일 편집:
```
ANTHROPIC_API_KEY=your-actual-api-key-here
PORT=3001
FRONTEND_URL=http://localhost:5173
```

### 4. 의존성 설치

백엔드와 프론트엔드 각각 설치:

```bash
# 백엔드 설치
cd backend
npm install

# 프론트엔드 설치
cd ../frontend
npm install
```

## 🚀 실행 방법

### 개발 모드 실행

터미널을 2개 열어서 각각 실행:

**터미널 1 - 백엔드 서버:**
```bash
cd backend
npm run dev
```
서버가 http://localhost:3001 에서 실행됩니다.

**터미널 2 - 프론트엔드:**
```bash
cd frontend
npm run dev
```
프론트엔드가 http://localhost:5173 에서 실행됩니다.

### 프로덕션 빌드

```bash
# 백엔드 빌드
cd backend
npm run build
npm start

# 프론트엔드 빌드
cd frontend
npm run build
npm run preview
```

## 📖 사용 방법

### 1. 랜딩페이지 생성

1. 브라우저에서 http://localhost:5173 접속
2. **생성** 탭에서 정보 입력:
   - 업종/서비스 (예: "자동차보험")
   - 타겟 고객 (예: "시니어 60대 이상")
   - 핵심 메시지
   - 톤앤매너 선택
   - 색상 테마 선택
3. **"랜딩페이지 생성"** 버튼 클릭
4. 30초~1분 내에 AI가 페이지 생성

### 2. 실시간 편집

1. **편집** 탭으로 전환
2. 미리보기에서 수정할 텍스트 클릭
3. 팝업 창에서 텍스트 수정
4. 저장 버튼 클릭

### 3. 다운로드

1. 미리보기 상단 툴바에서 **"다운로드"** 버튼 클릭
2. HTML 파일이 자동 다운로드

## 📝 템플릿 예시

### 보험 템플릿
- 신뢰감 있는 통계 수치
- 보장 항목 명시
- 보험료 계산기
- 고객 후기

### 펫케어 템플릿
- 감성적인 메시지
- 귀여운 아이콘
- 반려동물 정보 입력
- 24시간 상담 강조

## 🔧 커스터마이징

### 프롬프트 수정

`backend/src/prompts/templates.ts` 파일에서 프롬프트 템플릿을 수정할 수 있습니다:

```typescript
const templatePrompts = {
  custom: `
    여기에 커스텀 템플릿 가이드 추가
  `
};
```

### 색상 테마 추가

`frontend/src/components/ConceptForm.tsx`에서 새로운 색상 옵션 추가:

```typescript
const colorOptions = [
  { value: 'custom', label: '커스텀', color: 'bg-custom-500' },
  // ...
];
```

## 🐛 문제 해결

### API 키 오류
- `.env` 파일에 올바른 API 키가 설정되었는지 확인
- 키에 공백이나 따옴표가 없는지 확인

### 포트 충돌
- 3001, 5173 포트가 사용 중이면 `.env`와 `vite.config.ts`에서 변경

### 생성 실패
- Claude API 사용량 제한 확인
- 네트워크 연결 상태 확인

## 📄 API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/generate` | 랜딩페이지 생성 |
| POST | `/api/generate/stream` | 스트리밍 생성 |
| PUT | `/api/edit/:pageId` | 페이지 수정 |
| PATCH | `/api/quick-edit` | 빠른 텍스트 수정 |
| GET | `/api/page/:pageId` | 페이지 조회 |
| GET | `/api/pages` | 페이지 목록 |

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 라이선스

MIT License

## 💡 향후 계획

- [ ] 이미지 자동 생성 (DALL-E 연동)
- [ ] 다국어 지원
- [ ] SEO 최적화 옵션
- [ ] 코드 내보내기 (React/Vue)
- [ ] 협업 기능
- [ ] 버전 관리

## 🆘 지원

문의사항이나 버그 리포트는 Issues 탭을 이용해주세요.