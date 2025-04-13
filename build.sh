#!/usr/bin/env bash

# Install system dependencies for Playwright Chromium
apt-get update && apt-get install -y \
  libgtk-4-1 \
  libgraphene-1.0-0 \
  libgstgl1.0-0 \
  libgstcodecparsers-1.0-0 \
  libavif15 \
  libenchant-2-2 \
  libsecret-1-0 \
  libmanette-0.2-0 \
  libgles2

# Install Playwright browsers (Chromium in this case)
playwright install