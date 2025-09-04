import React from 'react';
import { useGeneratorStore } from '../store/useGeneratorStore';
import { ConceptInput } from '../types';

const toneOptions = [
  { value: 'professional', label: '전문적인', icon: '👔' },
  { value: 'friendly', label: '친근한', icon: '😊' },
  { value: 'playful', label: '재미있는', icon: '🎉' },
  { value: 'serious', label: '진지한', icon: '🎯' },
  { value: 'luxurious', label: '고급스러운', icon: '💎' },
] as const;

const colorOptions = [
  { value: 'blue', label: '블루', color: 'bg-blue-500' },
  { value: 'green', label: '그린', color: 'bg-green-500' },
  { value: 'purple', label: '퍼플', color: 'bg-purple-500' },
  { value: 'red', label: '레드', color: 'bg-red-500' },
  { value: 'orange', label: '오렌지', color: 'bg-orange-500' },
] as const;

const templateOptions = [
  { value: 'insurance', label: '보험', icon: '🛡️', description: '신뢰감 있는 보험 서비스' },
  { value: 'petcare', label: '펫케어', icon: '🐾', description: '반려동물 관련 서비스' },
  { value: 'education', label: '교육', icon: '📚', description: '온라인 교육 플랫폼' },
  { value: 'healthcare', label: '헬스케어', icon: '🏥', description: '의료/건강 서비스' },
  { value: 'ecommerce', label: '이커머스', icon: '🛒', description: '온라인 쇼핑몰' },
  { value: 'custom', label: '직접 입력', icon: '✏️', description: '템플릿 없이 시작' },
] as const;

const sectionOptions = [
  { value: 'hero', label: '히어로', description: '메인 배너' },
  { value: 'features', label: '특징', description: '주요 기능' },
  { value: 'pricing', label: '가격', description: '요금제' },
  { value: 'testimonials', label: '후기', description: '고객 후기' },
  { value: 'faq', label: 'FAQ', description: '자주 묻는 질문' },
  { value: 'cta', label: 'CTA', description: '행동 유도' },
] as const;

export const ConceptForm: React.FC = () => {
  const { concept, updateConcept, generatePage, isGenerating } = useGeneratorStore();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    generatePage();
  };

  const handleTemplateSelect = (template: ConceptInput['template']) => {
    updateConcept({ template });
    
    // 템플릿별 기본값 설정
    if (template === 'insurance') {
      updateConcept({
        industry: '자동차보험',
        target: '시니어(60대 이상)',
        mainValue: '전화 한 통으로 간편하게 가입하는 다이렉트 보험',
        tone: 'professional',
        colorScheme: 'blue',
      });
    } else if (template === 'petcare') {
      updateConcept({
        industry: '반려동물 보험',
        target: '반려동물 보호자',
        mainValue: '우리 아이를 위한 든든한 의료보험',
        tone: 'friendly',
        colorScheme: 'purple',
      });
    }
  };

  const toggleSection = (section: string) => {
    const sections = concept.sections || [];
    if (sections.includes(section as any)) {
      updateConcept({
        sections: sections.filter((s) => s !== section),
      });
    } else {
      updateConcept({
        sections: [...sections, section as any],
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* 템플릿 선택 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          템플릿 선택 (선택사항)
        </label>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {templateOptions.map((template) => (
            <button
              key={template.value}
              type="button"
              onClick={() => handleTemplateSelect(template.value)}
              className={`p-4 rounded-lg border-2 transition-all ${
                concept.template === template.value
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="text-2xl mb-1">{template.icon}</div>
              <div className="font-medium">{template.label}</div>
              <div className="text-xs text-gray-500 mt-1">{template.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* 기본 정보 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            업종/서비스 <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={concept.industry || ''}
            onChange={(e) => updateConcept({ industry: e.target.value })}
            className="input-field"
            placeholder="예: 자동차보험, 온라인 교육"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            타겟 고객 <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={concept.target || ''}
            onChange={(e) => updateConcept({ target: e.target.value })}
            className="input-field"
            placeholder="예: 30-40대 직장인, 시니어"
            required
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          핵심 가치/메시지 <span className="text-red-500">*</span>
        </label>
        <textarea
          value={concept.mainValue || ''}
          onChange={(e) => updateConcept({ mainValue: e.target.value })}
          className="input-field"
          rows={3}
          placeholder="고객에게 전달하고 싶은 핵심 메시지를 입력하세요"
          required
        />
      </div>

      {/* 톤앤매너 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          톤앤매너
        </label>
        <div className="flex flex-wrap gap-2">
          {toneOptions.map((tone) => (
            <button
              key={tone.value}
              type="button"
              onClick={() => updateConcept({ tone: tone.value })}
              className={`px-4 py-2 rounded-lg border transition-all ${
                concept.tone === tone.value
                  ? 'border-primary-500 bg-primary-50 text-primary-700'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <span className="mr-2">{tone.icon}</span>
              {tone.label}
            </button>
          ))}
        </div>
      </div>

      {/* 색상 스킴 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          메인 컬러
        </label>
        <div className="flex flex-wrap gap-2">
          {colorOptions.map((color) => (
            <button
              key={color.value}
              type="button"
              onClick={() => updateConcept({ colorScheme: color.value })}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-all ${
                concept.colorScheme === color.value
                  ? 'border-gray-800 ring-2 ring-offset-2 ring-gray-400'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <div className={`w-4 h-4 rounded ${color.color}`} />
              {color.label}
            </button>
          ))}
        </div>
      </div>

      {/* 섹션 선택 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          포함할 섹션
        </label>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {sectionOptions.map((section) => (
            <label
              key={section.value}
              className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
            >
              <input
                type="checkbox"
                checked={concept.sections?.includes(section.value) || false}
                onChange={() => toggleSection(section.value)}
                className="mr-3 h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <div>
                <div className="font-medium">{section.label}</div>
                <div className="text-xs text-gray-500">{section.description}</div>
              </div>
            </label>
          ))}
        </div>
      </div>

      {/* 추가 요구사항 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          추가 요구사항 (선택사항)
        </label>
        <textarea
          value={concept.customRequirements || ''}
          onChange={(e) => updateConcept({ customRequirements: e.target.value })}
          className="input-field"
          rows={3}
          placeholder="특별히 강조하고 싶은 내용이나 추가 요구사항을 입력하세요"
        />
      </div>

      {/* 생성 버튼 */}
      <div className="flex justify-end gap-3">
        <button
          type="button"
          onClick={() => updateConcept({})}
          className="btn-secondary"
          disabled={isGenerating}
        >
          초기화
        </button>
        <button
          type="submit"
          className="btn-primary flex items-center gap-2"
          disabled={isGenerating}
        >
          {isGenerating ? (
            <>
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              생성 중...
            </>
          ) : (
            <>
              <span>✨</span>
              랜딩페이지 생성
            </>
          )}
        </button>
      </div>
    </form>
  );
};