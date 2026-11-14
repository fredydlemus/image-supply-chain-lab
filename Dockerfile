FROM python:3.12-slim

WORKDIR /app

COPY src/ .

RUN useradd -m appuser && \
    chown -R appuser:appuser /app

ARG APP_VERSION
ARG GIT_SHA
ARG BUILD_SOURCE=laptop

ENV APP_VERSION=${APP_VERSION} \
    GIT_SHA=${GIT_SHA} \
    BUILD_SOURCE=${BUILD_SOURCE}

USER appuser

EXPOSE 8080

CMD ["python", "app.py"]