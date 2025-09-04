#!/usr/bin/env python3
"""
템플릿 변형에 대한 CSS 스타일
각 레이아웃 변형에 맞는 스타일 정의
"""

def get_hero_styles(hero_type: str, colors: dict) -> str:
    """히어로 섹션 스타일"""
    
    base_styles = f"""
        /* 기본 히어로 스타일 */
        .hero-centered, .hero-left, .hero-split, .hero-fullscreen {{
            position: relative;
            overflow: hidden;
        }}
        
        h1 {{
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 1.5rem;
        }}
        
        .subtitle {{
            font-size: clamp(1.1rem, 2vw, 1.5rem);
            opacity: 0.9;
            margin-bottom: 2rem;
        }}
        
        .cta-button {{
            display: inline-block;
            padding: 16px 40px;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            margin: 8px;
        }}
        
        .cta-button.primary {{
            background: white;
            color: {colors['primary']};
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .cta-button.primary:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .cta-button.secondary {{
            background: transparent;
            color: white;
            border: 2px solid white;
        }}
        
        .cta-button.secondary:hover {{
            background: white;
            color: {colors['primary']};
        }}
    """
    
    if hero_type == "centered":
        return base_styles + """
        /* 중앙 정렬 히어로 */
        .hero-centered {
            background: linear-gradient(135deg, """ + colors['primary'] + """ 0%, """ + colors['secondary'] + """ 100%);
            color: white;
            padding: 120px 20px;
            text-align: center;
            min-height: 90vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .hero-centered .hero-content {
            max-width: 900px;
            animation: fadeInUp 0.8s ease;
        }
        """
    
    elif hero_type == "left_aligned":
        return base_styles + """
        /* 좌측 정렬 히어로 */
        .hero-left {
            background: linear-gradient(135deg, """ + colors['primary'] + """ 0%, """ + colors['secondary'] + """ 100%);
            color: white;
            padding: 80px 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
        }
        
        .hero-left .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 24px;
            width: 100%;
        }
        
        .hero-left .hero-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }
        
        .hero-left .hero-content {
            animation: fadeInLeft 0.8s ease;
        }
        
        .hero-left .hero-visual {
            position: relative;
            animation: fadeInRight 0.8s ease;
        }
        
        .visual-placeholder {
            position: relative;
            height: 500px;
        }
        
        .floating-card {
            position: absolute;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 20px 30px;
            border-radius: 20px;
            font-size: 1.1rem;
            animation: float 3s ease-in-out infinite;
        }
        
        .floating-card.card-1 { top: 20%; left: 10%; animation-delay: 0s; }
        .floating-card.card-2 { top: 40%; right: 20%; animation-delay: 1s; }
        .floating-card.card-3 { bottom: 20%; left: 30%; animation-delay: 2s; }
        
        .trust-badges {
            margin-top: 30px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .trust-badges span {
            background: rgba(255,255,255,0.1);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        
        @media (max-width: 968px) {
            .hero-left .hero-grid {
                grid-template-columns: 1fr;
            }
            .hero-left .hero-visual {
                display: none;
            }
        }
        """
    
    elif hero_type == "split":
        return base_styles + """
        /* 분할형 히어로 */
        .hero-split {
            min-height: 100vh;
            display: flex;
        }
        
        .split-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            width: 100%;
        }
        
        .split-left {
            background: linear-gradient(135deg, """ + colors['primary'] + """ 0%, """ + colors['secondary'] + """ 100%);
            color: white;
            display: flex;
            align-items: center;
            padding: 60px;
        }
        
        .split-content {
            max-width: 600px;
            animation: fadeInLeft 0.8s ease;
        }
        
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }
        
        .feature-list {
            margin: 30px 0;
        }
        
        .feature-item {
            padding: 10px 0;
            font-size: 1.1rem;
        }
        
        .cta-button.large {
            padding: 20px 50px;
            font-size: 1.2rem;
        }
        
        .split-right {
            background: #f8f9fa;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 60px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 30px;
            animation: fadeInRight 0.8s ease;
        }
        
        .stat-card {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 800;
            color: """ + colors['primary'] + """;
            margin-bottom: 10px;
        }
        
        .stat-label {
            color: #666;
            font-size: 1rem;
        }
        
        @media (max-width: 968px) {
            .split-container {
                grid-template-columns: 1fr;
            }
            .split-right {
                padding: 40px;
            }
        }
        """
    
    elif hero_type == "fullscreen":
        return base_styles + """
        /* 풀스크린 히어로 */
        .hero-fullscreen {
            min-height: 100vh;
            background: linear-gradient(135deg, """ + colors['primary'] + """ 0%, """ + colors['secondary'] + """ 100%);
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .hero-fullscreen::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,154.7C960,171,1056,181,1152,165.3C1248,149,1344,107,1392,85.3L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
            background-size: cover;
            background-position: bottom;
            opacity: 0.3;
        }
        
        .fullscreen-overlay {
            position: relative;
            z-index: 1;
            text-align: center;
            padding: 40px;
            width: 100%;
            max-width: 1200px;
        }
        
        .mega-headline h1 {
            font-size: clamp(3rem, 8vw, 5rem);
            margin-bottom: 2rem;
            animation: fadeInScale 1s ease;
        }
        
        .mega-subtitle {
            font-size: clamp(1.3rem, 3vw, 2rem);
            margin-bottom: 3rem;
            opacity: 0.95;
            animation: fadeInUp 1s ease 0.2s both;
        }
        
        .cta-area {
            animation: fadeInUp 1s ease 0.4s both;
        }
        
        .mega-button {
            padding: 24px 60px;
            font-size: 1.3rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .cta-hint {
            margin-top: 20px;
            font-size: 1rem;
            opacity: 0.9;
        }
        
        .scroll-indicator {
            position: absolute;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            animation: bounce 2s infinite;
        }
        
        .scroll-arrow {
            font-size: 2rem;
            margin-top: 10px;
        }
        
        @keyframes fadeInScale {
            from {
                opacity: 0;
                transform: scale(0.8);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateX(-50%) translateY(0); }
            40% { transform: translateX(-50%) translateY(-10px); }
            60% { transform: translateX(-50%) translateY(-5px); }
        }
        """
    
    return base_styles


