FROM node:21.6-slim

USER root
WORKDIR /app

RUN npm install -g @quasar/cli && \
    npm install -g @vue/cli && \
    npm install -g @vue/cli-init && \
    npm i workbox-webpack-plugin

COPY ./frontend/package*.json /app

RUN npm install

COPY ./frontend /app

RUN quasar build --mode pwa

CMD ["quasar", "serve", "dist/pwa"]
