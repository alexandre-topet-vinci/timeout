FROM node:20-alpine AS builder

WORKDIR /app

# Variable d'environnement pour le build
ARG NEXT_PUBLIC_API_URL=http://localhost:3002
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Copier package.json
COPY package*.json ./
RUN npm install

# Copier le code source
COPY . .

# Build l'application
RUN npm run build

# Image de production
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV production

# Copier les fichiers nécessaires
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Exposer le port
EXPOSE 3000

# Démarrer l'application
CMD ["node", "server.js"]
