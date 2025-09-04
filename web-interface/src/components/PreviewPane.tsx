import React, { useRef, useEffect, useState } from 'react';
import { useGeneratorStore } from '../store/useGeneratorStore';

interface PreviewPaneProps {
  onElementClick?: (element: HTMLElement) => void;
}

export const PreviewPane: React.FC<PreviewPaneProps> = ({ onElementClick }) => {
  const { previewHtml, isGenerating } = useGeneratorStore();
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [scale, setScale] = useState(1);
  const [deviceView, setDeviceView] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');

  const deviceSizes = {
    desktop: { width: '100%', height: '100%' },
    tablet: { width: '768px', height: '1024px' },
    mobile: { width: '375px', height: '667px' },
  };

  useEffect(() => {
    if (!iframeRef.current || !previewHtml) return;

    const iframeDoc = iframeRef.current.contentDocument;
    if (!iframeDoc) return;

    // HTML 삽입
    iframeDoc.open();
    iframeDoc.write(previewHtml);
    iframeDoc.close();

    // 편집 모드일 때 클릭 이벤트 추가
    if (onElementClick) {
      const handleClick = (e: MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();
        
        const target = e.target as HTMLElement;
        if (target && target.tagName !== 'HTML' && target.tagName !== 'BODY') {
          // 하이라이트 효과
          target.style.outline = '2px solid #3b82f6';
          target.style.outlineOffset = '2px';
          
          setTimeout(() => {
            target.style.outline = '';
            target.style.outlineOffset = '';
          }, 2000);
          
          onElementClick(target);
        }
      };

      iframeDoc.addEventListener('click', handleClick);
      
      return () => {
        iframeDoc.removeEventListener('click', handleClick);
      };
    }
  }, [previewHtml, onElementClick]);

  const handleZoom = (direction: 'in' | 'out') => {
    setScale((prev) => {
      const newScale = direction === 'in' ? prev + 0.1 : prev - 0.1;
      return Math.max(0.5, Math.min(1.5, newScale));
    });
  };

  const handleDownload = () => {
    const blob = new Blob([previewHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'landing-page.html';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleNewTab = () => {
    const newWindow = window.open();
    if (newWindow) {
      newWindow.document.write(previewHtml);
      newWindow.document.close();
    }
  };

  if (!previewHtml && !isGenerating) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 rounded-lg">
        <div className="text-center">
          <div className="text-6xl mb-4">🎨</div>
          <h3 className="text-lg font-medium text-gray-900">미리보기 준비</h3>
          <p className="text-gray-500 mt-2">왼쪽 폼을 작성하고 생성 버튼을 클릭하세요</p>
        </div>
      </div>
    );
  }

  if (isGenerating) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 rounded-lg">
        <div className="text-center">
          <div className="relative">
            <div className="w-20 h-20 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-2xl">✨</span>
            </div>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mt-4">AI가 페이지를 생성중입니다</h3>
          <p className="text-gray-500 mt-2">잠시만 기다려주세요...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-gray-100 rounded-lg overflow-hidden">
      {/* 툴바 */}
      <div className="bg-white border-b px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          {/* 디바이스 뷰 선택 */}
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setDeviceView('desktop')}
              className={`px-3 py-1 rounded transition-colors ${
                deviceView === 'desktop'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="데스크톱"
            >
              💻
            </button>
            <button
              onClick={() => setDeviceView('tablet')}
              className={`px-3 py-1 rounded transition-colors ${
                deviceView === 'tablet'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="태블릿"
            >
              📱
            </button>
            <button
              onClick={() => setDeviceView('mobile')}
              className={`px-3 py-1 rounded transition-colors ${
                deviceView === 'mobile'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="모바일"
            >
              📲
            </button>
          </div>

          <div className="h-6 w-px bg-gray-300" />

          {/* 줌 컨트롤 */}
          <div className="flex items-center gap-1">
            <button
              onClick={() => handleZoom('out')}
              className="p-1 hover:bg-gray-100 rounded transition-colors"
              disabled={scale <= 0.5}
            >
              ➖
            </button>
            <span className="text-sm text-gray-600 min-w-[3rem] text-center">
              {Math.round(scale * 100)}%
            </span>
            <button
              onClick={() => handleZoom('in')}
              className="p-1 hover:bg-gray-100 rounded transition-colors"
              disabled={scale >= 1.5}
            >
              ➕
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleNewTab}
            className="px-3 py-1.5 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors flex items-center gap-2"
          >
            <span>🔗</span>
            새 탭
          </button>
          <button
            onClick={handleDownload}
            className="px-3 py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2"
          >
            <span>⬇️</span>
            다운로드
          </button>
        </div>
      </div>

      {/* 프리뷰 영역 */}
      <div className="flex-1 overflow-auto p-4">
        <div
          className="mx-auto transition-all duration-300 bg-white rounded-lg shadow-lg"
          style={{
            width: deviceView === 'desktop' ? '100%' : deviceSizes[deviceView].width,
            maxWidth: '100%',
          }}
        >
          <iframe
            ref={iframeRef}
            className="w-full border-0 rounded-lg"
            style={{
              height: deviceView === 'desktop' ? '800px' : deviceSizes[deviceView].height,
              transform: `scale(${scale})`,
              transformOrigin: 'top center',
            }}
            title="Landing Page Preview"
            sandbox="allow-same-origin allow-scripts"
          />
        </div>
      </div>
    </div>
  );
};