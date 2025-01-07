#!/bin/bash

# Build the Docker container
docker build -t nd_integration_development .

# Run the container and execute a bash prompt inside it
docker run -it -p 8123:8123 -v "$(pwd)":/home/vscode/src -v ~/.config/nvim:/home/vscode/.config/nvim nd_integration_development /bin/bash 

