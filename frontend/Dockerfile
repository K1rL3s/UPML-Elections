FROM node:21.6-slim

USER root
WORKDIR /app

RUN npm install -g @quasar/cli && \
    npm install -g @vue/cli && \
    npm install -g @vue/cli-init

COPY ./frontend/package*.json /app

RUN npm install

COPY ./frontend /app

RUN quasar build --mode pwa

CMD ["quasar", "serve", "dist/pwa"]
