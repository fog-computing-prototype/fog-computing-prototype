# Build stage
FROM node:lts-alpine3.16 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build

# Production stage
FROM nginx:1.23.0-alpine as production-stage
# RUN mkdir /app
# COPY --from=build-stage /app/dist /app
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]