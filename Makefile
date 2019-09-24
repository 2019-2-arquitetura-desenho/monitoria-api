help:
		@echo ""
		@echo "Usage: make COMMAND"
		@echo ""
		@echo "A Makefile for building docker project "
		@echo ""
		@echo "Commands:"
		@echo "help          Show help messgae."
		@echo "server        Build and Up docker container"
		@echo ""

start-docker:
	sudo systemctl start docker

server:
	sudo docker-compose up --build