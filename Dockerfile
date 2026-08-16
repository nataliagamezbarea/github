FROM python:3.12-slim

# Instalar dependencias de sistema necesarias para tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    tcl \
    git \
    zenity \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar script y requirements
COPY python.py requirements.txt icon.png ./
COPY app ./app



# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x python.py

CMD ["python", "python.py"]
