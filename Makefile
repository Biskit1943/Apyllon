VERSION=$(shell ./version.sh)
APP_NAME=poi-storage

.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

dev-aarch64:  ## Build the development aarch64 image
	@echo 'building apyllon:$(VERSION)-dev'
	docker run --privileged yen3/binfmt-register set aarch64 & \
	docker build \
		--tag apyllon-arm64v8:latest-dev \
		--tag apyllon-arm64v8:$(VERSION)-dev \
		--file ./docker/Dockerfile.frontend.aarch64v8.dev . \
	& \
	docker build \
		--tag apyllon-arm64v8:latest-dev \
		--tag apyllon-arm64v8:$(VERSION)-dev \
		--file ./docker/Dockerfile.backend.aarch64v8.dev .
	docker run --privileged yen3/binfmt-register clear aarch64

