#!/usr/bin/env node
/**
 * 정적 파일 서버
 * 생성된 랜딩페이지를 정적으로 서빙
 */

const express = require('express');
const path = require('path');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = process.env.STATIC_PORT || 8080;

// CORS 설정
app.use(cors());

// 기본 경로 설정
const BASE_DIR = path.join(__dirname, '..');
const PAGES_DIR = path.join(BASE_DIR, 'generated-pages');
const DEPLOYED_DIR = path.join(BASE_DIR, 'deployed-pages');

// 디렉토리 생성
if (!fs.existsSync(PAGES_DIR)) {
  fs.mkdirSync(PAGES_DIR, { recursive: true });
}
if (!fs.existsSync(DEPLOYED_DIR)) {
  fs.mkdirSync(DEPLOYED_DIR, { recursive: true });
}

// 정적 파일 서빙 (generated-pages)
app.use('/pages', express.static(PAGES_DIR, {
  extensions: ['html'],
  index: 'index.html',
  setHeaders: (res, path) => {
    res.set('X-Content-Type-Options', 'nosniff');
    if (path.endsWith('.html')) {
      res.set('Content-Type', 'text/html; charset=UTF-8');
    }
  }
}));

// 정적 파일 서빙 (deployed-pages)
app.use('/deployed', express.static(DEPLOYED_DIR, {
  extensions: ['html'],
  setHeaders: (res, path) => {
    res.set('X-Content-Type-Options', 'nosniff');
    if (path.endsWith('.html')) {
      res.set('Content-Type', 'text/html; charset=UTF-8');
    }
  }
}));

