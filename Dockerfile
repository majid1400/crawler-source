FROM python:3.8-slim

RUN echo "[global]\nindex = http://repo-nexus.example.org:8081/repository/pypi-group/\nindex-url = http://repo-nexus.example.org:8081/repository/pypi-group/simple\ntrusted-host=repo-nexus.example.org" > /etc/pip.conf

WORKDIR /opt/app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /app .
WORKDIR /opt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
