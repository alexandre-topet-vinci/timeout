import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class AiService {
  private readonly pythonApiUrl: string;

  constructor(private readonly httpService: HttpService) {
    this.pythonApiUrl = process.env.PYTHON_API_URL || 'http://python-api:8000';
  }

  async askQuestion(question: string) {
    try {
      const response = await firstValueFrom(
        this.httpService.post(`${this.pythonApiUrl}/api/ask`, { question }),
      );
      return response.data;
    } catch (error) {
      throw new HttpException(
        'Erreur lors de la communication avec le modèle IA',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getStats() {
    try {
      const response = await firstValueFrom(
        this.httpService.get(`${this.pythonApiUrl}/api/stats`),
      );
      return response.data;
    } catch (error) {
      throw new HttpException(
        'Erreur lors de la récupération des statistiques',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }
}
