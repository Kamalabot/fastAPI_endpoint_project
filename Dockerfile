FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.main_withORM:app", "--host", "0.0.0.0", "--port", "8000"]
