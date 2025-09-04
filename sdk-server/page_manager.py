#!/usr/bin/env python3
"""
페이지 관리 시스템
생성된 페이지의 관리, 버전 관리, 배포 등을 담당
"""

import os
import json
import time
import shutil
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import hashlib

class PageManager:
    """페이지 관리 시스템"""
    
    def __init__(self, pages_dir=None):
        self.base_dir = Path(__file__).parent.parent
        self.pages_dir = Path(pages_dir) if pages_dir else self.base_dir / "generated-pages"
        self.pages_dir.mkdir(exist_ok=True)
        
        # 배포 디렉토리
        self.deploy_dir = self.base_dir / "deployed-pages"
        self.deploy_dir.mkdir(exist_ok=True)
        
    def get_all_pages(self):
        """모든 페이지 정보 조회"""
        pages = []
        
        for page_dir in self.pages_dir.iterdir():
            if page_dir.is_dir():
                metadata_file = page_dir / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        
                    # 파일 크기 추가
                    html_file = page_dir / "index.html"
                    if html_file.exists():
                        metadata['file_size'] = html_file.stat().st_size
                        metadata['file_size_kb'] = round(metadata['file_size'] / 1024, 2)
                    
                    # 버전 수 추가
                    version_dir = page_dir / "versions"
                    if version_dir.exists():
                        metadata['version_count'] = len(list(version_dir.glob("*.html")))
                    else:
                        metadata['version_count'] = 1
                    
                    pages.append(metadata)
        
        # 최신순 정렬
        pages.sort(key=lambda x: x.get('created_at', 0), reverse=True)
        
        return pages
    
    def get_page_details(self, page_id):
        """특정 페이지 상세 정보"""
        page_dir = self.pages_dir / page_id
        
        if not page_dir.exists():
            return None
        
        # 메타데이터 로드
        metadata_file = page_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = {"id": page_id}
        
        # HTML 내용
        html_file = page_dir / "index.html"
        if html_file.exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            metadata['html'] = html_content
            metadata['file_size'] = len(html_content)
        
        # 버전 정보
        versions = self.get_page_versions(page_id)
        metadata['versions'] = versions
        
        return metadata
    
    def get_page_versions(self, page_id):
        """페이지 버전 목록"""
        version_dir = self.pages_dir / page_id / "versions"
        
        if not version_dir.exists():
            return []
        
        versions = []
        for version_file in sorted(version_dir.glob("*.html")):
            # 파일명에서 버전 정보 추출
            name_parts = version_file.stem.split('_')
            version_num = name_parts[0] if name_parts else 'v1'
            timestamp = name_parts[1] if len(name_parts) > 1 else ''
            
            versions.append({
                'version': version_num,
                'filename': version_file.name,
                'created_at': version_file.stat().st_mtime,
                'created_at_str': datetime.fromtimestamp(
                    version_file.stat().st_mtime
                ).strftime('%Y-%m-%d %H:%M:%S'),
                'size': version_file.stat().st_size,
                'size_kb': round(version_file.stat().st_size / 1024, 2)
            })
        
        return versions
    
    def restore_version(self, page_id, version_filename):
        """특정 버전으로 복원"""
        page_dir = self.pages_dir / page_id
        version_file = page_dir / "versions" / version_filename
        current_file = page_dir / "index.html"
        
        if not version_file.exists():
            return False
        
        # 현재 버전을 백업
        if current_file.exists():
            version_dir = page_dir / "versions"
            version_dir.mkdir(exist_ok=True)
            
            # 백업 파일명 생성
            backup_name = f"backup_{int(time.time())}.html"
            backup_file = version_dir / backup_name
            
            shutil.copy2(current_file, backup_file)
        
        # 선택한 버전으로 복원
        shutil.copy2(version_file, current_file)
        
        # 메타데이터 업데이트
        metadata_file = page_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            metadata['last_restored'] = {
                'version': version_filename,
                'restored_at': time.time(),
                'restored_at_str': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return True
    
    def delete_page(self, page_id):
        """페이지 삭제"""
        page_dir = self.pages_dir / page_id
        
        if page_dir.exists():
            # 삭제 전 백업 (trash 폴더로 이동)
            trash_dir = self.base_dir / "trash"
            trash_dir.mkdir(exist_ok=True)
            
            trash_page_dir = trash_dir / f"{page_id}_{int(time.time())}"
            shutil.move(str(page_dir), str(trash_page_dir))
            
            return True
        
        return False
    
    def duplicate_page(self, page_id):
        """페이지 복제"""
        source_dir = self.pages_dir / page_id
        
        if not source_dir.exists():
            return None
        
        # 새 ID 생성
        new_id = f"{page_id}_copy_{int(time.time())}"
        dest_dir = self.pages_dir / new_id
        
        # 디렉토리 복사
        shutil.copytree(source_dir, dest_dir)
        
        # 메타데이터 업데이트
        metadata_file = dest_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            metadata['id'] = new_id
            metadata['original_id'] = page_id
            metadata['created_at'] = time.time()
            metadata['created_at_str'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            metadata['is_copy'] = True
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return new_id
    
    def deploy_page(self, page_id, deploy_name=None):
        """페이지를 배포 디렉토리로 복사"""
        source_file = self.pages_dir / page_id / "index.html"
        
        if not source_file.exists():
            return None
        
        # 배포 이름 설정
        if not deploy_name:
            deploy_name = page_id
        
        # 안전한 파일명으로 변환
        safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in deploy_name)
        deploy_file = self.deploy_dir / f"{safe_name}.html"
        
        # 파일 복사
        shutil.copy2(source_file, deploy_file)
        
        # 배포 정보 저장
        deploy_info = {
            'page_id': page_id,
            'deploy_name': safe_name,
            'deployed_at': time.time(),
            'deployed_at_str': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_path': str(deploy_file),
            'url': f"http://localhost:8080/{safe_name}.html"
        }
        
        deploy_info_file = self.deploy_dir / f"{safe_name}.json"
        with open(deploy_info_file, 'w', encoding='utf-8') as f:
            json.dump(deploy_info, f, indent=2, ensure_ascii=False)
        
        return deploy_info
    
    def analyze_page(self, page_id):
        """페이지 분석 (SEO, 성능 등)"""
        html_file = self.pages_dir / page_id / "index.html"
        
        if not html_file.exists():
            return None
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        analysis = {
            'seo': {
                'has_title': bool(soup.find('title')),
                'title': soup.find('title').text if soup.find('title') else None,
                'has_meta_description': bool(soup.find('meta', {'name': 'description'})),
                'meta_description': soup.find('meta', {'name': 'description'})['content'] 
                    if soup.find('meta', {'name': 'description'}) else None,
                'h1_count': len(soup.find_all('h1')),
                'h2_count': len(soup.find_all('h2')),
                'img_without_alt': len(soup.find_all('img', alt=False))
            },
            'structure': {
                'total_elements': len(soup.find_all()),
                'div_count': len(soup.find_all('div')),
                'section_count': len(soup.find_all('section')),
                'script_count': len(soup.find_all('script')),
                'style_count': len(soup.find_all('style')),
                'link_count': len(soup.find_all('a')),
                'form_count': len(soup.find_all('form'))
            },
            'performance': {
                'file_size': len(html_content),
                'file_size_kb': round(len(html_content) / 1024, 2),
                'inline_css_size': sum(len(style.text) for style in soup.find_all('style')),
                'inline_js_size': sum(len(script.text) for script in soup.find_all('script'))
            }
        }
        
        return analysis
    
    def search_pages(self, query):
        """페이지 검색"""
        results = []
        query_lower = query.lower()
        
        for page_dir in self.pages_dir.iterdir():
            if page_dir.is_dir():
                # 메타데이터에서 검색
                metadata_file = page_dir / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    # 컨셉 정보에서 검색
                    concept = metadata.get('concept', {})
                    if (query_lower in concept.get('industry', '').lower() or
                        query_lower in concept.get('target', '').lower() or
                        query_lower in concept.get('mainValue', '').lower()):
                        
                        results.append({
                            'id': metadata['id'],
                            'industry': concept.get('industry', ''),
                            'target': concept.get('target', ''),
                            'created_at': metadata.get('created_at_str', '')
                        })
                        continue
                
                # HTML 내용에서 검색
                html_file = page_dir / "index.html"
                if html_file.exists():
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    if query_lower in html_content.lower():
                        # 메타데이터 로드
                        if metadata_file.exists():
                            with open(metadata_file, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)
                            
                            results.append({
                                'id': metadata['id'],
                                'industry': metadata.get('concept', {}).get('industry', ''),
                                'target': metadata.get('concept', {}).get('target', ''),
                                'created_at': metadata.get('created_at_str', '')
                            })
        
        return results

# CLI 테스트용
if __name__ == "__main__":
    manager = PageManager()
    
    print("📦 페이지 관리 시스템")
    print("-" * 40)
    
    # 모든 페이지 목록
    pages = manager.get_all_pages()
    print(f"총 {len(pages)}개의 페이지")
    
    for page in pages[:5]:  # 최근 5개만
        print(f"  - {page['id']}: {page.get('concept', {}).get('industry', 'Unknown')}")
    
    # 첫 번째 페이지 분석
    if pages:
        first_page = pages[0]
        analysis = manager.analyze_page(first_page['id'])
        if analysis:
            print(f"\n페이지 분석: {first_page['id']}")
            print(f"  - 파일 크기: {analysis['performance']['file_size_kb']} KB")
            print(f"  - SEO 타이틀: {analysis['seo']['has_title']}")
            print(f"  - H1 태그: {analysis['seo']['h1_count']}개")