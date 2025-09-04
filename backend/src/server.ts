import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import generatorRoutes from './routes/generator.routes';

// 환경 변수 로드
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// 미들웨어
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true
}));

app.use(express.json({ limit: '10mb' })); // HTML이 클 수 있으므로 limit 증가
app.use(express.urlencoded({ extended: true }));

// 헬스 체크
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    apiKey: process.env.ANTHROPIC_API_KEY ? 'configured' : 'missing'
  });
});

// API 라우트
app.use('/api', generatorRoutes);

// 정적 파일 서빙 (생성된 페이지 미리보기용)
app.use('/preview', express.static('generated-pages'));

// 에러 핸들러
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Server error:', err);
  res.status(err.status || 500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`
🚀 Landing Page Generator Backend Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Server running on: http://localhost:${PORT}
🔑 API Key Status: ${process.env.ANTHROPIC_API_KEY ? '✅ Configured' : '❌ Missing'}
🌍 Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:5173'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Available Endpoints:
- GET  /health              - Health check
- POST /api/generate        - Generate landing page
- POST /api/generate/stream - Stream generation (SSE)
- PUT  /api/edit/:pageId    - Edit existing page
- PATCH /api/quick-edit     - Quick text edits
- GET  /api/page/:pageId    - Get specific page
- GET  /api/pages           - List all pages
- GET  /preview/:pageId.html - Preview generated page
  `);
});

export default app;