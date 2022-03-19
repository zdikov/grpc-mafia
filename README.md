# Mafia game implementaion based on grpc

## How to run server?
```sh
docker run -p 8080:<your_port> zdikov/grpc-mafia
```
## How to run client?

### Prepare
```sh
pip3 install -r requirements.txt
python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. mafia.proto
```
### Run client
```sh
python3 client.py
```
