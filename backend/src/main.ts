import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // CORS pour Next.js
  app.enableCors({
    origin: [
      'http://localhost:1418',
      'http://localhost:3000',
      process.env.FRONTEND_URL || 'http://localhost:1418'
    ],
    credentials: true,
  });
  
  const port = process.env.PORT || 3001;
  await app.listen(port);
  console.log(`🚀 Backend NestJS démarré sur le port ${port}`);
}

bootstrap();
