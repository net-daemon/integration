# Using the same image as the vs code devcontainers for consistency
# for non-vs code users.
# Neovim is setup as the default editor.
FROM mcr.microsoft.com/devcontainers/python:3.12

# Set the working directory to /home/vscode/src
WORKDIR /home/vscode

# Install Neovim
RUN apt-get update && apt-get install -y \
    wget \
    libfuse2 \
    cmake \
    curl \
    pkg-config \
    libtool \
    unzip \
    ansible-lint \
    libfuse2 \
    libpcap-dev \
    libturbojpeg0 \
    ffmpeg 


# Install the latest Go
RUN wget https://golang.org/dl/go1.23.4.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz && \
    rm go1.23.4.linux-amd64.tar.gz

# Set Go environment variables
ENV PATH=$PATH:/usr/local/go/bin


COPY scripts/docker_setup.sh /usr/src/install.sh
COPY scripts/setup /usr/src/scripts/setup.sh
COPY requirements.txt /usr/src/requirements.txt

RUN chmod +x /usr/src/install.sh
RUN chmod +x /usr/src/scripts/setup.sh

USER vscode
# Run the install.sh script to install the necessary dependencies for Neovim
RUN /usr/src/install.sh

# Install the Home Assistant dependecies
RUN /usr/src/scripts/setup.sh

WORKDIR /home/vscode/src

# Set Neovim as the default editor
ENV EDITOR=nvim
ENV VISUAL=nvim

