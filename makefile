NAME=fossil-hunt

all: run

build:
	docker build -t ${NAME} .

run:
	xhost +local:docker
	docker run --rm \
		--privileged \
		--net=host \
		-e DISPLAY=${DISPLAY} \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		--device /dev/dri:/dev/dri \
		-p 8050:8050 \
		${NAME}
