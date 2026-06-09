FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Install CPU-only PyTorch first so EasyOCR does not pull CUDA/NVIDIA wheels.
RUN pip install --default-timeout=300 --retries 10 --no-cache-dir \
    torch==2.5.1 torchvision==0.20.1 \
    --index-url https://download.pytorch.org/whl/cpu

# Install the remaining extractor dependencies.
RUN pip install --default-timeout=300 --retries 10 --no-cache-dir -r requirements.txt

COPY app/ app/

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]