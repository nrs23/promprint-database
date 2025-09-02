# promprint/Dockerfile
FROM python:3.13-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install uv
RUN pip install uv

WORKDIR /app

# Copy uv project files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using uv's project management
RUN uv sync --frozen --no-dev

COPY . /app/

EXPOSE 8070

# Command for production
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8070", "promprint.wsgi"]
