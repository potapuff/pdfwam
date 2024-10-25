FROM frolvlad/alpine-python2

RUN apk add --no-cache git && \
    pip install requests

RUN git clone https://github.com/potapuff/pdfwam.git /pdfwam

WORKDIR /pdfwam

ENTRYPOINT ["python", "pdfchecker.py"]

# Usage:
# docker build -t pdfwam .
# For Linux:
# docker run --rm -v $(pwd)/pdf:/pdf pdfwam /pdf/test.pdf -q -r
# or for Windows
# docker run --rm -v %cd%/pdf:/pdf pdfwam /pdf/test.pdf -q -r