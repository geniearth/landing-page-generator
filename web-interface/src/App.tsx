import React, { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { ConceptForm } from './components/ConceptForm';
import { PreviewPane } from './components/PreviewPane';
import { LiveEditor } from './components/LiveEditor';
import { useGeneratorStore } from './store/useGeneratorStore';

function App() {
  const [activeTab, setActiveTab] = useState<'create' | 'edit'>('create');
  const [selectedElement, setSelectedElement] = useState<HTMLElement | null>(null);
  const { previewHtml } = useGeneratorStore();

  const handleElementClick = (element: HTMLElement) => {
    setSelectedElement(element);
    setActiveTab('edit');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <span className="text-2xl">🚀</span>
              <h1 className="text-xl font-bold text-gray-900">
                AI Landing Page Generator
              </h1>
              <span className="px-2 py-1 bg-primary-100 text-primary-700 text-xs rounded-full">
                Beta
              </span>
            </div>
            
            <nav className="flex items-center gap-4">
              <a 
                href="https://github.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                GitHub
              </a>
              <button className="text-gray-600 hover:text-gray-900 transition-colors">
                도움말
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Panel - Form/Editor */}
          <div className="lg:col-span-1">
            {/* Tab Navigation */}
            <div className="flex mb-4 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setActiveTab('create')}
                className={`flex-1 px-4 py-2 rounded-md transition-all ${
                  activeTab === 'create'
                    ? 'bg-white shadow-sm text-primary-600 font-medium'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <span className="mr-2">✨</span>
                생성
              </button>
              <button
                onClick={() => setActiveTab('edit')}
                className={`flex-1 px-4 py-2 rounded-md transition-all ${
                  activeTab === 'edit'
                    ? 'bg-white shadow-sm text-primary-600 font-medium'
                    : 'text-gray-600 hover:text-gray-900'
                } ${!previewHtml ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={!previewHtml}
              >
                <span className="mr-2">✏️</span>
                편집
              </button>
            </div>

            {/* Content */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              {activeTab === 'create' ? (
                <>
                  <div className="mb-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-2">
                      랜딩페이지 생성
                    </h2>
                    <p className="text-sm text-gray-600">
                      아래 정보를 입력하면 AI가 자동으로 랜딩페이지를 생성합니다
                    </p>
                  </div>
                  <ConceptForm />
                </>
              ) : (
                <>
                  <div className="mb-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-2">
                      실시간 편집
                    </h2>
                    <p className="text-sm text-gray-600">
                      미리보기에서 요소를 클릭하거나 아래 도구를 사용하세요
                    </p>
                  </div>
                  <LiveEditor />
                </>
              )}
            </div>
          </div>

          {/* Right Panel - Preview */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm h-[800px]">
              <PreviewPane 
                onElementClick={activeTab === 'edit' ? handleElementClick : undefined}
              />
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 border-t bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-gray-600 text-sm">
              © 2024 AI Landing Page Generator. Claude SDK를 활용한 프로젝트
            </div>
            <div className="flex gap-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">
                이용약관
              </a>
              <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">
                개인정보처리방침
              </a>
              <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">
                문의하기
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;