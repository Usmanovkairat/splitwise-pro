FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ONCALL_STATE_DIR=/data
WORKDIR /srv/oncall
RUN useradd --uid 10001 --no-create-home responder && mkdir /data && chown responder /data
COPY responder.py ./
USER responder
EXPOSE 8080
CMD ["python", "responder.py"]
