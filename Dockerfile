FROM python:3.10-slim

WORKDIR /apps

RUN apt-get update && apt-get install -y python3-venv && apt-get clean

COPY ./req.txt .

RUN python3 -m venv env && env/bin/pip install --no-cache-dir --upgrade pip \
    && env/bin/pip install --no-cache-dir -r req.txt

COPY manage.py .
COPY apps/ ./apps/
COPY core/ ./core/

RUN chmod -R 755 /apps && chmod -R 755 env

ENV PATH="/apps/env/bin:$PATH"

RUN python --version
RUN which python
RUN ls -l /apps/env/bin

CMD ["env/bin/python", "manage.py", "runserver"]
