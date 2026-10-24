FROM runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# The RunPod PyTorch base image ships a Debian-managed cryptography package
# without pip RECORD metadata. Install the version required by RunPod on top
# without attempting to uninstall the system copy.
RUN python -m pip install --no-cache-dir --ignore-installed "cryptography>=50,<51"

# Keep torchvision aligned with the base image's torch 2.9.1 + CUDA 12.8.
# Installing it first prevents EasyOCR's dependency resolver from replacing
# the preinstalled PyTorch/CUDA stack with a newer incompatible build.
RUN python -m pip install --no-cache-dir --no-deps \
    --index-url https://download.pytorch.org/whl/cu128 \
    "torchvision==0.24.1"

COPY runpod/requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

# Pre-download the English EasyOCR model during image build so the first
# serverless request does not need to fetch model weights.
RUN python -c "import easyocr; easyocr.Reader(['en'], gpu=False)"

COPY runpod/handler.py /app/handler.py

CMD ["python", "-u", "/app/handler.py"]
