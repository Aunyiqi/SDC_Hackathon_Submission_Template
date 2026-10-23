FROM runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404

WORKDIR /app

# RunPod's build log showed that git is not available in this base image.
# Install only the missing system dependency before Python packages are resolved.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY runpod/requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

# Pre-download the English EasyOCR model during image build so the first
# serverless request does not need to fetch model weights.
RUN python -c "import easyocr; easyocr.Reader(['en'], gpu=False)"

COPY runpod/handler.py /app/handler.py

CMD ["python", "-u", "/app/handler.py"]
