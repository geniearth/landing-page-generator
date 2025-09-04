import { ConceptInput, GeneratedPage } from '../types';
import { claudeService } from './claude.service';
import { generateLandingPagePrompt, generateEditPrompt, quickEditHtml } from '../prompts/templates';
import * as fs from 'fs/promises';
import * as path from 'path';

export class GeneratorService {
  private generatedPages: Map<string, GeneratedPage> = new Map();

  async generateLandingPage(concept: ConceptInput): Promise<GeneratedPage> {
    try {
      // 프롬프트 생성
      const prompt = generateLandingPagePrompt(concept);
      
      // Claude API 호출
      console.log('Generating landing page with Claude...');
      const html = await claudeService.generateContent(prompt);
      
      // HTML 검증 및 정리
      const cleanedHtml = this.cleanHtml(html);
      
      // 메타데이터 생성
      const pageId = this.generatePageId();
      const generatedPage: GeneratedPage = {
        html: cleanedHtml,
        metadata: {
          title: `${concept.industry} - AI Generated Landing Page`,
          description: concept.mainValue,
          generatedAt: new Date().toISOString(),
          concept
        }
      };
      
      // 메모리에 저장 (실제로는 데이터베이스 사용)
      this.generatedPages.set(pageId, generatedPage);
      
      // 파일로도 저장 (백업용)
      await this.saveToFile(pageId, generatedPage);
      
      return generatedPage;
    } catch (error) {
      console.error('Error generating landing page:', error);
      throw new Error('Failed to generate landing page');
    }
  }

  async editLandingPage(
    pageId: string,
    editType: string,
    editDetails: any
  ): Promise<GeneratedPage> {
    const existingPage = this.generatedPages.get(pageId);
    
    if (!existingPage) {
      throw new Error('Page not found');
    }

    try {
      let updatedHtml: string;

      // 간단한 텍스트 수정은 직접 처리
      if (editType === 'quickText') {
        updatedHtml = quickEditHtml(
          existingPage.html,
          editDetails.selector,
          'text',
          editDetails.value
        );
      } else {
        // 복잡한 수정은 Claude API 사용
        const prompt = generateEditPrompt(existingPage.html, editType, editDetails);
        updatedHtml = await claudeService.generateContent(prompt);
      }

      // 업데이트된 페이지 저장
      const updatedPage: GeneratedPage = {
        ...existingPage,
        html: this.cleanHtml(updatedHtml),
        metadata: {
          ...existingPage.metadata,
          generatedAt: new Date().toISOString()
        }
      };

      this.generatedPages.set(pageId, updatedPage);
      await this.saveToFile(pageId, updatedPage);

      return updatedPage;
    } catch (error) {
      console.error('Error editing landing page:', error);
      throw new Error('Failed to edit landing page');
    }
  }

  async streamGenerateLandingPage(
    concept: ConceptInput,
    onChunk: (chunk: string) => void
  ): Promise<void> {
    try {
      const prompt = generateLandingPagePrompt(concept);
      
      let fullHtml = '';
      await claudeService.streamContent(prompt, (chunk) => {
        fullHtml += chunk;
        onChunk(chunk);
      });

      // 스트리밍 완료 후 저장
      const pageId = this.generatePageId();
      const generatedPage: GeneratedPage = {
        html: this.cleanHtml(fullHtml),
        metadata: {
          title: `${concept.industry} - AI Generated Landing Page`,
          description: concept.mainValue,
          generatedAt: new Date().toISOString(),
          concept
        }
      };

      this.generatedPages.set(pageId, generatedPage);
      await this.saveToFile(pageId, generatedPage);
    } catch (error) {
      console.error('Error in streaming generation:', error);
      throw error;
    }
  }

  getPage(pageId: string): GeneratedPage | undefined {
    return this.generatedPages.get(pageId);
  }

  listPages(): Array<{ id: string; metadata: GeneratedPage['metadata'] }> {
    const pages: Array<{ id: string; metadata: GeneratedPage['metadata'] }> = [];
    
    this.generatedPages.forEach((page, id) => {
      pages.push({ id, metadata: page.metadata });
    });

    return pages;
  }

  private cleanHtml(html: string): string {
    // HTML 코드 블록 제거 (```html ... ```)
    let cleaned = html.replace(/```html\n?/g, '').replace(/```\n?/g, '');
    
    // 앞뒤 공백 제거
    cleaned = cleaned.trim();
    
    // DOCTYPE이 없으면 추가
    if (!cleaned.toLowerCase().startsWith('<!doctype')) {
      cleaned = '<!DOCTYPE html>\n' + cleaned;
    }

    return cleaned;
  }

  private generatePageId(): string {
    return `page_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private async saveToFile(pageId: string, page: GeneratedPage): Promise<void> {
    try {
      const outputDir = path.join(process.cwd(), 'generated-pages');
      await fs.mkdir(outputDir, { recursive: true });
      
      const filePath = path.join(outputDir, `${pageId}.html`);
      await fs.writeFile(filePath, page.html, 'utf-8');
      
      const metadataPath = path.join(outputDir, `${pageId}.json`);
      await fs.writeFile(metadataPath, JSON.stringify(page.metadata, null, 2), 'utf-8');
      
      console.log(`Page saved to: ${filePath}`);
    } catch (error) {
      console.error('Error saving page to file:', error);
      // 파일 저장 실패는 치명적이지 않으므로 에러를 throw하지 않음
    }
  }
}

export const generatorService = new GeneratorService();