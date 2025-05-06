FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install --only=production

COPY src ./src
RUN chmod -R a+x /app

USER nobody

EXPOSE 9000
CMD ["npm", "start"]
