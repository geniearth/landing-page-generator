#!/usr/bin/env python3
"""
Claude SDK 기반 랜딩페이지 생성 서버
로컬에서 실행되며 파일 시스템에 직접 페이지를 생성합니다.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from anthropic import Anthropic
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# 환경변수 로드
load_dotenv(Path(__file__).parent.parent / '.env')

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

class LocalPageGenerator:
    """Claude SDK를 사용한 로컬 페이지 생성기"""
    
    def __init__(self):
        # Claude SDK 초기화
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        
        self.client = Anthropic(api_key=api_key)
        
        # 디렉토리 설정
        self.base_dir = Path(__file__).parent.parent
        self.pages_dir = self.base_dir / "generated-pages"
        self.pages_dir.mkdir(exist_ok=True)
        
        print(f"📁 페이지 저장 디렉토리: {self.pages_dir}")
    
    def generate_page_id(self, concept):
        """고유한 페이지 ID 생성"""
        timestamp = str(int(time.time()))
        concept_hash = hashlib.md5(json.dumps(concept, sort_keys=True).encode()).hexdigest()[:8]
        return f"page_{timestamp}_{concept_hash}"
    
    def build_prompt(self, concept):
        """프롬프트 생성"""
        from templates import generate_landing_page_prompt
        return generate_landing_page_prompt(concept)
    
    def generate_page(self, concept):
        """SDK를 사용해 페이지 생성"""
        try:
            # 프롬프트 생성
            prompt = self.build_prompt(concept)
            
            print(f"🤖 Claude SDK로 페이지 생성 중...")
            print(f"   업종: {concept.get('industry')}")
            print(f"   타겟: {concept.get('target')}")
            
            # Claude API 호출
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # 응답에서 HTML 추출
            html_content = message.content[0].text
            
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
        # 코드 블록 제거
        html = html.replace('```html', '').replace('```', '')
        html = html.strip()
        
        # DOCTYPE 확인
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
            "versions": []
        }
        
        metadata_path = page_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
        
        # 초기 버전 저장
        version_dir = page_dir / "versions"
        version_dir.mkdir(exist_ok=True)
        
        version_file = version_dir / f"v1_{int(time.time())}.html"
        version_file.write_text(html_content, encoding='utf-8')
        
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
                        "path": f"/pages/{metadata['id']}"
                    })
        
        # 최신순으로 정렬
        pages.sort(key=lambda x: x["created_at"], reverse=True)
        
        return pages
    
    def edit_page(self, page_id, edits):
        """페이지 편집"""
        html_path = self.pages_dir / page_id / "index.html"
        
        if not html_path.exists():
            return False
        
        # 현재 HTML 읽기
        html = html_path.read_text(encoding='utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # 편집 적용
        for edit in edits:
            selector = edit.get('selector')
            value = edit.get('value')
            property_type = edit.get('property', 'text')
            
            element = soup.select_one(selector)
            if element:
                if property_type == 'text':
                    element.string = value
                elif property_type == 'html':
                    element.clear()
                    element.append(BeautifulSoup(value, 'html.parser'))
        
        # 버전 저장
        version_dir = self.pages_dir / page_id / "versions"
        version_dir.mkdir(exist_ok=True)
        
        version_count = len(list(version_dir.glob("*.html"))) + 1
        version_file = version_dir / f"v{version_count}_{int(time.time())}.html"
        version_file.write_text(html, encoding='utf-8')  # 이전 버전 저장
        
        # 수정된 HTML 저장
        new_html = str(soup)
        html_path.write_text(new_html, encoding='utf-8')
        
        print(f"✏️ 페이지 수정됨: {page_id}")
        
        return True

# 생성기 인스턴스
generator = LocalPageGenerator()

# === Flask 라우트 ===

@app.route('/health', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({
        "status": "ok",
        "service": "SDK Page Generator",
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

@app.route('/api/pages/<page_id>/edit', methods=['PUT'])
def edit_page(page_id):
    """페이지 편집"""
    edits = request.json.get('edits', [])
    
    if generator.edit_page(page_id, edits):
        return jsonify({
            "success": True,
            "message": "페이지가 수정되었습니다."
        })
    else:
        return jsonify({
            "success": False,
            "error": "페이지 수정에 실패했습니다."
        }), 500

@app.route('/api/pages/<page_id>/versions', methods=['GET'])
def get_versions(page_id):
    """버전 목록"""
    version_dir = generator.pages_dir / page_id / "versions"
    
    if not version_dir.exists():
        return jsonify({"versions": []})
    
    versions = []
    for version_file in sorted(version_dir.glob("*.html")):
        versions.append({
            "name": version_file.stem,
            "created_at": version_file.stat().st_mtime,
            "size": version_file.stat().st_size
        })
    
    return jsonify({
        "success": True,
        "versions": versions
    })

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════╗
║   🚀 Claude SDK 페이지 생성 서버        ║
║   로컬 파일 시스템 기반 동작            ║
╚════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=5000, debug=True)