def get_features_styles(features_type: str, colors: dict) -> str:
    """특징 섹션 스타일"""
    
    base_styles = """
        /* 기본 특징 섹션 스타일 */
        .features-grid, .features-list, .features-timeline, .features-hover {
            padding: 80px 20px;
            background: #f8f9fa;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 3rem;
            color: #1a1a1a;
        }
    """
    
    if features_type == "grid":
        return base_styles + """
        /* 그리드형 특징 */
        .features-container.grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
        }
        
        .feature-card {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.12);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1.5rem;
        }
        
        .feature-title {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #1a1a1a;
        }
        
        .feature-description {
            color: #666;
            line-height: 1.8;
        }
        """
    
    elif features_type == "list":
        return base_styles + """
        /* 리스트형 특징 */
        .features-list-container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .feature-list-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 40px;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        .feature-list-item:hover {
            transform: translateX(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        }
        
        .feature-number {
            font-size: 2rem;
            font-weight: 800;
            color: """ + colors['primary'] + """;
            margin-right: 30px;
            min-width: 60px;
        }
        
        .feature-content h3 {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }
        
        .feature-content p {
            color: #666;
            line-height: 1.6;
        }
        """
    
    elif features_type == "timeline":
        return base_styles + """
        /* 타임라인형 특징 */
        .timeline-container {
            position: relative;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 0;
        }
        
        .timeline-line {
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, """ + colors['primary'] + """, """ + colors['secondary'] + """);
            transform: translateX(-50%);
        }
        
        .timeline-item {
            position: relative;
            margin-bottom: 60px;
            width: 45%;
        }
        
        .timeline-item.left {
            left: 0;
            text-align: right;
        }
        
        .timeline-item.right {
            left: 55%;
            text-align: left;
        }
        
        .timeline-marker {
            position: absolute;
            width: 50px;
            height: 50px;
            background: white;
            border: 3px solid """ + colors['primary'] + """;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            top: 0;
        }
        
        .timeline-item.left .timeline-marker {
            right: -27px;
        }
        
        .timeline-item.right .timeline-marker {
            left: -27px;
        }
        
        .timeline-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .timeline-content h3 {
            font-size: 1.4rem;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }
        
        .timeline-content p {
            color: #666;
            line-height: 1.6;
        }
        
        @media (max-width: 768px) {
            .timeline-line { left: 30px; }
            .timeline-item { width: calc(100% - 60px); left: 60px !important; text-align: left !important; }
            .timeline-item .timeline-marker { left: -27px !important; }
        }
        """
    
    elif features_type == "cards_hover":
        return base_styles + """
        /* 호버 카드형 특징 */
        .hover-cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
        }
        
        .hover-card {
            position: relative;
            height: 300px;
            perspective: 1000px;
        }
        
        .card-front, .card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 20px;
            padding: 30px;
            transition: transform 0.6s;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .card-front {
            background: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .card-back {
            background: linear-gradient(135deg, """ + colors['primary'] + """, """ + colors['secondary'] + """);
            color: white;
            transform: rotateY(180deg);
        }
        
        .hover-card:hover .card-front {
            transform: rotateY(-180deg);
        }
        
        .hover-card:hover .card-back {
            transform: rotateY(0);
        }
        
        .card-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .card-front h3 {
            font-size: 1.4rem;
            color: #1a1a1a;
        }
        
        .card-back p {
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        
        .learn-more {
            color: white;
            text-decoration: none;
            font-weight: 600;
            border-bottom: 2px solid white;
            transition: transform 0.3s ease;
        }
        
        .learn-more:hover {
            transform: translateX(5px);
        }
        """
    
    return base_styles


def get_animation_styles() -> str:
    """공통 애니메이션 스타일"""
    return """
        /* 애니메이션 */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes fadeInRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
    """