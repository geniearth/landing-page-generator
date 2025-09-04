#!/usr/bin/env python3
"""
업종별 전문 템플릿 라이브러리
각 업종에 특화된 고품질 콘텐츠와 디자인 제공
"""

class IndustryTemplates:
    """업종별 전문 템플릿 관리자"""
    
    @staticmethod
    def get_insurance_template(target, main_value):
        """보험 업종 전용 템플릿"""
        return {
            'hero': {
                'title': '든든한 보장, 합리적인 보험료',
                'subtitle': f'{target}을 위한 맞춤형 보험 설계',
                'description': f'{main_value}. 복잡한 약관은 쉽게, 보험료는 합리적으로, 보장은 든든하게.',
                'cta_primary': '무료 보험료 계산',
                'cta_secondary': '전문가 상담 예약'
            },
            'features': [
                {
                    'icon': '🛡️',
                    'title': '완벽한 보장 범위',
                    'description': '일상의 모든 위험으로부터 고객님을 보호하는 종합 보장'
                },
                {
                    'icon': '💰',
                    'title': '합리적인 보험료',
                    'description': '불필요한 특약 없이 필요한 보장만 선택하는 맞춤 설계'
                },
                {
                    'icon': '⚡',
                    'title': '24시간 내 보상',
                    'description': '사고 발생 시 24시간 내 신속한 보험금 지급'
                },
                {
                    'icon': '📱',
                    'title': '간편한 모바일 청구',
                    'description': '복잡한 서류 없이 모바일로 3분 만에 청구 완료'
                },
                {
                    'icon': '🏥',
                    'title': '전국 제휴 병원',
                    'description': '전국 5,000개 제휴 병원에서 간편 이용'
                },
                {
                    'icon': '👨‍💼',
                    'title': '전문 설계사 1:1',
                    'description': '20년 경력의 전문가가 직접 설계하는 맞춤 보험'
                }
            ],
            'trust_indicators': [
                {'number': '150만+', 'label': '가입 고객'},
                {'number': '99.2%', 'label': '보험금 지급률'},
                {'number': '4.8/5', 'label': '고객 만족도'},
                {'number': '24시간', 'label': '평균 처리 시간'}
            ],
            'faq': [
                {
                    'question': '보험료는 어떻게 산정되나요?',
                    'answer': '나이, 직업, 건강상태 등을 종합적으로 고려하여 개인별 맞춤 보험료를 산정합니다. 온라인 계산기로 바로 확인 가능합니다.'
                },
                {
                    'question': '기존 보험이 있어도 가입 가능한가요?',
                    'answer': '네, 가능합니다. 기존 보험과 중복되지 않는 보장을 추가하거나, 더 나은 조건으로 갈아타실 수 있습니다.'
                },
                {
                    'question': '보험금 청구는 얼마나 걸리나요?',
                    'answer': '서류 접수 후 평균 24시간 이내 처리됩니다. 간단한 사고는 모바일로 즉시 처리 가능합니다.'
                },
                {
                    'question': '중도 해지 시 환급금은 어떻게 되나요?',
                    'answer': '납입 기간과 상품에 따라 다르지만, 해지환급금 계산기로 미리 확인하실 수 있습니다.'
                }
            ],
            'colors': {
                'primary': '#2563eb',
                'secondary': '#0ea5e9',
                'accent': '#06b6d4'
            }
        }
    
    @staticmethod
    def get_real_estate_template(target, main_value):
        """부동산 업종 전용 템플릿"""
        return {
            'hero': {
                'title': '내 집 마련의 꿈, 현실로',
                'subtitle': f'{target}의 라이프스타일에 맞는 완벽한 공간',
                'description': f'{main_value}. 전문가의 눈으로 검증된 우수 매물만을 추천드립니다.',
                'cta_primary': 'VR 투어 시작',
                'cta_secondary': '맞춤 매물 추천받기'
            },
            'features': [
                {
                    'icon': '🏠',
                    'title': '검증된 프리미엄 매물',
                    'description': '전문가가 직접 방문하여 검증한 우수 매물만 선별'
                },
                {
                    'icon': '📍',
                    'title': 'AI 입지 분석',
                    'description': '빅데이터 기반 교통, 학군, 편의시설 종합 분석'
                },
                {
                    'icon': '💼',
                    'title': '20년 경력 전문가',
                    'description': '지역별 전문 공인중개사의 맞춤 컨설팅'
                },
                {
                    'icon': '📈',
                    'title': '투자 가치 분석',
                    'description': '미래 가치와 수익률을 예측하는 전문 분석'
                },
                {
                    'icon': '🔍',
                    'title': 'VR 실감 투어',
                    'description': '방문 없이도 실제처럼 둘러보는 가상현실 투어'
                },
                {
                    'icon': '🔒',
                    'title': '안전한 에스크로',
                    'description': '계약부터 잔금까지 안전하게 보호되는 거래'
                }
            ],
            'trust_indicators': [
                {'number': '50,000+', 'label': '거래 완료'},
                {'number': '98%', 'label': '재방문율'},
                {'number': '4.9/5', 'label': '고객 평점'},
                {'number': '72시간', 'label': '평균 매칭'}
            ],
            'faq': [
                {
                    'question': '중개 수수료는 얼마인가요?',
                    'answer': '법정 수수료를 준수하며, 거래 금액에 따라 0.4~0.9%입니다. 상담 시 정확한 금액을 안내드립니다.'
                },
                {
                    'question': 'VR 투어는 무료인가요?',
                    'answer': '네, 모든 매물의 VR 투어는 무료로 제공됩니다. 스마트폰이나 PC에서 바로 체험 가능합니다.'
                },
                {
                    'question': '전세 자금 대출도 도와주시나요?',
                    'answer': '네, 제휴 금융기관을 통해 최적의 대출 조건을 찾아드립니다. 서류 준비부터 실행까지 전 과정을 지원합니다.'
                }
            ],
            'colors': {
                'primary': '#10b981',
                'secondary': '#34d399',
                'accent': '#86efac'
            }
        }
    
    @staticmethod
    def get_education_template(target, main_value):
        """교육 업종 전용 템플릿"""
        return {
            'hero': {
                'title': '당신의 성장을 위한 최고의 선택',
                'subtitle': f'{target}을 위한 체계적인 교육 프로그램',
                'description': f'{main_value}. 이론과 실무를 겸비한 전문가로 성장하세요.',
                'cta_primary': '무료 체험 신청',
                'cta_secondary': '커리큘럼 다운로드'
            },
            'features': [
                {
                    'icon': '👨‍🏫',
                    'title': '현직 전문가 강사진',
                    'description': '실무 경험이 풍부한 업계 최고 전문가들의 직강'
                },
                {
                    'icon': '📚',
                    'title': '체계적 커리큘럼',
                    'description': '기초부터 심화까지 단계별 맞춤 학습 설계'
                },
                {
                    'icon': '💻',
                    'title': '실습 중심 교육',
                    'description': '프로젝트 기반 학습으로 실무 역량 강화'
                },
                {
                    'icon': '📊',
                    'title': 'AI 학습 관리',
                    'description': '개인별 학습 패턴 분석 및 맞춤 코칭'
                },
                {
                    'icon': '🏆',
                    'title': '자격증 취득 지원',
                    'description': '시험 대비 특강 및 합격 보장 프로그램'
                },
                {
                    'icon': '🤝',
                    'title': '취업 연계 서비스',
                    'description': '우수 기업 채용 연계 및 이력서 코칭'
                }
            ],
            'trust_indicators': [
                {'number': '30,000+', 'label': '수강생'},
                {'number': '92%', 'label': '수료율'},
                {'number': '87%', 'label': '취업률'},
                {'number': '4.7/5', 'label': '강의 만족도'}
            ],
            'faq': [
                {
                    'question': '수업은 어떻게 진행되나요?',
                    'answer': '온라인 실시간 강의와 녹화 강의를 병행하며, 주 2회 실습 세션이 있습니다.'
                },
                {
                    'question': '수강 기간은 얼마나 되나요?',
                    'answer': '과정별로 다르지만 일반적으로 3-6개월이며, 수료 후에도 1년간 복습 가능합니다.'
                },
                {
                    'question': '환불 정책은 어떻게 되나요?',
                    'answer': '수강 시작 후 7일 이내 전액 환불 가능하며, 이후에는 잔여 기간에 따라 부분 환불됩니다.'
                }
            ],
            'colors': {
                'primary': '#8b5cf6',
                'secondary': '#a78bfa',
                'accent': '#c4b5fd'
            }
        }
    
    @staticmethod
    def get_healthcare_template(target, main_value):
        """의료/헬스케어 업종 전용 템플릿"""
        return {
            'hero': {
                'title': '건강한 삶을 위한 첫걸음',
                'subtitle': f'{target}의 건강을 지키는 전문 의료 서비스',
                'description': f'{main_value}. 최첨단 의료 장비와 전문 의료진이 함께합니다.',
                'cta_primary': '온라인 예약',
                'cta_secondary': '건강 검진 패키지'
            },
            'features': [
                {
                    'icon': '👨‍⚕️',
                    'title': '대학병원 출신 의료진',
                    'description': '각 분야 최고 전문의들의 정확한 진료'
                },
                {
                    'icon': '🏥',
                    'title': '최첨단 의료 장비',
                    'description': 'MRI, CT 등 최신 장비로 정밀한 검사'
                },
                {
                    'icon': '📱',
                    'title': '모바일 건강 관리',
                    'description': '검사 결과 확인부터 처방까지 앱으로 간편하게'
                },
                {
                    'icon': '🕐',
                    'title': '대기 시간 제로',
                    'description': '예약제 운영으로 기다림 없는 진료'
                },
                {
                    'icon': '💊',
                    'title': '맞춤형 건강 관리',
                    'description': '개인별 건강 상태에 따른 체계적 관리'
                },
                {
                    'icon': '🚑',
                    'title': '24시간 응급실',
                    'description': '언제든 이용 가능한 응급 의료 서비스'
                }
            ],
            'trust_indicators': [
                {'number': '100,000+', 'label': '진료 건수'},
                {'number': '98%', 'label': '환자 만족도'},
                {'number': '15년', 'label': '운영 경력'},
                {'number': '50+', 'label': '전문 의료진'}
            ],
            'faq': [
                {
                    'question': '예약은 어떻게 하나요?',
                    'answer': '홈페이지, 모바일 앱, 전화로 예약 가능하며, 당일 예약도 가능합니다.'
                },
                {
                    'question': '주차는 무료인가요?',
                    'answer': '네, 진료 시간에 따라 2-4시간 무료 주차가 제공됩니다.'
                },
                {
                    'question': '보험 적용이 되나요?',
                    'answer': '건강보험 및 실손보험 모두 적용 가능하며, 보험 청구 대행 서비스도 제공합니다.'
                }
            ],
            'colors': {
                'primary': '#06b6d4',
                'secondary': '#22d3ee',
                'accent': '#67e8f9'
            }
        }
    
    @staticmethod
    def get_ecommerce_template(target, main_value):
        """이커머스 업종 전용 템플릿"""
        return {
            'hero': {
                'title': '쇼핑의 새로운 기준',
                'subtitle': f'{target}을 위한 스마트한 쇼핑 경험',
                'description': f'{main_value}. 최저가 보장과 빠른 배송으로 만족을 드립니다.',
                'cta_primary': '베스트 상품 보기',
                'cta_secondary': '첫 구매 50% 할인'
            },
            'features': [
                {
                    'icon': '🛍️',
                    'title': '100만개 상품',
                    'description': '패션부터 가전까지 모든 카테고리 보유'
                },
                {
                    'icon': '💰',
                    'title': '최저가 보장',
                    'description': '더 저렴한 곳을 찾으면 차액의 2배 보상'
                },
                {
                    'icon': '🚚',
                    'title': '당일/새벽 배송',
                    'description': '오늘 주문하면 내일 아침 도착'
                },
                {
                    'icon': '♻️',
                    'title': '365일 교환/환불',
                    'description': '마음에 들지 않으면 언제든 반품 가능'
                },
                {
                    'icon': '💎',
                    'title': 'VIP 멤버십',
                    'description': '추가 할인과 무료 배송 혜택'
                },
                {
                    'icon': '🎁',
                    'title': '포인트 적립',
                    'description': '구매 금액의 5% 적립 및 현금처럼 사용'
                }
            ],
            'trust_indicators': [
                {'number': '500만+', 'label': '회원 수'},
                {'number': '4.8/5', 'label': '평균 평점'},
                {'number': '24시간', 'label': '평균 배송'},
                {'number': '99.9%', 'label': '정품 보장'}
            ],
            'faq': [
                {
                    'question': '배송료는 얼마인가요?',
                    'answer': '3만원 이상 구매 시 무료이며, 그 이하는 2,500원입니다. 새벽배송은 무조건 무료입니다.'
                },
                {
                    'question': '결제 수단은 무엇이 있나요?',
                    'answer': '신용카드, 계좌이체, 간편결제(카카오페이, 네이버페이 등), 포인트 결제가 가능합니다.'
                },
                {
                    'question': '교환/반품 비용은 누가 부담하나요?',
                    'answer': '단순 변심은 고객 부담, 상품 하자는 무료로 처리해드립니다.'
                }
            ],
            'colors': {
                'primary': '#f59e0b',
                'secondary': '#fbbf24',
                'accent': '#fcd34d'
            }
        }
    
    @staticmethod
    def get_finance_template(target, main_value):
        """금융/핀테크 업종 전용 템플릿"""
        return {
            'hero': {
                'title': '돈이 일하는 스마트한 방법',
                'subtitle': f'{target}을 위한 맞춤형 자산 관리',
                'description': f'{main_value}. AI가 분석하고 전문가가 관리하는 똑똑한 투자.',
                'cta_primary': '무료 포트폴리오 진단',
                'cta_secondary': '수익률 시뮬레이션'
            },
            'features': [
                {
                    'icon': '📊',
                    'title': 'AI 자산 분석',
                    'description': '빅데이터 기반 최적의 투자 포트폴리오 제안'
                },
                {
                    'icon': '💼',
                    'title': '전문가 자문',
                    'description': '15년 이상 경력의 자산관리사 1:1 상담'
                },
                {
                    'icon': '🔒',
                    'title': '안전한 보안',
                    'description': '금융감독원 인증 최고 수준 보안 시스템'
                },
                {
                    'icon': '📈',
                    'title': '높은 수익률',
                    'description': '시중 금리 대비 평균 3배 높은 수익'
                },
                {
                    'icon': '💳',
                    'title': '수수료 면제',
                    'description': '가입비, 운용 수수료 전액 면제'
                },
                {
                    'icon': '📱',
                    'title': '실시간 관리',
                    'description': '24시간 실시간 자산 현황 확인 및 거래'
                }
            ],
            'trust_indicators': [
                {'number': '3조원+', 'label': '운용 자산'},
                {'number': '12.5%', 'label': '평균 수익률'},
                {'number': '20만+', 'label': '투자자'},
                {'number': 'AAA', 'label': '신용 등급'}
            ],
            'faq': [
                {
                    'question': '최소 투자 금액은 얼마인가요?',
                    'answer': '최소 10만원부터 시작 가능하며, 적립식 투자는 월 1만원부터 가능합니다.'
                },
                {
                    'question': '원금 손실 위험은 없나요?',
                    'answer': '투자 상품의 특성상 원금 손실 가능성이 있으나, 리스크 관리 시스템으로 최소화합니다.'
                },
                {
                    'question': '중도 해지가 가능한가요?',
                    'answer': '언제든 가능하며, 영업일 기준 2-3일 내 출금 가능합니다.'
                }
            ],
            'colors': {
                'primary': '#0891b2',
                'secondary': '#06b6d4',
                'accent': '#22d3ee'
            }
        }
    
    @staticmethod
    def get_template(industry, target, main_value):
        """업종에 맞는 템플릿 반환"""
        
        # 업종 키워드 매칭
        if any(keyword in industry for keyword in ['보험', '생명', '손해', '자동차보험']):
            return IndustryTemplates.get_insurance_template(target, main_value)
        
        elif any(keyword in industry for keyword in ['부동산', '아파트', '주택', '임대']):
            return IndustryTemplates.get_real_estate_template(target, main_value)
        
        elif any(keyword in industry for keyword in ['교육', '학원', '강의', '학습']):
            return IndustryTemplates.get_education_template(target, main_value)
        
        elif any(keyword in industry for keyword in ['병원', '의료', '헬스케어', '건강']):
            return IndustryTemplates.get_healthcare_template(target, main_value)
        
        elif any(keyword in industry for keyword in ['쇼핑', '이커머스', '온라인몰', '마켓']):
            return IndustryTemplates.get_ecommerce_template(target, main_value)
        
        elif any(keyword in industry for keyword in ['금융', '은행', '투자', '핀테크']):
            return IndustryTemplates.get_finance_template(target, main_value)
        
        else:
            # 기본 템플릿 반환
            return IndustryTemplates.get_default_template(target, main_value)
    
    @staticmethod
    def get_default_template(target, main_value):
        """기본 템플릿"""
        return {
            'hero': {
                'title': '비즈니스의 새로운 가능성',
                'subtitle': f'{target}을 위한 최적의 솔루션',
                'description': f'{main_value}. 전문성과 혁신으로 성공을 만들어갑니다.',
                'cta_primary': '무료 상담 신청',
                'cta_secondary': '서비스 알아보기'
            },
            'features': [
                {
                    'icon': '⚡',
                    'title': '빠른 처리',
                    'description': '효율적인 프로세스로 시간을 절약하세요'
                },
                {
                    'icon': '💎',
                    'title': '최고 품질',
                    'description': '업계 최고 수준의 품질을 보장합니다'
                },
                {
                    'icon': '🛡️',
                    'title': '신뢰성',
                    'description': '검증된 전문성으로 믿을 수 있습니다'
                },
                {
                    'icon': '🎯',
                    'title': '맞춤 서비스',
                    'description': '고객 니즈에 최적화된 솔루션'
                },
                {
                    'icon': '📞',
                    'title': '전문 상담',
                    'description': '전문가가 직접 상담해드립니다'
                },
                {
                    'icon': '💰',
                    'title': '합리적 가격',
                    'description': '투명하고 합리적인 가격 정책'
                }
            ],
            'trust_indicators': [
                {'number': '10,000+', 'label': '고객사'},
                {'number': '98%', 'label': '만족도'},
                {'number': '24/7', 'label': '지원'},
                {'number': '10년+', 'label': '경력'}
            ],
            'faq': [
                {
                    'question': '서비스 이용은 어떻게 시작하나요?',
                    'answer': '홈페이지에서 간단한 신청서 작성 후, 전문 상담사가 연락드려 안내해드립니다.'
                },
                {
                    'question': '비용은 어떻게 되나요?',
                    'answer': '서비스 종류와 규모에 따라 다르며, 무료 상담을 통해 정확한 견적을 제공합니다.'
                },
                {
                    'question': '계약 기간은 얼마나 되나요?',
                    'answer': '최소 계약 기간은 없으며, 고객님의 필요에 따라 유연하게 조정 가능합니다.'
                }
            ],
            'colors': {
                'primary': '#5046e5',
                'secondary': '#7c3aed',
                'accent': '#a855f7'
            }
        }