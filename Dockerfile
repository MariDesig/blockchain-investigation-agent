FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "blockchain_agent.main", "--network", "ethereum", "--seeds", "0xSERVICE_A", "0xSERVICE_B", "--depth", "2"]
