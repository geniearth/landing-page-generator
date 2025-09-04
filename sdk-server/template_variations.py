#!/usr/bin/env python3
"""
다양한 레이아웃 템플릿 변형
각 섹션별로 여러 변형을 제공하여 다양한 디자인 생성
"""

import random
from typing import Dict, Any

class TemplateVariations:
    """템플릿 변형 관리자"""
    
    @staticmethod
    def get_hero_variation(variation_type: str, data: Dict[str, Any]) -> str:
        """히어로 섹션 변형"""
        
        if variation_type == "centered":
            # 중앙 정렬형 (기본)
            return f"""
    <section class="hero-centered">
        <div class="hero-content">
            <h1>{data['headline']}</h1>
            <p class="subtitle">{data['subtitle']}</p>
            <div class="cta-buttons">
                <a href="#" class="cta-button primary">{data['cta_primary']}</a>
                <a href="#" class="cta-button secondary">{data.get('cta_secondary', '자세히 알아보기')}</a>
            </div>
        </div>
    </section>"""
        
        elif variation_type == "left_aligned":
            # 좌측 정렬형
            return f"""
    <section class="hero-left">
        <div class="container">
            <div class="hero-grid">
                <div class="hero-content">
                    <h1>{data['headline']}</h1>
                    <p class="subtitle">{data['subtitle']}</p>
                    <div class="cta-buttons">
                        <a href="#" class="cta-button primary">{data['cta_primary']}</a>
                    </div>
                    <div class="trust-badges">
                        <span>⭐ 4.9/5 평점</span>
                        <span>🏆 2024 최우수상</span>
                        <span>🔒 100% 안전</span>
                    </div>
                </div>
                <div class="hero-visual">
                    <div class="visual-placeholder">
                        <div class="floating-card card-1">✨ {data.get('value1', '빠른 처리')}</div>
                        <div class="floating-card card-2">🎯 {data.get('value2', '맞춤 서비스')}</div>
                        <div class="floating-card card-3">💎 {data.get('value3', '최고 품질')}</div>
                    </div>
                </div>
            </div>
        </div>
    </section>"""
        
        elif variation_type == "split":
            # 분할형 (50/50)
            return f"""
    <section class="hero-split">
        <div class="split-container">
            <div class="split-left">
                <div class="split-content">
                    <span class="badge">{data.get('badge', '🚀 NEW')}</span>
                    <h1>{data['headline']}</h1>
                    <p class="subtitle">{data['subtitle']}</p>
                    <div class="feature-list">
                        <div class="feature-item">✅ {data.get('feature1', '간편한 시작')}</div>
                        <div class="feature-item">✅ {data.get('feature2', '전문가 지원')}</div>
                        <div class="feature-item">✅ {data.get('feature3', '만족 보장')}</div>
                    </div>
                    <a href="#" class="cta-button primary large">{data['cta_primary']}</a>
                </div>
            </div>
            <div class="split-right">
                <div class="visual-content">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">{data.get('stat1', '99%')}</div>
                            <div class="stat-label">만족도</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{data.get('stat2', '24/7')}</div>
                            <div class="stat-label">지원</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{data.get('stat3', '10만+')}</div>
                            <div class="stat-label">고객</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>"""
        
        elif variation_type == "fullscreen":
            # 풀스크린형
            return f"""
    <section class="hero-fullscreen">
        <div class="fullscreen-overlay">
            <div class="fullscreen-content">
                <div class="mega-headline">
                    <h1>{data['headline']}</h1>
                </div>
                <p class="mega-subtitle">{data['subtitle']}</p>
                <div class="cta-area">
                    <a href="#" class="cta-button mega-button">{data['cta_primary']}</a>
                    <p class="cta-hint">🔥 {data.get('urgency', '지금 가입하면 50% 할인')}</p>
                </div>
            </div>
            <div class="scroll-indicator">
                <span>스크롤하여 더 알아보기</span>
                <div class="scroll-arrow">↓</div>
            </div>
        </div>
    </section>"""
        
        else:
            # 기본값
            return TemplateVariations.get_hero_variation("centered", data)
    
    @staticmethod
    def get_features_variation(variation_type: str, features: list) -> str:
        """특징 섹션 변형"""
        
        if variation_type == "grid":
            # 그리드형 (기본)
            features_html = '\n'.join([f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature.get('icon', '✨')}</div>
                    <h3 class="feature-title">{feature['title']}</h3>
                    <p class="feature-description">{feature['description']}</p>
                </div>""" for feature in features])
            
            return f"""
    <section class="features-grid">
        <div class="container">
            <h2 class="section-title">핵심 특징</h2>
            <div class="features-container grid-3">
                {features_html}
            </div>
        </div>
    </section>"""
        
        elif variation_type == "list":
            # 리스트형
            features_html = '\n'.join([f"""
                <div class="feature-list-item">
                    <div class="feature-number">{i+1:02d}</div>
                    <div class="feature-content">
                        <h3>{feature['title']}</h3>
                        <p>{feature['description']}</p>
                    </div>
                </div>""" for i, feature in enumerate(features)])
            
            return f"""
    <section class="features-list">
        <div class="container">
            <h2 class="section-title">우리가 제공하는 가치</h2>
            <div class="features-list-container">
                {features_html}
            </div>
        </div>
    </section>"""
        
        elif variation_type == "timeline":
            # 타임라인형
            features_html = '\n'.join([f"""
                <div class="timeline-item {'left' if i % 2 == 0 else 'right'}">
                    <div class="timeline-marker">{feature.get('icon', '🎯')}</div>
                    <div class="timeline-content">
                        <h3>{feature['title']}</h3>
                        <p>{feature['description']}</p>
                    </div>
                </div>""" for i, feature in enumerate(features)])
            
            return f"""
    <section class="features-timeline">
        <div class="container">
            <h2 class="section-title">성공으로 가는 단계</h2>
            <div class="timeline-container">
                <div class="timeline-line"></div>
                {features_html}
            </div>
        </div>
    </section>"""
        
        elif variation_type == "cards_hover":
            # 호버 효과 카드형
            features_html = '\n'.join([f"""
                <div class="hover-card">
                    <div class="card-front">
                        <div class="card-icon">{feature.get('icon', '💡')}</div>
                        <h3>{feature['title']}</h3>
                    </div>
                    <div class="card-back">
                        <p>{feature['description']}</p>
                        <a href="#" class="learn-more">자세히 보기 →</a>
                    </div>
                </div>""" for feature in features])
            
            return f"""
    <section class="features-hover">
        <div class="container">
            <h2 class="section-title">더 알아보기</h2>
            <div class="hover-cards-container">
                {features_html}
            </div>
        </div>
    </section>"""
        
        else:
            return TemplateVariations.get_features_variation("grid", features)
    
    @staticmethod
    def get_cta_variation(variation_type: str, data: Dict[str, Any]) -> str:
        """CTA 섹션 변형"""
        
        if variation_type == "simple":
            # 심플형
            return f"""
    <section class="cta-simple">
        <div class="container">
            <h2>{data.get('title', '지금 시작하세요')}</h2>
            <p>{data.get('subtitle', '더 나은 미래를 위한 첫 걸음')}</p>
            <a href="#" class="cta-button primary large">{data['cta_primary']}</a>
        </div>
    </section>"""
        
        elif variation_type == "with_form":
            # 폼 포함형
            return f"""
    <section class="cta-form">
        <div class="container">
            <div class="cta-grid">
                <div class="cta-content">
                    <h2>{data.get('title', '무료 상담 신청')}</h2>
                    <p>{data.get('subtitle', '전문가가 직접 연락드립니다')}</p>
                    <ul class="benefits-list">
                        <li>✅ 무료 상담</li>
                        <li>✅ 맞춤 제안</li>
                        <li>✅ 부담 없는 상담</li>
                    </ul>
                </div>
                <div class="cta-form-container">
                    <form class="contact-form">
                        <input type="text" placeholder="이름" required>
                        <input type="tel" placeholder="연락처" required>
                        <input type="email" placeholder="이메일" required>
                        <select>
                            <option>관심 서비스 선택</option>
                            <option>기본 패키지</option>
                            <option>프리미엄 패키지</option>
                            <option>맞춤 상담</option>
                        </select>
                        <button type="submit" class="submit-button">{data['cta_primary']}</button>
                    </form>
                </div>
            </div>
        </div>
    </section>"""
        
        elif variation_type == "countdown":
            # 카운트다운형
            return f"""
    <section class="cta-countdown">
        <div class="container">
            <div class="countdown-wrapper">
                <h2>🔥 {data.get('title', '한정 특가 이벤트')}</h2>
                <div class="countdown-timer">
                    <div class="time-unit">
                        <span class="time-value">23</span>
                        <span class="time-label">시간</span>
                    </div>
                    <div class="time-unit">
                        <span class="time-value">59</span>
                        <span class="time-label">분</span>
                    </div>
                    <div class="time-unit">
                        <span class="time-value">59</span>
                        <span class="time-label">초</span>
                    </div>
                </div>
                <p class="offer-text">{data.get('subtitle', '지금 가입하면 50% 할인')}</p>
                <a href="#" class="cta-button urgent">{data['cta_primary']}</a>
            </div>
        </div>
    </section>"""
        
        else:
            return TemplateVariations.get_cta_variation("simple", data)
    
    @staticmethod
    def get_random_layout():
        """랜덤 레이아웃 조합 생성"""
        hero_types = ["centered", "left_aligned", "split", "fullscreen"]
        features_types = ["grid", "list", "timeline", "cards_hover"]
        cta_types = ["simple", "with_form", "countdown"]
        
        return {
            'hero': random.choice(hero_types),
            'features': random.choice(features_types),
            'cta': random.choice(cta_types)
        }
    
    @staticmethod
    def get_industry_optimized_layout(industry: str):
        """업종별 최적화된 레이아웃"""
        layouts = {
            'insurance': {
                'hero': 'split',
                'features': 'list',
                'cta': 'with_form'
            },
            'real_estate': {
                'hero': 'fullscreen',
                'features': 'grid',
                'cta': 'with_form'
            },
            'education': {
                'hero': 'left_aligned',
                'features': 'timeline',
                'cta': 'simple'
            },
            'healthcare': {
                'hero': 'split',
                'features': 'grid',
                'cta': 'with_form'
            },
            'ecommerce': {
                'hero': 'fullscreen',
                'features': 'cards_hover',
                'cta': 'countdown'
            },
            'finance': {
                'hero': 'left_aligned',
                'features': 'list',
                'cta': 'with_form'
            }
        }
        
        # 업종이 없으면 랜덤
        return layouts.get(industry, TemplateVariations.get_random_layout())