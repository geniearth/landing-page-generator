import { z } from 'zod';

// 컨셉 입력 스키마
export const ConceptInputSchema = z.object({
  industry: z.string().min(1, "업종을 입력해주세요"),
  target: z.string().min(1, "타겟 고객을 입력해주세요"),
  mainValue: z.string().min(1, "주요 가치를 입력해주세요"),
  tone: z.enum(['professional', 'friendly', 'playful', 'serious', 'luxurious']),
  colorScheme: z.enum(['blue', 'green', 'purple', 'red', 'orange', 'custom']).optional(),
  sections: z.array(z.enum(['hero', 'features', 'pricing', 'testimonials', 'faq', 'cta'])).optional(),
  customRequirements: z.string().optional(),
  template: z.enum(['insurance', 'petcare', 'education', 'healthcare', 'ecommerce', 'custom']).optional()
});

export type ConceptInput = z.infer<typeof ConceptInputSchema>;

// 생성된 페이지 응답
export interface GeneratedPage {
  html: string;
  metadata: {
    title: string;
    description: string;
    generatedAt: string;
    concept: ConceptInput;
  };
}

// 편집 요청
export const EditRequestSchema = z.object({
  pageId: z.string(),
  edits: z.array(z.object({
    selector: z.string(), // CSS selector
    property: z.string(), // text, style, attribute
    value: z.string()
  }))
});

export type EditRequest = z.infer<typeof EditRequestSchema>;