import { ConceptInput } from '../types';

// 톤앤매너 매핑
const toneMap = {
  professional: '전문적이고 신뢰감 있는',
  friendly: '친근하고 따뜻한',
  playful: '재미있고 활발한',
  serious: '진지하고 격식 있는',
  luxurious: '고급스럽고 세련된'
};

// 색상 스킴 매핑
const colorSchemeMap = {
  blue: '--primary: #2563eb; --primary-dark: #1e40af; --secondary: #10b981;',
  green: '--primary: #10b981; --primary-dark: #059669; --secondary: #3b82f6;',
  purple: '--primary: #9333ea; --primary-dark: #7c3aed; --secondary: #ec4899;',
  red: '--primary: #ef4444; --primary-dark: #dc2626; --secondary: #f59e0b;',
  orange: '--primary: #f97316; --primary-dark: #ea580c; --secondary: #84cc16;',
  custom: ''
};

// 템플릿별 특화 프롬프트
const templatePrompts = {
  insurance: `
    보험 서비스 특화 요소:
    - 신뢰감을 주는 통계 수치 포함
    - 보장 항목 명확히 표시
    - 간편한 보험료 계산기
    - 전문 상담사 연결 CTA
    - 고객 후기와 보상 사례
  `,
  petcare: `
    반려동물 서비스 특화 요소:
    - 따뜻하고 감성적인 메시지
    - 귀여운 아이콘과 일러스트
    - 반려동물 나이/품종별 맞춤 정보
    - 24시간 상담 가능 강조
    - 실제 치료 사례와 후기
  `,
  education: `
    교육 서비스 특화 요소:
    - 커리큘럼과 학습 과정 표시
    - 강사진 소개
    - 수강생 성과와 후기
    - 무료 체험 또는 샘플 강의
    - 수료증/자격증 정보
  `,
  healthcare: `
    헬스케어 서비스 특화 요소:
    - 의료진 자격과 경력 표시
    - 진료 과목과 특화 분야
    - 온라인 예약 시스템
    - 건강 정보와 팁
    - 의료 장비와 시설 소개
  `,
  ecommerce: `
    이커머스 특화 요소:
    - 상품 갤러리와 카테고리
    - 할인과 프로모션 배너
    - 장바구니와 즉시 구매 버튼
    - 배송과 반품 정책
    - 고객 리뷰와 평점
  `,
  custom: ''
};

