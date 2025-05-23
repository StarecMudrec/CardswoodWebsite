FROM node:16-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm run build

COPY . /app

EXPOSE 5173

CMD ["npm", "run", "dev"]