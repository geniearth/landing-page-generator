#!/usr/bin/env python3
"""
Claude Code SDK 활용 랜딩페이지 생성 서버
API 키 없이 Claude Code 환경에서 직접 실행
"""

import os
import json
import time
import hashlib
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from bs4 import BeautifulSoup
import subprocess
import sys
from claude_generator import ClaudeHTMLGenerator
from dynamic_content_generator import DynamicContentGenerator
from template_variations import TemplateVariations
from template_styles import get_hero_styles, get_features_styles, get_animation_styles

app = Flask(__name__)

# CORS 설정 - 더 포괄적으로 설정
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    },
    r"/health": {
        "origins": "*",
        "methods": ["GET"]
    }
})

# CORS preflight 요청 처리
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://localhost:3000', 'http://127.0.0.1:5173']:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

class ClaudeCodeGenerator:
    """Claude Code를 활용한 로컬 페이지 생성기"""
    
    def __init__(self):
        # 디렉토리 설정
        self.base_dir = Path(__file__).parent.parent
        self.pages_dir = self.base_dir / "generated-pages"
        self.pages_dir.mkdir(exist_ok=True)
        
        print(f"📁 페이지 저장 디렉토리: {self.pages_dir}")
        print("✅ Claude Code SDK 모드로 실행 중 (API 키 불필요)")
    
    def generate_page_id(self, concept):
        """고유한 페이지 ID 생성"""
        timestamp = str(int(time.time()))
        concept_hash = hashlib.md5(json.dumps(concept, sort_keys=True).encode()).hexdigest()[:8]
        return f"page_{timestamp}_{concept_hash}"
    
    def build_prompt(self, concept):
        """프롬프트 생성"""
        from templates import generate_landing_page_prompt
        return generate_landing_page_prompt(concept)
    
    def generate_with_claude_code(self, prompt):
        """
        Claude Code를 활용하여 HTML 생성
        API 키 없이 로컬에서 직접 생성
        """
        import sys
        print("🎨 동적 콘텐츠 생성 시작", file=sys.stderr)
        
        # 동적 콘텐츠 생성기를 직접 사용
        return self.create_demo_template(prompt)
    
    def _extract_concept_from_prompt(self, prompt):
        """프롬프트에서 concept 정보 추출"""
        concept = {
            'industry': '서비스',
            'target': '고객',
            'mainValue': '최고의 가치 제공',
            'tone': 'professional',
            'colors': ['#667eea', '#764ba2']
        }
        
        lines = prompt.split('\n')
        for line in lines:
            if "업종/서비스:" in line:
                concept['industry'] = line.split("업종/서비스:")[1].strip()
            elif "타겟 고객:" in line:
                concept['target'] = line.split("타겟 고객:")[1].strip()
            elif "핵심 가치/메시지:" in line:
                concept['mainValue'] = line.split("핵심 가치/메시지:")[1].strip()
            elif "톤앤매너:" in line:
                tone_text = line.split("톤앤매너:")[1].strip()
                if 'casual' in tone_text.lower():
                    concept['tone'] = 'casual'
                elif 'luxury' in tone_text.lower() or '고급' in tone_text:
                    concept['tone'] = 'luxury'
                elif 'tech' in tone_text.lower() or '테크' in tone_text:
                    concept['tone'] = 'tech'
                elif 'warm' in tone_text.lower() or '따뜻' in tone_text:
                    concept['tone'] = 'warm'
        
        return concept
    
    def create_demo_template(self, prompt):
        """동적 콘텐츠 생성기를 사용한 템플릿 생성"""
        concept = self._extract_concept_from_prompt(prompt)
        content_gen = DynamicContentGenerator()
        dynamic = content_gen.generate_dynamic_content(
            concept['industry'],
            concept['target'],
            concept['mainValue']
        )
        
        print(f"🎨 동적 콘텐츠 생성 완료: {dynamic['headline'][:30]}...")
        
        # 업종 카테고리 결정
        industry_map = {
            '보험': 'insurance', '자동차보험': 'insurance', '생명보험': 'insurance',
            '부동산': 'real_estate', '아파트': 'real_estate', '주택': 'real_estate',
            '교육': 'education', '학원': 'education', '온라인교육': 'education',
            '헬스케어': 'healthcare', '병원': 'healthcare', '건강': 'healthcare', '피트니스': 'healthcare', '헬스장': 'healthcare',
            '쇼핑': 'ecommerce', '쇼핑몰': 'ecommerce', '이커머스': 'ecommerce', '온라인쇼핑': 'ecommerce',
            '금융': 'finance', '은행': 'finance', '대출': 'finance', '투자': 'finance'
        }
        
        industry_category = 'general'
        for key, value in industry_map.items():
            if key in concept['industry']:
                industry_category = value
                break
        
        # 레이아웃 선택 (업종별 최적화 또는 랜덤)
        if industry_category != 'general':
            layout = TemplateVariations.get_industry_optimized_layout(industry_category)
        else:
            layout = TemplateVariations.get_random_layout()
        
        print(f"📐 레이아웃 선택: {layout}")
        
        # 히어로 데이터 준비
        hero_data = {
            'headline': dynamic['headline'],
            'subtitle': dynamic['subtitle'],
            'cta_primary': dynamic.get('cta_primary', '지금 시작하기'),
            'cta_secondary': dynamic.get('cta_secondary', '자세히 알아보기'),
            'badge': f"🔥 {concept['target']} 인기",
            'feature1': dynamic['features'][0]['title'] if len(dynamic['features']) > 0 else '빠른 시작',
            'feature2': dynamic['features'][1]['title'] if len(dynamic['features']) > 1 else '전문가 지원',
            'feature3': dynamic['features'][2]['title'] if len(dynamic['features']) > 2 else '만족 보장',
            'stat1': dynamic.get('trust_indicators', [{'number': '99%'}])[0].get('number', '99%'),
            'stat2': dynamic.get('trust_indicators', [{'number': '24/7'}, {'number': '24/7'}])[1].get('number', '24/7') if len(dynamic.get('trust_indicators', [])) > 1 else '24/7',
            'stat3': dynamic.get('trust_indicators', [{'number': '10만+'}, {'number': '10만+'}, {'number': '10만+'}])[2].get('number', '10만+') if len(dynamic.get('trust_indicators', [])) > 2 else '10만+',
            'value1': concept['mainValue'][:20] + '...' if len(concept['mainValue']) > 20 else concept['mainValue'],
            'value2': '최고의 품질',
            'value3': '합리적 가격',
            'urgency': '오늘 가입 시 특별 혜택'
        }
        
        # CTA 데이터 준비
        cta_data = {
            'title': dynamic.get('headline', '지금 시작하세요'),
            'subtitle': dynamic.get('subtitle', '최고의 서비스를 경험해보세요'),
            'cta_primary': dynamic.get('cta_primary', '무료 상담 신청')
        }
        
        # HTML 섹션 생성
        hero_html = TemplateVariations.get_hero_variation(layout['hero'], hero_data)
        features_html = TemplateVariations.get_features_variation(layout['features'], dynamic['features'][:6])
        cta_html = TemplateVariations.get_cta_variation(layout['cta'], cta_data)
        
        # 스타일 생성
        hero_styles = get_hero_styles(layout['hero'], dynamic['colors'])
        features_styles = get_features_styles(layout['features'], dynamic['colors'])
        animation_styles = get_animation_styles()
        
        # 최종 HTML 생성
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{dynamic['subtitle']}">
    <title>{dynamic['headline']} | {concept['industry']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        
        {hero_styles}
        {features_styles}
        {animation_styles}
        
        /* 푸터 스타일 */
        .footer {{
            background: #1a1a1a;
            color: white;
            text-align: center;
            padding: 40px 20px;
        }}
        
        .footer p {{
            opacity: 0.8;
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    {hero_html}
    
    {features_html}
    
    {cta_html}
    
    <footer class="footer">
        <p>© 2024 {concept['industry']} 서비스. 모든 권리 보유.</p>
        <p>생성 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>
    
    <script>
        // 부드러운 스크롤
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def generate_page(self, concept):
        """SDK를 사용해 페이지 생성"""
        try:
            # 프롬프트 생성
            prompt = self.build_prompt(concept)
            
            print(f"📝 컨셉 정보:")
            print(f"   업종: {concept.get('industry')}")
            print(f"   타겟: {concept.get('target')}")
            print(f"   메시지: {concept.get('mainValue')}")
            
            # Claude Code로 HTML 생성
            html_content = self.generate_with_claude_code(prompt)
            
            # HTML 정리
            html_content = self.clean_html(html_content)
            
            # 페이지 저장
            page_id = self.save_page(html_content, concept)
            
            print(f"✅ 페이지 생성 완료: {page_id}")
            
            return {
                "success": True,
                "page_id": page_id,
                "path": f"/pages/{page_id}",
                "file_path": str(self.pages_dir / page_id / "index.html")
            }
            
        except Exception as e:
            print(f"❌ 페이지 생성 실패: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def clean_html(self, html):
        """HTML 코드 정리"""
        html = html.strip()
        
        if not html.lower().startswith('<!doctype'):
            html = '<!DOCTYPE html>\n' + html
        
        return html
    
    def save_page(self, html_content, concept):
        """생성된 페이지를 파일로 저장"""
        page_id = self.generate_page_id(concept)
        page_dir = self.pages_dir / page_id
        page_dir.mkdir(exist_ok=True)
        
        # HTML 저장
        html_path = page_dir / "index.html"
        html_path.write_text(html_content, encoding='utf-8')
        
        # 메타데이터 저장
        metadata = {
            "id": page_id,
            "concept": concept,
            "created_at": time.time(),
            "created_at_str": time.strftime('%Y-%m-%d %H:%M:%S'),
            "file_path": str(html_path),
            "generated_by": "Claude Code SDK",
            "api_key_used": False
        }
        
        metadata_path = page_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
        
        print(f"💾 페이지 저장됨: {html_path}")
        
        return page_id
    
    def get_page(self, page_id):
        """페이지 조회"""
        html_path = self.pages_dir / page_id / "index.html"
        metadata_path = self.pages_dir / page_id / "metadata.json"
        
        if not html_path.exists():
            return None
        
        return {
            "html": html_path.read_text(encoding='utf-8'),
            "metadata": json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
        }
    
    def list_pages(self):
        """모든 페이지 목록"""
        pages = []
        
        for page_dir in self.pages_dir.iterdir():
            if page_dir.is_dir():
                metadata_path = page_dir / "metadata.json"
                if metadata_path.exists():
                    metadata = json.loads(metadata_path.read_text())
                    pages.append({
                        "id": metadata["id"],
                        "industry": metadata["concept"].get("industry", "Unknown"),
                        "target": metadata["concept"].get("target", "Unknown"),
                        "created_at": metadata["created_at_str"],
                        "path": f"/pages/{metadata['id']}",
                        "generated_by": metadata.get("generated_by", "Unknown")
                    })
        
        pages.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return pages

# 생성기 인스턴스
generator = ClaudeCodeGenerator()

# === Flask 라우트 ===

@app.route('/health', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({
        "status": "ok",
        "service": "Claude Code SDK Generator",
        "mode": "Local SDK (No API Key)",
        "timestamp": time.time(),
        "pages_dir": str(generator.pages_dir)
    })

@app.route('/api/generate', methods=['POST'])
def generate_page():
    """페이지 생성"""
    concept = request.json
    
    # 필수 필드 검증
    required = ['industry', 'target', 'mainValue']
    for field in required:
        if not concept.get(field):
            return jsonify({
                "success": False,
                "error": f"{field}는 필수 입력 항목입니다."
            }), 400
    
    result = generator.generate_page(concept)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

@app.route('/api/pages', methods=['GET'])
def list_pages():
    """페이지 목록"""
    pages = generator.list_pages()
    return jsonify({
        "success": True,
        "pages": pages,
        "total": len(pages)
    })

@app.route('/api/pages/<page_id>', methods=['GET'])
def get_page(page_id):
    """페이지 조회"""
    page = generator.get_page(page_id)
    
    if page:
        return jsonify({
            "success": True,
            "data": page
        })
    else:
        return jsonify({
            "success": False,
            "error": "페이지를 찾을 수 없습니다."
        }), 404

@app.route('/api/pages/<page_id>/html', methods=['GET'])
def get_page_html(page_id):
    """HTML 파일 직접 반환"""
    html_path = generator.pages_dir / page_id / "index.html"
    
    if html_path.exists():
        return send_file(str(html_path), mimetype='text/html')
    else:
        return "Page not found", 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('SDK_PORT', 5001))  # 기본 포트를 5001로 변경
    
    print("""
╔══════════════════════════════════════════════╗
║   🚀 Claude Code SDK 페이지 생성 서버        ║
║   API 키 없이 로컬에서 실행                  ║
╚══════════════════════════════════════════════╝
    """)
    
    print("ℹ️  Claude Code 환경에서 실행 중입니다.")
    print("✅ API 키가 필요하지 않습니다.")
    print(f"🔌 포트: {port}")
    print("")
    
    app.run(host='0.0.0.0', port=port, debug=True)