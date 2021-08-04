FROM python:3.8
ENV VAR1 IEV

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app
#RUN useradd appuser && chown -R appuser /app
#USER appuser

EXPOSE 8080

CMD [ "python3", "./mainAlertman2omi.py"]
