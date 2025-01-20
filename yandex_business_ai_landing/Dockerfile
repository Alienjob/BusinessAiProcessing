FROM python:3.12-slim

ARG GIT_PAT=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
ENV BRANCH_NAME=test

RUN apt-get update && \
    apt-get install -y git build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://x-access-token:${GIT_PAT}@github.com/Alienjob/yandex_ai_back_end.git . && \
    git checkout ${BRANCH_NAME}

WORKDIR /app/yandex_business_ai_landing
ENV FLASK_APP=app.py
# ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install --upgrade pip && \
    pip install -r requirements.txt 

EXPOSE 5000

CMD ["sh", "-c", "ls  && flask db upgrade && flask run"]
