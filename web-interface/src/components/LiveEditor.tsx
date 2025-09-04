import React, { useState, useEffect } from 'react';
import { useGeneratorStore } from '../store/useGeneratorStore';
import toast from 'react-hot-toast';

interface EditableElement {
  selector: string;
  text: string;
  tagName: string;
}

export const LiveEditor: React.FC = () => {
  const { previewHtml, quickEditText, isEditing } = useGeneratorStore();
  const [selectedElement, setSelectedElement] = useState<EditableElement | null>(null);
  const [editText, setEditText] = useState('');
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  useEffect(() => {
    if (selectedElement) {
      setEditText(selectedElement.text);
      setIsEditModalOpen(true);
    }
  }, [selectedElement]);

  const handleElementSelect = (element: HTMLElement) => {
    // CSS selector 생성 (간단한 버전)
    let selector = element.tagName.toLowerCase();
    if (element.id) {
      selector = `#${element.id}`;
    } else if (element.className) {
      selector = `${selector}.${element.className.split(' ').join('.')}`;
    }

    setSelectedElement({
      selector,
      text: element.textContent || '',
      tagName: element.tagName,
    });
  };

  const handleSaveEdit = async () => {
    if (!selectedElement) return;

    try {
      await quickEditText(selectedElement.selector, editText);
      toast.success('텍스트가 수정되었습니다');
      setIsEditModalOpen(false);
      setSelectedElement(null);
    } catch (error) {
      toast.error('수정에 실패했습니다');
    }
  };

  const quickActions = [
    {
      label: '헤드라인 수정',
      icon: '📝',
      selector: 'h1',
      action: () => {
        const newText = prompt('새 헤드라인을 입력하세요:');
        if (newText) {
          quickEditText('h1', newText);
        }
      },
    },
    {
      label: '버튼 텍스트',
      icon: '🔘',
      selector: 'button',
      action: () => {
        const newText = prompt('새 버튼 텍스트를 입력하세요:');
        if (newText) {
          quickEditText('button', newText);
        }
      },
    },
    {
      label: '색상 변경',
      icon: '🎨',
      action: () => {
        toast('색상 팔레트 기능은 준비 중입니다', { icon: '🚧' });
      },
    },
  ];

  if (!previewHtml) {
    return null;
  }

  return (
    <>
      {/* 편집 툴바 */}
      <div className="bg-white border rounded-lg p-4 mb-4">
        <h3 className="font-medium text-gray-900 mb-3">빠른 편집</h3>
        <div className="space-y-2">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={action.action}
              className="w-full text-left px-3 py-2 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors flex items-center gap-2"
              disabled={isEditing}
            >
              <span>{action.icon}</span>
              <span className="text-sm">{action.label}</span>
            </button>
          ))}
        </div>

        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            💡 미리보기에서 텍스트를 클릭하면 직접 편집할 수 있습니다
          </p>
        </div>
      </div>

      {/* 편집 모달 */}
      {isEditModalOpen && selectedElement && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-medium mb-4">텍스트 편집</h3>
            
            <div className="mb-4">
              <label className="block text-sm text-gray-600 mb-1">
                선택된 요소: <code className="bg-gray-100 px-1 rounded">{selectedElement.selector}</code>
              </label>
              <textarea
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                rows={4}
                autoFocus
              />
            </div>

            <div className="flex justify-end gap-2">
              <button
                onClick={() => {
                  setIsEditModalOpen(false);
                  setSelectedElement(null);
                }}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                취소
              </button>
              <button
                onClick={handleSaveEdit}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                disabled={isEditing}
              >
                {isEditing ? '저장 중...' : '저장'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};