FROM python:3.7

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    swig \
    cmake \
    libgl1-mesa-glx \
    libglu1-mesa \
    freeglut3-dev \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# 🔥 Pin old packaging tools
RUN pip install pip==21.3.1
RUN pip install setuptools==59.5.0
RUN pip install wheel==0.37.1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/AI Masterclass/Inference

CMD ["xvfb-run", "-s", "-screen 0 1400x900x24", "python", "full_world_model.py"]