FROM python:3.12
WORKDIR /app
COPY pyproject.toml poetry.lock alembic.ini entrypoint.sh ./
COPY db ./db
COPY migrations ./migrations
COPY repository ./repository
COPY utils ./utils
COPY services ./services

RUN apt-get update && apt-get install -y libgl1-mesa-glx && \
    python -m pip install --upgrade pip && \
    pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-cache --no-interaction

CMD ["sh", "./entrypoint.sh"]
