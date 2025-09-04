import { Router, Request, Response } from 'express';
import { ConceptInputSchema, EditRequestSchema } from '../types';
import { generatorService } from '../services/generator.service';

const router = Router();

// 랜딩페이지 생성
router.post('/generate', async (req: Request, res: Response) => {
  try {
    // 입력 검증
    const validation = ConceptInputSchema.safeParse(req.body);
    
    if (!validation.success) {
      return res.status(400).json({
        error: 'Invalid input',
        details: validation.error.errors
      });
    }

    // 페이지 생성
    const generatedPage = await generatorService.generateLandingPage(validation.data);
    
    res.json({
      success: true,
      data: generatedPage
    });
  } catch (error) {
    console.error('Generate endpoint error:', error);
    res.status(500).json({
      error: 'Failed to generate landing page',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// 스트리밍 생성 (SSE - Server-Sent Events)
router.post('/generate/stream', async (req: Request, res: Response) => {
  try {
    const validation = ConceptInputSchema.safeParse(req.body);
    
    if (!validation.success) {
      return res.status(400).json({
        error: 'Invalid input',
        details: validation.error.errors
      });
    }

    // SSE 헤더 설정
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });

    // 스트리밍 시작
    await generatorService.streamGenerateLandingPage(
      validation.data,
      (chunk) => {
        res.write(`data: ${JSON.stringify({ chunk })}\n\n`);
      }
    );

    // 완료 신호
    res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
    res.end();
  } catch (error) {
    console.error('Stream generate endpoint error:', error);
    res.write(`data: ${JSON.stringify({ error: 'Generation failed' })}\n\n`);
    res.end();
  }
});

// 페이지 수정
router.put('/edit/:pageId', async (req: Request, res: Response) => {
  try {
    const { pageId } = req.params;
    const { editType, editDetails } = req.body;

    if (!editType || !editDetails) {
      return res.status(400).json({
        error: 'editType and editDetails are required'
      });
    }

    const updatedPage = await generatorService.editLandingPage(
      pageId,
      editType,
      editDetails
    );

    res.json({
      success: true,
      data: updatedPage
    });
  } catch (error) {
    console.error('Edit endpoint error:', error);
    res.status(500).json({
      error: 'Failed to edit landing page',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// 빠른 텍스트 수정
router.patch('/quick-edit', async (req: Request, res: Response) => {
  try {
    const validation = EditRequestSchema.safeParse(req.body);
    
    if (!validation.success) {
      return res.status(400).json({
        error: 'Invalid input',
        details: validation.error.errors
      });
    }

    const { pageId, edits } = validation.data;

    // 각 편집 항목 적용
    let currentPage = generatorService.getPage(pageId);
    
    if (!currentPage) {
      return res.status(404).json({ error: 'Page not found' });
    }

    for (const edit of edits) {
      currentPage = await generatorService.editLandingPage(
        pageId,
        'quickText',
        edit
      );
    }

    res.json({
      success: true,
      data: currentPage
    });
  } catch (error) {
    console.error('Quick edit endpoint error:', error);
    res.status(500).json({
      error: 'Failed to apply edits',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// 페이지 조회
router.get('/page/:pageId', (req: Request, res: Response) => {
  const { pageId } = req.params;
  const page = generatorService.getPage(pageId);

  if (!page) {
    return res.status(404).json({ error: 'Page not found' });
  }

  res.json({
    success: true,
    data: page
  });
});

// 페이지 목록
router.get('/pages', (req: Request, res: Response) => {
  const pages = generatorService.listPages();
  
  res.json({
    success: true,
    data: pages
  });
});

export default router;