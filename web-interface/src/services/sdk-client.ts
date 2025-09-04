/**
 * SDK 서버 클라이언트
 * Python Flask SDK 서버와 통신
 */

import { ConceptInput, GeneratedPage } from '../types';

const SDK_SERVER_URL = 'http://localhost:5001';  // 포트 변경 (5000은 사용 중)

export interface PageInfo {
  id: string;
  industry: string;
  target: string;
  created_at: string;
  path: string;
  file_size_kb?: number;
  version_count?: number;
}

export interface GenerateResponse {
  success: boolean;
  page_id?: string;
  path?: string;
  file_path?: string;
  error?: string;
}

export interface PageAnalysis {
  seo: {
    has_title: boolean;
    title: string | null;
    has_meta_description: boolean;
    meta_description: string | null;
    h1_count: number;
    h2_count: number;
    img_without_alt: number;
  };
  structure: {
    total_elements: number;
    div_count: number;
    section_count: number;
    script_count: number;
    style_count: number;
    link_count: number;
    form_count: number;
  };
  performance: {
    file_size: number;
    file_size_kb: number;
    inline_css_size: number;
    inline_js_size: number;
  };
}

class SDKClient {
  private baseUrl: string;

  constructor(baseUrl: string = SDK_SERVER_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * 헬스 체크
   */
  async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      const data = await response.json();
      return data.status === 'ok';
    } catch (error) {
      console.error('SDK Server health check failed:', error);
      return false;
    }
  }

  /**
   * 랜딩페이지 생성
   */
  async generatePage(concept: ConceptInput): Promise<GenerateResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(concept),
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Page generation failed:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  /**
   * 페이지 목록 조회
   */
  async listPages(): Promise<PageInfo[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/pages`);
      const data = await response.json();
      
      if (data.success) {
        return data.pages || [];
      }
      
      return [];
    } catch (error) {
      console.error('Failed to list pages:', error);
      return [];
    }
  }

  /**
   * 특정 페이지 조회
   */
  async getPage(pageId: string): Promise<GeneratedPage | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/pages/${pageId}`);
      const data = await response.json();
      
      if (data.success && data.data) {
        return data.data;
      }
      
      return null;
    } catch (error) {
      console.error('Failed to get page:', error);
      return null;
    }
  }

  /**
   * 페이지 HTML 직접 조회
   */
  async getPageHtml(pageId: string): Promise<string | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/pages/${pageId}/html`);
      
      if (response.ok) {
        return await response.text();
      }
      
      return null;
    } catch (error) {
      console.error('Failed to get page HTML:', error);
      return null;
    }
  }

  /**
   * 페이지 편집
   */
  async editPage(pageId: string, edits: Array<{
    selector: string;
    property?: string;
    value: string;
  }>): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/pages/${pageId}/edit`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ edits }),
      });

      const data = await response.json();
      return data.success === true;
    } catch (error) {
      console.error('Failed to edit page:', error);
      return false;
    }
  }

  /**
   * 페이지 버전 목록
   */
  async getPageVersions(pageId: string): Promise<any[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/pages/${pageId}/versions`);
      const data = await response.json();
      
      if (data.success) {
        return data.versions || [];
      }
      
      return [];
    } catch (error) {
      console.error('Failed to get page versions:', error);
      return [];
    }
  }

  /**
   * 페이지 미리보기 URL 생성
   */
  getPreviewUrl(pageId: string): string {
    return `${this.baseUrl}/api/pages/${pageId}/html`;
  }

  /**
   * 파일 다운로드 URL 생성
   */
  getDownloadUrl(pageId: string): string {
    return `${this.baseUrl}/api/pages/${pageId}/html`;
  }
}

// 싱글톤 인스턴스
export const sdkClient = new SDKClient();

// 스토리지 헬퍼 함수들
export const storage = {
  /**
   * 최근 생성된 페이지 ID 저장
   */
  saveRecentPageId(pageId: string) {
    localStorage.setItem('recent_page_id', pageId);
    
    // 최근 페이지 목록 업데이트
    const recentPages = this.getRecentPageIds();
    if (!recentPages.includes(pageId)) {
      recentPages.unshift(pageId);
      // 최대 10개까지만 저장
      if (recentPages.length > 10) {
        recentPages.pop();
      }
      localStorage.setItem('recent_page_ids', JSON.stringify(recentPages));
    }
  },

  /**
   * 최근 페이지 ID 조회
   */
  getRecentPageId(): string | null {
    return localStorage.getItem('recent_page_id');
  },

  /**
   * 최근 페이지 ID 목록 조회
   */
  getRecentPageIds(): string[] {
    const stored = localStorage.getItem('recent_page_ids');
    return stored ? JSON.parse(stored) : [];
  },

  /**
   * 마지막 사용한 컨셉 저장
   */
  saveLastConcept(concept: ConceptInput) {
    localStorage.setItem('last_concept', JSON.stringify(concept));
  },

  /**
   * 마지막 사용한 컨셉 조회
   */
  getLastConcept(): ConceptInput | null {
    const stored = localStorage.getItem('last_concept');
    return stored ? JSON.parse(stored) : null;
  },
};