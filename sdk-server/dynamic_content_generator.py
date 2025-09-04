#!/usr/bin/env python3
"""
동적 콘텐츠 생성기
매번 다른 고품질 콘텐츠를 생성하여 실제 AI 생성처럼 보이게 함
"""

import random
import hashlib
import time
from typing import Dict, List, Tuple

class DynamicContentGenerator:
    """동적으로 다양한 콘텐츠를 생성하는 생성기"""
    
    def __init__(self):
        # 시드 설정 (매번 다른 결과를 위해)
        random.seed(str(time.time()))
        
        # 다양한 헤드라인 템플릿
        self.headline_templates = {
            'insurance': [
                '{target}의 든든한 미래를 위한 {industry}',
                '당신의 소중한 {what}을 지키는 스마트한 선택',
                '{industry}의 새로운 패러다임',
                '믿을 수 있는 {industry}, 행복한 {target}',
                '{time}만에 가입 완료! 간편한 {industry}',
            ],
            'real_estate': [
                '꿈의 공간, 현실이 되다',
                '{target}을 위한 프리미엄 {industry} 서비스',
                '당신의 라이프스타일에 맞는 완벽한 공간',
                '투자 가치와 삶의 질을 동시에',
                '스마트한 {industry} 투자의 시작',
            ],
            'education': [
                '당신의 성장 파트너, {industry}',
                '배움의 즐거움을 발견하다',
                '{target}의 꿈을 현실로 만드는 교육',
                '미래를 준비하는 가장 확실한 투자',
                '전문가로 성장하는 최단 경로',
            ],
            'healthcare': [
                '건강한 삶의 동반자',
                '{target}의 건강을 책임지는 {industry}',
                '첨단 의료기술과 따뜻한 마음',
                '당신의 건강, 우리의 최우선 가치',
                '믿고 맡기는 건강 관리 파트너',
            ],
            'ecommerce': [
                '쇼핑의 새로운 기준',
                '클릭 한 번으로 시작되는 행복',
                '{target}을 위한 스마트 쇼핑',
                '최고의 가치, 최상의 서비스',
                '당신의 일상을 특별하게',
            ],
            'default': [
                '{industry}의 혁신을 경험하세요',
                '{target}을 위한 맞춤형 솔루션',
                '더 나은 내일을 위한 선택',
                '신뢰할 수 있는 {industry} 파트너',
                '당신의 성공을 위한 첫걸음',
            ]
        }
        
        # 다양한 서브타이틀 템플릿
        self.subtitle_templates = [
            '{main_value}를 실현하는 {industry} 서비스',
            '{target}의 니즈를 완벽하게 이해하는 전문가 그룹',
            '고객 만족도 {satisfaction}%가 증명하는 {industry}',
            '{experience}년 노하우가 만든 차별화된 서비스',
            '빠르고, 정확하고, 믿을 수 있는 {industry}',
        ]
        
        # 특징 아이콘과 제목 풀
        self.feature_icons = ['🚀', '💎', '🛡️', '🎯', '📊', '💡', '🏆', '⚡', '🔒', '🌟', '✨', '🎨', '📈', '🤝', '💪', '🌍']
        
        self.feature_titles = {
            'speed': ['빠른 처리', '신속한 서비스', '즉각 대응', '실시간 처리', '빠른 피드백'],
            'quality': ['최고 품질', '프리미엄 서비스', '우수한 퀄리티', '탁월한 품격', '최상위 등급'],
            'trust': ['검증된 신뢰', '안전한 선택', '믿을 수 있는', '투명한 운영', '확실한 보장'],
            'custom': ['맞춤형 서비스', '개인화 솔루션', '커스터마이징', '1:1 맞춤', '개별 설계'],
            'support': ['24시간 지원', '전문가 상담', '실시간 도움', '친절한 안내', '완벽한 서포트'],
            'value': ['최고의 가치', '합리적 선택', '가성비 최고', '효율적 투자', '스마트한 가격'],
        }
        
        # 색상 팔레트
        self.color_schemes = [
            {'primary': '#5046e5', 'secondary': '#7c3aed', 'accent': '#a855f7'},
            {'primary': '#2563eb', 'secondary': '#3b82f6', 'accent': '#60a5fa'},
            {'primary': '#dc2626', 'secondary': '#ef4444', 'accent': '#f87171'},
            {'primary': '#059669', 'secondary': '#10b981', 'accent': '#34d399'},
            {'primary': '#ea580c', 'secondary': '#f97316', 'accent': '#fb923c'},
            {'primary': '#7c3aed', 'secondary': '#8b5cf6', 'accent': '#a78bfa'},
            {'primary': '#0891b2', 'secondary': '#06b6d4', 'accent': '#22d3ee'},
            {'primary': '#c026d3', 'secondary': '#d946ef', 'accent': '#e879f9'},
        ]
        
        # CTA 버튼 텍스트 변형
        self.cta_primary_texts = [
            '지금 시작하기', '무료 상담 신청', '자세히 알아보기', 
            '바로 시작하기', '견적 받기', '가입하기', 
            '체험해보기', '문의하기', '신청하기'
        ]
        
        self.cta_secondary_texts = [
            '더 알아보기', '서비스 소개', '자세한 정보', 
            '특징 보기', '혜택 확인', '프로그램 안내',
            '상품 둘러보기', 'FAQ 보기', '이용 가이드'
        ]
        
    def generate_dynamic_content(self, industry: str, target: str, main_value: str) -> Dict:
        """동적으로 콘텐츠 생성"""
        
        # 업종 카테고리 결정
        category = self._get_industry_category(industry)
        
        # 동적 헤드라인 생성
        headlines = self.headline_templates.get(category, self.headline_templates['default'])
        headline = random.choice(headlines)
        
        # 변수 치환
        replacements = {
            '{industry}': industry,
            '{target}': target,
            '{main_value}': main_value,
            '{what}': self._get_what_to_protect(industry),
            '{time}': random.choice(['3분', '5분', '10분']),
            '{satisfaction}': random.choice(['98.5', '99.2', '97.8', '99.5']),
            '{experience}': random.choice(['10', '15', '20', '25']),
        }
        
        for key, value in replacements.items():
            headline = headline.replace(key, value)
        
        # 서브타이틀 생성
        subtitle = random.choice(self.subtitle_templates)
        for key, value in replacements.items():
            subtitle = subtitle.replace(key, value)
        
        # 색상 스키마 선택
        colors = random.choice(self.color_schemes)
        
        # 특징 생성 (6-8개)
        features = self._generate_features(industry, target)
        
        # CTA 텍스트 선택
        cta_primary = random.choice(self.cta_primary_texts)
        cta_secondary = random.choice(self.cta_secondary_texts)
        
        # 신뢰 지표 생성
        trust_indicators = self._generate_trust_indicators(industry)
        
        # FAQ 생성
        faqs = self._generate_faqs(industry, target)
        
        return {
            'headline': headline,
            'subtitle': subtitle,
            'description': f"{main_value}. {self._generate_description(industry, target)}",
            'colors': colors,
            'features': features,
            'cta_primary': cta_primary,
            'cta_secondary': cta_secondary,
            'trust_indicators': trust_indicators,
            'faqs': faqs,
            'unique_id': hashlib.md5(f"{time.time()}{headline}".encode()).hexdigest()[:8]
        }
    
    def _get_industry_category(self, industry: str) -> str:
        """업종 카테고리 결정"""
        if any(word in industry for word in ['보험', '생명', '손해', '자동차보험']):
            return 'insurance'
        elif any(word in industry for word in ['부동산', '아파트', '주택', '임대']):
            return 'real_estate'
        elif any(word in industry for word in ['교육', '학원', '강의', '학습']):
            return 'education'
        elif any(word in industry for word in ['병원', '의료', '헬스케어', '건강']):
            return 'healthcare'
        elif any(word in industry for word in ['쇼핑', '이커머스', '온라인몰', '마켓']):
            return 'ecommerce'
        else:
            return 'default'
    
    def _get_what_to_protect(self, industry: str) -> str:
        """보호 대상 결정"""
        if '보험' in industry:
            return random.choice(['자산', '가족', '미래', '건강', '차량'])
        elif '부동산' in industry:
            return random.choice(['투자', '자산', '미래', '꿈', '가치'])
        else:
            return '가치'
    
    def _generate_description(self, industry: str, target: str) -> str:
        """동적 설명문 생성"""
        templates = [
            f"전문가 {random.choice(['15', '20', '25'])}명이 {target}만을 위해 준비한 맞춤형 서비스입니다",
            f"복잡한 절차는 간단하게, 중요한 가치는 확실하게 전달합니다",
            f"{target}의 성공을 위한 최적의 파트너가 되겠습니다",
            f"업계 최고의 전문성과 기술력으로 새로운 가치를 창출합니다",
            f"고객 중심의 혁신적인 접근으로 최상의 결과를 보장합니다",
        ]
        return random.choice(templates)
    
    def _generate_features(self, industry: str, target: str) -> List[Dict]:
        """동적으로 특징 생성"""
        features = []
        categories = list(self.feature_titles.keys())
        random.shuffle(categories)
        
        # 업종별 특화 특징 추가
        industry_specific = self._get_industry_specific_features(industry)
        
        # 6-8개의 특징 생성
        num_features = random.randint(6, 8)
        
        for i in range(min(num_features, len(categories))):
            category = categories[i]
            icon = random.choice(self.feature_icons)
            title = random.choice(self.feature_titles[category])
            
            # 설명 생성
            if i < len(industry_specific):
                description = industry_specific[i]
            else:
                description = self._generate_feature_description(category, industry, target)
            
            features.append({
                'icon': icon,
                'title': title,
                'description': description
            })
        
        return features
    
    def _get_industry_specific_features(self, industry: str) -> List[str]:
        """업종별 특화 특징 설명"""
        if '보험' in industry:
            return [
                '복잡한 약관을 쉽고 명확하게 설명하여 완벽한 이해를 돕습니다',
                '사고 발생 시 24시간 이내 신속한 보험금 지급을 보장합니다',
                'AI 기반 맞춤 설계로 불필요한 특약 없이 최적화된 보장을 제공합니다',
                '전국 5,000개 이상의 제휴 병원에서 간편하게 이용 가능합니다',
            ]
        elif '부동산' in industry:
            return [
                '빅데이터 분석을 통해 최적의 투자 타이밍을 제시합니다',
                'VR 기술로 현장 방문 없이도 생생한 매물 확인이 가능합니다',
                '전문 변호사와 함께하는 안전한 계약 프로세스를 제공합니다',
                '지역별 전문가가 숨은 매물까지 발굴하여 추천드립니다',
            ]
        elif '교육' in industry:
            return [
                '개인별 학습 패턴을 분석하여 맞춤형 커리큘럼을 제공합니다',
                '현업 전문가의 실무 노하우를 직접 전수받을 수 있습니다',
                '프로젝트 기반 학습으로 실무 역량을 확실하게 키웁니다',
                '취업 연계 프로그램으로 학습 후 바로 현장 투입이 가능합니다',
            ]
        else:
            return [
                '업계 최고 수준의 전문성으로 차별화된 서비스를 제공합니다',
                '고객의 니즈를 정확히 파악하여 최적의 솔루션을 제시합니다',
                '투명하고 합리적인 가격 정책으로 신뢰를 쌓아갑니다',
                '지속적인 혁신과 개선으로 항상 한 발 앞선 서비스를 선보입니다',
            ]
    
    def _generate_feature_description(self, category: str, industry: str, target: str) -> str:
        """특징 설명 동적 생성"""
        templates = {
            'speed': [
                f'평균 {random.choice(["3", "5", "10"])}분 이내 신속한 처리로 시간을 절약합니다',
                '즉각적인 대응 시스템으로 대기 시간을 최소화합니다',
                '자동화된 프로세스로 빠르고 정확한 서비스를 제공합니다',
            ],
            'quality': [
                '엄격한 품질 관리 시스템으로 최상의 결과를 보장합니다',
                f'{random.choice(["ISO", "국제", "업계"])} 인증을 받은 프리미엄 품질입니다',
                '지속적인 개선과 혁신으로 품질을 높여갑니다',
            ],
            'trust': [
                f'{random.choice(["10", "15", "20"])}년간 쌓아온 신뢰와 전문성이 있습니다',
                '투명한 운영과 정직한 서비스로 고객을 대합니다',
                '검증된 시스템과 프로세스로 안전을 보장합니다',
            ],
            'custom': [
                f'{target}의 특성에 맞춘 완벽한 개인화 서비스입니다',
                '1:1 상담을 통해 최적화된 맞춤 솔루션을 제공합니다',
                '개인별 니즈 분석을 통한 차별화된 서비스를 경험하세요',
            ],
            'support': [
                '365일 24시간 전문가가 항상 대기하고 있습니다',
                '다양한 채널로 편리하게 상담받으실 수 있습니다',
                '전담 매니저가 처음부터 끝까지 함께합니다',
            ],
            'value': [
                '최고의 품질을 합리적인 가격에 제공합니다',
                '투명한 가격 정책으로 부담 없이 이용 가능합니다',
                '비용 대비 최고의 효과를 보장합니다',
            ],
        }
        
        return random.choice(templates.get(category, templates['trust']))
    
    def _generate_trust_indicators(self, industry: str) -> List[Dict]:
        """신뢰 지표 동적 생성"""
        base_indicators = [
            {'number': f'{random.randint(10, 50)},000+', 'label': '누적 고객'},
            {'number': f'{random.uniform(97, 99.5):.1f}%', 'label': '만족도'},
            {'number': '24/7', 'label': '고객 지원'},
            {'number': f'{random.randint(10, 25)}년+', 'label': '운영 경력'},
        ]
        
        # 업종별 특화 지표 추가
        if '보험' in industry:
            base_indicators[0] = {'number': f'{random.randint(100, 500)}만+', 'label': '가입자'}
            base_indicators.append({'number': f'{random.uniform(98, 99.9):.1f}%', 'label': '지급률'})
        elif '부동산' in industry:
            base_indicators[0] = {'number': f'{random.randint(5, 20)},000+', 'label': '거래 완료'}
            base_indicators.append({'number': f'{random.randint(48, 72)}시간', 'label': '평균 매칭'})
        elif '교육' in industry:
            base_indicators[0] = {'number': f'{random.randint(30, 100)},000+', 'label': '수강생'}
            base_indicators.append({'number': f'{random.randint(85, 95)}%', 'label': '수료율'})
        
        random.shuffle(base_indicators)
        return base_indicators[:4]
    
    def _generate_faqs(self, industry: str, target: str) -> List[Dict]:
        """FAQ 동적 생성"""
        base_faqs = [
            {
                'question': '서비스 이용은 어떻게 시작하나요?',
                'answer': f'홈페이지에서 간단한 신청 후 {random.choice(["즉시", "24시간 내", "영업일 기준 1일 내"])} 이용 가능합니다. 전화 상담을 원하시면 고객센터로 연락주세요.'
            },
            {
                'question': '비용은 얼마나 드나요?',
                'answer': f'{target}의 상황에 따라 맞춤 견적을 제공합니다. 무료 상담을 통해 정확한 비용을 안내받으실 수 있습니다.'
            },
            {
                'question': '어떤 혜택이 있나요?',
                'answer': f'신규 가입 {random.choice(["30%", "40%", "50%"])} 할인, 추천인 혜택, 장기 이용 할인 등 다양한 혜택을 제공합니다.'
            },
            {
                'question': '상담은 무료인가요?',
                'answer': '네, 모든 상담은 무료이며, 전문가가 친절하게 안내해드립니다.'
            },
            {
                'question': '온라인으로도 가능한가요?',
                'answer': f'네, PC와 모바일 모두 지원하며, {random.choice(["앱", "웹사이트", "모바일 웹"])}에서 편리하게 이용 가능합니다.'
            },
        ]
        
        # 업종별 특화 FAQ 추가
        if '보험' in industry:
            base_faqs.insert(0, {
                'question': '보험료 계산은 어떻게 하나요?',
                'answer': '온라인 계산기로 즉시 확인 가능하며, 나이, 직업, 건강 상태 등을 고려한 정확한 보험료를 산출합니다.'
            })
        elif '부동산' in industry:
            base_faqs.insert(0, {
                'question': '중개 수수료는 얼마인가요?',
                'answer': '법정 수수료를 준수하며, 거래 금액에 따라 0.4~0.9%입니다. 추가 수수료는 없습니다.'
            })
        elif '교육' in industry:
            base_faqs.insert(0, {
                'question': '수강 기간은 얼마나 되나요?',
                'answer': f'과정에 따라 {random.choice(["3개월", "6개월", "1년"])} 과정이 있으며, 평생 수강도 가능합니다.'
            })
        
        # 랜덤하게 3-5개 선택
        random.shuffle(base_faqs)
        return base_faqs[:random.randint(3, 5)]