# Strumento di conversione dei documenti del cliente per gli agenti.
# MarkItDown (Microsoft) estrae testo, titoli e tabelle da DOCX, XLSX/XLS,
# PDF e PPTX in Markdown; nessun servizio esterno, tutto in locale.
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir "markitdown[docx,xlsx,xls,pdf,pptx]==0.1.8"
WORKDIR /tool
COPY .docker/documents/convert.py /tool/convert.py
ENTRYPOINT ["python", "/tool/convert.py", "--input", "/documents", "--output", "/out"]
