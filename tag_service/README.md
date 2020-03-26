# service tags

## Build docker image
sudo docker build -t tag_service .

## Start docker
sudo docker run -p 3005:5000 -t tag_service

## To start service (2 worker - edit number of workers in run_serice.sh)
chmod 777 ./scripts/run_service.sh

./scripts/run_service.sh

## Run api :
	cài docker, python (>3.0)
	ùng command prompt trỏ tới thư mục "tag_serice" chạy các lệnh sau:
		docker build -t tag_service .

		docker rm -f tag_service_July18

		docker run -p 3005:5000 --name tag_service_July18 --restart always -t tag_service bash -c "chmod 777 ./scripts/run_service.sh && ./scripts/run_service.sh"