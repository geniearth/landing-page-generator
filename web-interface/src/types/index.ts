export interface ConceptInput {
  industry: string;
  target: string;
  mainValue: string;
  tone: 'professional' | 'friendly' | 'playful' | 'serious' | 'luxurious';
  colorScheme?: 'blue' | 'green' | 'purple' | 'red' | 'orange' | 'custom';
  sections?: ('hero' | 'features' | 'pricing' | 'testimonials' | 'faq' | 'cta')[];
  customRequirements?: string;
  template?: 'insurance' | 'petcare' | 'education' | 'healthcare' | 'ecommerce' | 'custom';
}

export interface GeneratedPage {
  html: string;
  metadata: {
    title: string;
    description: string;
    generatedAt: string;
    concept: ConceptInput;
  };
}

export interface EditRequest {
  pageId: string;
  edits: {
    selector: string;
    property: string;
    value: string;
  }[];
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  details?: any;
}