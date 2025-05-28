FROM node:16-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm install browser-image-compression

COPY . /app

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev"]