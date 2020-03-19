# service tags

## Build docker image
sudo docker build -t tag_service .

## Start docker
sudo docker run -p 3005:5000 -t tag_service

## To start service (2 worker - edit number of workers in run_serice.sh)
chmod 777 ./scripts/run_service.sh

./scripts/run_service.sh