#!/bin/bash

set -euxo pipefail

apt-get update
apt install --no-install-recommends \
  terminator \
  tmux \
  vim \
  libsm6 \
  libxext6 \
  libxrender-dev \
  gedit \
  git \
  openssh-client \
  unzip \
  htop \
  libopenni-dev \
  apt-utils \
  usbutils \
  dialog \
  python3-virtualenv \
  python3-dev \
  python3-pip \
  ffmpeg \
  nvidia-settings \
  libffi-dev \
  flex \
  bison
