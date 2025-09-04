import axios from 'axios';
import { ConceptInput, GeneratedPage, EditRequest, ApiResponse } from '../types';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generatorApi = {
  // 랜딩페이지 생성
  generate: async (concept: ConceptInput): Promise<GeneratedPage> => {
    const response = await api.post<ApiResponse<GeneratedPage>>('/generate', concept);
    if (!response.data.success || !response.data.data) {
      throw new Error(response.data.error || 'Failed to generate page');
    }
    return response.data.data;
  },

  // 스트리밍 생성
  generateStream: (
    concept: ConceptInput,
    onChunk: (chunk: string) => void,
    onComplete: () => void,
    onError: (error: string) => void
  ) => {
    const eventSource = new EventSource('/api/generate/stream');
    
    // 데이터 전송을 위한 POST 요청
    api.post('/generate/stream', concept)
      .catch(error => {
        eventSource.close();
        onError(error.message);
      });

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.done) {
        eventSource.close();
        onComplete();
      } else if (data.error) {
        eventSource.close();
        onError(data.error);
      } else if (data.chunk) {
        onChunk(data.chunk);
      }
    };

    eventSource.onerror = () => {
      eventSource.close();
      onError('Connection lost');
    };

    return eventSource;
  },

  // 페이지 수정
  edit: async (
    pageId: string,
    editType: string,
    editDetails: any
  ): Promise<GeneratedPage> => {
    const response = await api.put<ApiResponse<GeneratedPage>>(
      `/edit/${pageId}`,
      { editType, editDetails }
    );
    if (!response.data.success || !response.data.data) {
      throw new Error(response.data.error || 'Failed to edit page');
    }
    return response.data.data;
  },

  // 빠른 편집
  quickEdit: async (editRequest: EditRequest): Promise<GeneratedPage> => {
    const response = await api.patch<ApiResponse<GeneratedPage>>(
      '/quick-edit',
      editRequest
    );
    if (!response.data.success || !response.data.data) {
      throw new Error(response.data.error || 'Failed to apply edits');
    }
    return response.data.data;
  },

  // 페이지 조회
  getPage: async (pageId: string): Promise<GeneratedPage> => {
    const response = await api.get<ApiResponse<GeneratedPage>>(`/page/${pageId}`);
    if (!response.data.success || !response.data.data) {
      throw new Error(response.data.error || 'Page not found');
    }
    return response.data.data;
  },

  // 페이지 목록
  listPages: async (): Promise<Array<{ id: string; metadata: GeneratedPage['metadata'] }>> => {
    const response = await api.get<ApiResponse<Array<{ id: string; metadata: GeneratedPage['metadata'] }>>>('/pages');
    return response.data.data || [];
  },
};