#!/usr/bin/env bash

set -e

# Install Node LTS
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh |  bash

export NVM_DIR="/usr/local/share/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

nvm install 22 

wget "https://github.com/BurntSushi/ripgrep/releases/download/14.1.1/ripgrep_14.1.1-1_amd64.deb"
sudo dpkg -i ripgrep_14.1.1-1_amd64.deb

# Install Neovim version 0.10.0
wget https://github.com/neovim/neovim/releases/download/v0.10.3/nvim.appimage
sudo chmod u+x /home/vscode/nvim.appimage
./nvim.appimage --appimage-extract
sudo mv squashfs-root /
sudo ln -s /squashfs-root/AppRun /usr/bin/nvim

# RUN wget https://github.com/neovim/neovim/releases/download/v0.10.3/nvim.appimage && \
#     sudo chmod u+x /home/vscode/nvim.appimage && \
#     ./nvim.appimage --appimage-extract && \
#     mv squashfs-root / && \
#     sudo ln -s /squashfs-root/AppRun /usr/bin/nvim \
#     git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf \

