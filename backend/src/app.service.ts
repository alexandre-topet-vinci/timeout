import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Backend NestJS pour IA Sarcastique - API v1.0';
  }
}
