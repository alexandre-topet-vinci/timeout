import { Controller, Post, Body, Get } from '@nestjs/common';
import { AiService } from './ai.service';

interface AskQuestionDto {
  question: string;
}

@Controller('api/ai')
export class AiController {
  constructor(private readonly aiService: AiService) {}

  @Post('ask')
  async askQuestion(@Body() body: AskQuestionDto) {
    return this.aiService.askQuestion(body.question);
  }

  @Get('stats')
  async getStats() {
    return this.aiService.getStats();
  }
}
