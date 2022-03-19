FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3-pip
COPY . .
RUN pip3 install -r requirements.txt
RUN python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. mafia.proto
ENTRYPOINT ["python3", "server.py"]

