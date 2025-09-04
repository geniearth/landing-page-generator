import { create } from 'zustand';
import { ConceptInput, GeneratedPage } from '../types';
import { sdkClient, storage, PageInfo } from '../services/sdk-client';
import toast from 'react-hot-toast';

interface GeneratorState {
  // 상태
  concept: Partial<ConceptInput>;
  currentPage: GeneratedPage | null;
  pageId: string | null;
  isGenerating: boolean;
  isEditing: boolean;
  pagesList: PageInfo[];
  previewHtml: string;
  isConnected: boolean;
  
  // 액션 - 컨셉 관리
  updateConcept: (concept: Partial<ConceptInput>) => void;
  resetConcept: () => void;
  
  // 액션 - 페이지 생성
  generatePage: () => Promise<void>;
  
  // 액션 - 페이지 편집
  quickEditText: (selector: string, newText: string) => Promise<void>;
  
  // 액션 - 페이지 관리
  loadPage: (pageId: string) => Promise<void>;
  loadPagesList: () => Promise<void>;
  setPreviewHtml: (html: string) => void;
  
  // SDK 연결 체크
  checkConnection: () => Promise<void>;
}

const initialConcept: Partial<ConceptInput> = {
  tone: 'professional',
  colorScheme: 'blue',
  sections: ['hero', 'features', 'testimonials', 'pricing', 'faq', 'cta'],
};

export const useGeneratorStore = create<GeneratorState>((set, get) => ({
  // 초기 상태
  concept: storage.getLastConcept() || initialConcept,
  currentPage: null,
  pageId: storage.getRecentPageId(),
  isGenerating: false,
  isEditing: false,
  pagesList: [],
  previewHtml: '',
  isConnected: false,

  // SDK 연결 체크
  checkConnection: async () => {
    const isHealthy = await sdkClient.checkHealth();
    set({ isConnected: isHealthy });
    
    if (!isHealthy) {
      toast.error('SDK 서버에 연결할 수 없습니다. Python 서버를 실행해주세요.');
    }
  },

  // 컨셉 관리
  updateConcept: (concept) => {
    set((state) => {
      const newConcept = { ...state.concept, ...concept };
      storage.saveLastConcept(newConcept as ConceptInput);
      return { concept: newConcept };
    });
  },

  resetConcept: () => {
    set({ concept: initialConcept });
    storage.saveLastConcept(initialConcept as ConceptInput);
  },

  // 페이지 생성
  generatePage: async () => {
    const { concept } = get();
    
    // 검증
    if (!concept.industry || !concept.target || !concept.mainValue) {
      toast.error('필수 정보를 모두 입력해주세요');
      return;
    }

    set({ isGenerating: true, previewHtml: '' });

    try {
      // SDK 서버로 생성 요청
      const response = await sdkClient.generatePage(concept as ConceptInput);
      
      if (response.success && response.page_id) {
        // 생성된 페이지 HTML 로드
        const html = await sdkClient.getPageHtml(response.page_id);
        
        if (html) {
          const page: GeneratedPage = {
            html,
            metadata: {
              title: `${concept.industry} - AI Generated`,
              description: concept.mainValue || '',
              generatedAt: new Date().toISOString(),
              concept: concept as ConceptInput,
            },
          };
          
          set({
            currentPage: page,
            pageId: response.page_id,
            previewHtml: html,
            isGenerating: false,
          });
          
          // 로컬 스토리지에 저장
          storage.saveRecentPageId(response.page_id);
          
          toast.success('랜딩페이지가 생성되었습니다!');
          
          // 페이지 목록 갱신
          get().loadPagesList();
        }
      } else {
        throw new Error(response.error || '페이지 생성 실패');
      }
    } catch (error) {
      console.error('Generate error:', error);
      toast.error(error instanceof Error ? error.message : '페이지 생성에 실패했습니다');
      set({ isGenerating: false });
    }
  },

  // 빠른 텍스트 수정
  quickEditText: async (selector, newText) => {
    const { pageId } = get();
    
    if (!pageId) {
      toast.error('편집할 페이지가 없습니다');
      return;
    }

    set({ isEditing: true });

    try {
      const success = await sdkClient.editPage(pageId, [
        {
          selector,
          property: 'text',
          value: newText,
        },
      ]);

      if (success) {
        // 수정된 페이지 다시 로드
        const html = await sdkClient.getPageHtml(pageId);
        if (html) {
          set((state) => ({
            previewHtml: html,
            currentPage: state.currentPage ? {
              ...state.currentPage,
              html,
            } : null,
            isEditing: false,
          }));
          
          toast.success('텍스트가 수정되었습니다');
        }
      } else {
        throw new Error('편집 실패');
      }
    } catch (error) {
      console.error('Quick edit error:', error);
      toast.error('텍스트 수정에 실패했습니다');
      set({ isEditing: false });
    }
  },

  // 페이지 로드
  loadPage: async (pageId) => {
    try {
      const page = await sdkClient.getPage(pageId);
      
      if (page) {
        set({
          currentPage: page,
          pageId,
          previewHtml: page.html || '',
        });
        
        storage.saveRecentPageId(pageId);
        toast.success('페이지를 불러왔습니다');
      } else {
        toast.error('페이지를 찾을 수 없습니다');
      }
    } catch (error) {
      console.error('Load page error:', error);
      toast.error('페이지 로드에 실패했습니다');
    }
  },

  // 페이지 목록 로드
  loadPagesList: async () => {
    try {
      const pages = await sdkClient.listPages();
      set({ pagesList: pages });
    } catch (error) {
      console.error('Load pages list error:', error);
      toast.error('페이지 목록을 불러올 수 없습니다');
    }
  },

  // 프리뷰 HTML 설정
  setPreviewHtml: (html) => set({ previewHtml: html }),
}));