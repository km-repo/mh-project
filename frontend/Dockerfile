# Frontend Dockerfile
FROM node:20

WORKDIR /app
COPY frontend/ /app

RUN npm install
RUN npm run build

# Serve with a lightweight webserver
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]