// 페이지별 직접 접근
app.get('/view/:pageId', (req, res) => {
  const pageId = req.params.pageId;
  const htmlPath = path.join(PAGES_DIR, pageId, 'index.html');
  
  if (fs.existsSync(htmlPath)) {
    res.sendFile(htmlPath);
  } else {
    res.status(404).send(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>페이지를 찾을 수 없습니다</title>
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
          }
          .error-container {
            text-align: center;
            padding: 2rem;
          }
          h1 { font-size: 3rem; margin-bottom: 1rem; }
          p { font-size: 1.2rem; opacity: 0.9; }
          a {
            display: inline-block;
            margin-top: 2rem;
            padding: 0.8rem 2rem;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: transform 0.3s;
          }
          a:hover { transform: translateY(-2px); }
        </style>
      </head>
      <body>
        <div class="error-container">
          <h1>404</h1>
          <p>페이지를 찾을 수 없습니다: ${pageId}</p>
          <a href="/">홈으로 돌아가기</a>
        </div>
      </body>
      </html>
    `);
  }
});

// 페이지 목록 API
app.get('/api/list', (req, res) => {
  const pages = [];
  
  // generated-pages 스캔
  if (fs.existsSync(PAGES_DIR)) {
    const dirs = fs.readdirSync(PAGES_DIR);
    
    dirs.forEach(dir => {
      const dirPath = path.join(PAGES_DIR, dir);
      const htmlPath = path.join(dirPath, 'index.html');
      const metadataPath = path.join(dirPath, 'metadata.json');
      
      if (fs.existsSync(htmlPath)) {
        const stat = fs.statSync(htmlPath);
        let metadata = {};
        
        if (fs.existsSync(metadataPath)) {
          try {
            metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
          } catch (e) {
            console.error(`Failed to parse metadata for ${dir}:`, e);
          }
        }
        
        pages.push({
          id: dir,
          path: `/view/${dir}`,
          size: stat.size,
          created: stat.birthtime,
          modified: stat.mtime,
          ...metadata
        });
      }
    });
  }
  
  // 최신순 정렬
  pages.sort((a, b) => new Date(b.created) - new Date(a.created));
  
  res.json({ pages, total: pages.length });
});

// 홈페이지 - 페이지 목록
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>생성된 랜딩페이지 목록</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
          padding: 2rem;
        }
        .container {
          max-width: 1200px;
          margin: 0 auto;
        }
        h1 {
          color: white;
          text-align: center;
          margin-bottom: 2rem;
          font-size: 2.5rem;
        }
        .pages-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 1.5rem;
        }
        .page-card {
          background: white;
          border-radius: 15px;
          padding: 1.5rem;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
          transition: transform 0.3s, box-shadow 0.3s;
          cursor: pointer;
        }
        .page-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }
        .page-title {
          font-size: 1.3rem;
          color: #333;
          margin-bottom: 0.5rem;
        }
        .page-meta {
          color: #666;
          font-size: 0.9rem;
          margin-bottom: 1rem;
        }
        .page-link {
          display: inline-block;
          padding: 0.5rem 1rem;
          background: linear-gradient(135deg, #667eea, #764ba2);
          color: white;
          text-decoration: none;
          border-radius: 25px;
          font-weight: bold;
          transition: opacity 0.3s;
        }
        .page-link:hover {
          opacity: 0.9;
        }
        .empty-state {
          text-align: center;
          color: white;
          padding: 4rem;
        }
        .loading {
          text-align: center;
          color: white;
          font-size: 1.5rem;
          padding: 2rem;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🚀 생성된 랜딩페이지</h1>
        <div id="loading" class="loading">페이지 목록을 불러오는 중...</div>
        <div id="pages-grid" class="pages-grid" style="display: none;"></div>
        <div id="empty-state" class="empty-state" style="display: none;">
          <h2>아직 생성된 페이지가 없습니다</h2>
          <p>웹 인터페이스에서 새 페이지를 생성해보세요!</p>
        </div>
      </div>

      <script>
        async function loadPages() {
          try {
            const response = await fetch('/api/list');
            const data = await response.json();
            
            const loading = document.getElementById('loading');
            const grid = document.getElementById('pages-grid');
            const emptyState = document.getElementById('empty-state');
            
            loading.style.display = 'none';
            
            if (data.pages && data.pages.length > 0) {
              grid.innerHTML = data.pages.map(page => \`
                <div class="page-card" onclick="window.open('\${page.path}', '_blank')">
                  <div class="page-title">\${page.id}</div>
                  <div class="page-meta">
                    \${page.concept ? \`
                      <div>업종: \${page.concept.industry || 'Unknown'}</div>
                      <div>타겟: \${page.concept.target || 'Unknown'}</div>
                    \` : ''}
                    <div>생성일: \${new Date(page.created).toLocaleDateString('ko-KR')}</div>
                    <div>크기: \${(page.size / 1024).toFixed(2)} KB</div>
                  </div>
                  <a href="\${page.path}" class="page-link" onclick="event.stopPropagation()">
                    페이지 보기 →
                  </a>
                </div>
              \`).join('');
              
              grid.style.display = 'grid';
            } else {
              emptyState.style.display = 'block';
            }
          } catch (error) {
            console.error('Failed to load pages:', error);
            document.getElementById('loading').innerHTML = 
              '페이지 목록을 불러올 수 없습니다. 서버 상태를 확인해주세요.';
          }
        }

        // 페이지 로드 시 실행
        loadPages();
        
        // 30초마다 자동 새로고침
        setInterval(loadPages, 30000);
      </script>
    </body>
    </html>
  `);
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════╗
║   📁 정적 파일 서버 실행 중                 ║
║   생성된 페이지를 서빙합니다                ║
╚════════════════════════════════════════════╝

🌐 서버 주소: http://localhost:${PORT}
📂 페이지 디렉토리: ${PAGES_DIR}
📋 페이지 목록: http://localhost:${PORT}/

페이지 접근 방법:
- 목록: http://localhost:${PORT}
- 개별 페이지: http://localhost:${PORT}/view/[page_id]
- API: http://localhost:${PORT}/api/list
  `);
});