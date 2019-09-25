help:
		@echo ""
		@echo "Usage: make COMMAND"
		@echo ""
		@echo "A Makefile for building docker project "
		@echo ""
		@echo "Commands:"
		@echo "help                 Show help messgae."
		@echo "start-docker         Starts docker service."
		@echo "start-docker2        Starts docker service."
		@echo "server               Build and Up docker container"
		@echo ""

start-docker:
	sudo systemctl start docker

start-docker2:
	sudo dockerd

server:
	sudo docker-compose up --build

bash:
	sudo docker exec -it monitoria-api sh