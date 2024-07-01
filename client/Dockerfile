FROM node:20.11.0-slim

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install --frozen-lockfile

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]