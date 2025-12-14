FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY app ./app
ENV DATABASE_URL=sqlite:///./contracts.db
EXPOSE 18013
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "18013"]