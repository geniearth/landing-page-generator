#!/usr/bin/env python3
"""동적 콘텐츠 생성 테스트"""

from dynamic_content_generator import DynamicContentGenerator

# 생성기 인스턴스
gen = DynamicContentGenerator()

# 테스트 1: 부동산
print("=== 부동산 테스트 ===")
content1 = gen.generate_dynamic_content("부동산", "30대 신혼부부", "첫 내 집 마련의 꿈을 실현")
print(f"헤드라인: {content1['headline']}")
print(f"서브타이틀: {content1['subtitle']}")
print(f"CTA: {content1['cta_primary']} / {content1['cta_secondary']}")
print(f"특징 개수: {len(content1['features'])}")
print(f"색상: {content1['colors']}")
print(f"고유ID: {content1['unique_id']}")
print()

# 테스트 2: 같은 입력으로 다시 실행 (다른 결과 확인)
print("=== 동일 입력, 다른 결과 확인 ===")
content2 = gen.generate_dynamic_content("부동산", "30대 신혼부부", "첫 내 집 마련의 꿈을 실현")
print(f"헤드라인: {content2['headline']}")
print(f"고유ID: {content2['unique_id']}")
print(f"같은 결과?: {content1['unique_id'] == content2['unique_id']}")
print()

# 테스트 3: 자동차보험
print("=== 자동차보험 테스트 ===")
content3 = gen.generate_dynamic_content("자동차보험", "시니어(60대 이상)", "전화 한 통으로 간편하게 가입")
print(f"헤드라인: {content3['headline']}")
print(f"FAQ 개수: {len(content3['faqs'])}")
for i, faq in enumerate(content3['faqs'][:2]):
    print(f"  FAQ {i+1}: {faq['question']}")