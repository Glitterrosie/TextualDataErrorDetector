FROM python:3.11-slim
RUN pip install poetry
# set the current working directory inside the container
WORKDIR /src
# Copy dependency files
COPY pyproject.toml poetry.lock ./
# Avoid creating a virtualenv in a container
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY src/ /src/
COPY datasets/ /datasets/
# Default command when the container starts
CMD ["python3", "main.py"]