FROM registry.baidubce.com/paddlepaddle/paddle:2.1.2

WORKDIR /app

RUN pip install paddleocr flask_cors

COPY . .

EXPOSE 5000

EXPOSE $PORT

ENTRYPOINT ["python"]
CMD ["app.py"]