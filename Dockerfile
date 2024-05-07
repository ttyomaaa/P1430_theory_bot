FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 80

WORKDIR ~/

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . ./

CMD ["sh", "./start.sh", "&&", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
