# Build stage
FROM python:3.9.13-slim
WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY ./ .
EXPOSE 5557
CMD ["./docker-entrypoint.sh"]
