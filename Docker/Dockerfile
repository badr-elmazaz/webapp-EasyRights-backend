FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9 AS stage1

ARG BUILD="gcc libffi-dev libc-dev python-dev"
WORKDIR /app

RUN apt-get update -y \
    && apt-get install git -y \
    && apt-get install -y wget \
    && apt install -y netcat \
    && python -m venv venv  \
    && apt-get install -y --no-install-recommends ${BUILD}


COPY . .

RUN venv/bin/pip install --no-cache-dir -r requirements.txt

RUN rm -rf requirements.txt
RUN python -m compileall -b .
RUN rm -rf **/*.py
RUN rm *.py
RUN wget -qO- https://raw.githubusercontent.com/eficode/wait-for/v2.2.1/wait-for > wait-for.sh


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
COPY --from=stage1 /app /app

#EXPOSE 5000
WORKDIR /app
ENV PATH="/app/venv/bin:$PATH"
RUN chmod +x wait-for.sh
RUN apt-get update -y
RUN apt install -y netcat
RUN apt-get install -y gcc


#CMD ["python", "app.pyc"]