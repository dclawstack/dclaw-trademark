FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e "."

COPY src ./src

EXPOSE 8141

CMD ["uvicorn", "dclaw_trademark.main:app", "--host", "0.0.0.0", "--port", "8141"]