export function generateLandingPagePrompt(concept: ConceptInput): string {
  const tone = toneMap[concept.tone];
  const colorScheme = concept.colorScheme ? colorSchemeMap[concept.colorScheme] : colorSchemeMap.blue;
  const templateGuide = concept.template ? templatePrompts[concept.template] : '';
  
  // 기본 섹션 설정
  const sections = concept.sections || ['hero', 'features', 'testimonials', 'pricing', 'faq', 'cta'];
  
  const prompt = `당신은 전문 웹 디자이너이자 개발자입니다. 다음 조건에 맞는 한국어 랜딩페이지를 생성해주세요.

## 프로젝트 정보
- 업종/서비스: ${concept.industry}
- 타겟 고객: ${concept.target}
- 핵심 가치/메시지: ${concept.mainValue}
- 톤앤매너: ${tone}
${concept.customRequirements ? `- 추가 요구사항: ${concept.customRequirements}` : ''}

${templateGuide}

## 디자인 요구사항
1. 반응형 디자인 (모바일, 태블릿, 데스크톱)
2. 모던하고 깔끔한 레이아웃
3. 부드러운 스크롤 애니메이션
4. 인터랙티브 호버 효과
5. 다음 색상 변수 사용:
   :root {
     ${colorScheme}
     --text-dark: #1f2937;
     --text-light: #6b7280;
     --bg-light: #f9fafb;
   }

## 필수 섹션 (순서대로)
${sections.includes('hero') ? `
### 1. Hero Section
- 강력한 헤드라인과 서브타이틀
- CTA 버튼 (주요 액션 유도)
- 비주얼 요소 (일러스트/그래픽)
- 네비게이션 바
` : ''}
${sections.includes('features') ? `
### 2. Features/Benefits Section
- 3-4개의 주요 특징/혜택
- 아이콘과 설명
- 시각적 구분이 명확한 카드 레이아웃
` : ''}
${sections.includes('testimonials') ? `
### 3. Testimonials Section
- 실제 고객 후기 형식
- 고객 정보 (이름, 나이/지역)
- 신뢰도를 높이는 구체적 내용
` : ''}
${sections.includes('pricing') ? `
### 4. Pricing Section
- 명확한 가격 표시
- 플랜별 특징 비교
- 추천 플랜 강조
` : ''}
${sections.includes('faq') ? `
### 5. FAQ Section
- 자주 묻는 질문 4-5개
- 아코디언 형식 (클릭하면 펼쳐짐)
` : ''}
${sections.includes('cta') ? `
### 6. CTA Section
- 강력한 행동 유도 메시지
- 눈에 띄는 CTA 버튼
- 연락처 정보
` : ''}

## 기술 요구사항
1. 단일 HTML 파일로 생성 (인라인 CSS와 JavaScript 포함)
2. 최신 CSS 기능 활용 (Grid, Flexbox, CSS Variables)
3. 바닐라 JavaScript 사용 (외부 라이브러리 없음)
4. SEO 최적화된 시맨틱 HTML
5. 웹 접근성 고려 (ARIA 속성)

## 콘텐츠 요구사항
1. 모든 텍스트는 한국어로 작성
2. ${concept.target}에게 어필하는 메시지
3. ${concept.mainValue}를 명확히 전달
4. 구체적이고 신뢰할 수 있는 내용
5. 감정에 호소하면서도 전문적인 톤

## 출력 형식
<!DOCTYPE html>로 시작하는 완전한 HTML 문서를 생성하세요.
모든 스타일은 <style> 태그 내에, 모든 스크립트는 <script> 태그 내에 포함하세요.
절대 코드 블록 마크다운을 사용하지 말고, 순수 HTML 코드만 출력하세요.`;

  return prompt;
}

// 섹션별 수정 프롬프트 생성
export function generateEditPrompt(
  originalHtml: string,
  editType: string,
  editDetails: any
): string {
  const prompts: Record<string, string> = {
    text: `
      다음 HTML에서 "${editDetails.selector}" 요소의 텍스트를 "${editDetails.newText}"로 변경하세요.
      다른 부분은 그대로 유지하고, 해당 텍스트만 수정하세요.
    `,
    style: `
      다음 HTML에서 "${editDetails.selector}" 요소의 스타일을 다음과 같이 변경하세요:
      ${editDetails.newStyles}
      다른 부분은 그대로 유지하세요.
    `,
    section: `
      다음 HTML에서 "${editDetails.sectionName}" 섹션을 다음과 같이 수정하세요:
      ${editDetails.changes}
      전체적인 디자인 일관성을 유지하면서 수정하세요.
    `,
    addSection: `
      다음 HTML에 새로운 "${editDetails.sectionType}" 섹션을 추가하세요.
      위치: ${editDetails.position}
      내용: ${editDetails.content}
      기존 디자인 스타일과 일치하도록 추가하세요.
    `
  };

  return `${prompts[editType]}\n\n원본 HTML:\n${originalHtml}`;
}

// 간단한 텍스트 수정을 위한 유틸리티
export function quickEditHtml(
  html: string,
  selector: string,
  property: string,
  value: string
): string {
  // 이 함수는 Claude API 호출 없이 간단한 수정을 처리
  // 실제 구현에서는 cheerio 같은 HTML 파서 사용 권장
  
  if (property === 'text') {
    // 간단한 텍스트 교체 로직
    const regex = new RegExp(`(${selector}[^>]*>)([^<]+)(<)`, 'gi');
    return html.replace(regex, `$1${value}$3`);
  }
  
  // 복잡한 수정은 Claude API 사용
  return html;
}