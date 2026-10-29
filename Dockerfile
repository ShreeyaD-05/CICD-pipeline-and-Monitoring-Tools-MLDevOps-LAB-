FROM python:3.11-slim

WORKDIR /app

# Copy pre-downloaded Linux wheels and install from local directory
# (avoids network timeouts during docker build)
COPY requirements.txt .
COPY wheels/ /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && rm -rf /wheels

COPY . .

# Train the model while building the image
RUN python train.py

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "--threads", "4", "app:app"]
