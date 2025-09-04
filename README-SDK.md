# 🚀 Claude SDK 기반 AI 랜딩페이지 생성기

로컬 파일 시스템 기반으로 작동하는 AI 랜딩페이지 자동 생성 시스템입니다.  
Claude SDK를 활용하여 페이지를 생성하고, 파일로 저장하여 관리합니다.

## ✨ 주요 특징

### 🎯 SDK 기반 아키텍처
- **로컬 실행**: API 호출 대신 로컬에서 SDK 직접 실행
- **파일 시스템 저장**: 생성된 페이지를 파일로 영구 보관
- **버전 관리**: 각 페이지의 편집 히스토리 자동 저장
- **무제한 생성**: API 비용 걱정 없이 무제한 페이지 생성

### 🛠 시스템 구성

```
landing-page-generator/
├── sdk-server/          # Python Flask SDK 서버
│   ├── generator.py     # 페이지 생성 엔진
│   ├── page_manager.py  # 페이지 관리 시스템
│   └── templates.py     # 프롬프트 템플릿
│
├── web-interface/       # React 웹 인터페이스
│   └── src/
│       ├── components/  # UI 컴포넌트
│       └── services/    # SDK 클라이언트
│
├── generated-pages/     # 생성된 페이지 저장소
│   └── [page_id]/
│       ├── index.html   # 페이지 HTML
│       ├── metadata.json # 메타데이터
│       └── versions/    # 버전 히스토리
│
└── static-server/       # 페이지 서빙 서버
    └── server.js        # Express 정적 서버
```

## 📦 설치 방법

### 필수 요구사항
- Python 3.8 이상
- Node.js 18.0 이상
- Claude API Key ([Anthropic Console](https://console.anthropic.com)에서 발급)

### 1. 프로젝트 클론
```bash
cd landing-page-generator
```

### 2. 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일 편집:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx  # 실제 API 키 입력
```

### 3. 빠른 시작 (추천)
```bash
# Mac/Linux
./start-sdk.sh

# Windows (각 서버를 개별 터미널에서 실행)
```

## 🚀 수동 실행 방법

### 1. Python SDK 서버
```bash
cd sdk-server
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python generator.py
```
→ http://localhost:5000 에서 실행

### 2. 정적 파일 서버
```bash
cd static-server
npm install
npm start
```
→ http://localhost:8080 에서 실행

### 3. 웹 인터페이스
```bash
cd web-interface
npm install
npm run dev
```
→ http://localhost:5173 에서 실행

## 📖 사용 방법

### 1. 페이지 생성
1. 웹 인터페이스 접속: http://localhost:5173
2. 컨셉 입력:
   - 업종: "자동차보험"
   - 타겟: "시니어 60대 이상"
   - 메시지: "전화 한 통으로 간편 가입"
3. **"랜딩페이지 생성"** 클릭
4. 30초~1분 내 생성 완료

### 2. 생성된 페이지 확인
- **웹 인터페이스**: 미리보기 패널에서 확인
- **정적 서버**: http://localhost:8080 에서 목록 확인
- **파일 시스템**: `generated-pages/[page_id]/index.html`

### 3. 페이지 편집
1. 편집 탭으로 전환
2. 미리보기에서 텍스트 클릭
3. 수정 후 저장
4. 버전이 자동으로 저장됨

## 🗂 파일 구조

### 생성된 페이지 구조
```
generated-pages/
└── page_1234567890_abcd/
    ├── index.html         # 메인 HTML 파일
    ├── metadata.json      # 페이지 정보
    └── versions/          # 편집 히스토리
        ├── v1_1234567890.html
        ├── v2_1234567891.html
        └── ...
```

### 메타데이터 예시
```json
{
  "id": "page_1234567890_abcd",
  "concept": {
    "industry": "자동차보험",
    "target": "시니어",
    "mainValue": "간편 가입"
  },
  "created_at": 1234567890,
  "created_at_str": "2024-01-01 12:00:00",
  "versions": []
}
```

## 🔧 API 엔드포인트

### SDK 서버 (Python Flask)
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/health` | 서버 상태 확인 |
| POST | `/api/generate` | 페이지 생성 |
| GET | `/api/pages` | 페이지 목록 |
| GET | `/api/pages/{id}` | 페이지 조회 |
| GET | `/api/pages/{id}/html` | HTML 직접 조회 |
| PUT | `/api/pages/{id}/edit` | 페이지 편집 |
| GET | `/api/pages/{id}/versions` | 버전 목록 |

### 정적 서버
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/` | 페이지 목록 UI |
| GET | `/view/{id}` | 페이지 보기 |
| GET | `/api/list` | 페이지 목록 JSON |

## 🎨 템플릿 커스터마이징

### 프롬프트 수정
`sdk-server/templates.py`:
```python
TEMPLATE_PROMPTS = {
    'custom': """
    커스텀 템플릿 가이드:
    - 특별한 요구사항
    - 업종별 특화 요소
    """
}
```

### 색상 테마 추가
```python
COLOR_SCHEME_MAP = {
    'custom': '--primary: #custom; --secondary: #custom;'
}
```

## 🚨 문제 해결

### Python SDK 서버 오류
```bash
# 가상환경 재생성
rm -rf sdk-server/venv
cd sdk-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 포트 충돌
`.env` 파일에서 포트 변경:
```
SDK_PORT=5001
STATIC_PORT=8081
```

### API 키 오류
- `.env` 파일의 API 키 확인
- 키 앞뒤 공백 제거
- 올바른 형식: `sk-ant-api03-xxxxx`

## 📊 성능 최적화

### 페이지 생성 속도
- 평균 생성 시간: 30-60초
- 프롬프트 최적화로 20% 단축 가능

### 파일 크기
- 평균 HTML 크기: 50-100KB
- 인라인 CSS/JS 포함
- gzip 압축 시 70% 감소

## 🤝 기여하기

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 라이선스

MIT License

## 🔮 향후 계획

- [ ] 페이지 템플릿 라이브러리
- [ ] 실시간 협업 편집
- [ ] A/B 테스트 기능
- [ ] 분석 대시보드
- [ ] Docker 컨테이너화
- [ ] 클라우드 배포 지원

## 💡 팁

### 빠른 생성을 위한 팁
1. 템플릿 사용: 보험, 펫케어 등 미리 정의된 템플릿 활용
2. 섹션 최소화: 필요한 섹션만 선택
3. 캐싱 활용: 자주 사용하는 컨셉 저장

### 효율적인 관리
1. 정기 백업: `generated-pages` 폴더 백업
2. 버전 관리: Git으로 페이지 버전 추적
3. 메타데이터 활용: 검색과 필터링에 활용

## 📞 지원

문제 발생 시 Issues 탭에 등록해주세요.

---

**Made with ❤️ using Claude SDK**