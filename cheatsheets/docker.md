---
title: docker cheatsheet
tags:
  - cheatsheet
  - docker
migrated_from: denisidoro/cheats (navi)
---

# docker cheatsheet

## Docker

**Remove an image**

```bash
docker image rm <image_id>
```

**Delete an image from the local image store**

```bash
docker rmi <image_id>
```

**Clean none/dangling images**

```bash
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
```

**Force clean none/dangling images**

```bash
docker rmi $(docker images --filter "dangling=true" -q --no-trunc) -f
```

**List all images that are locally stored with the Docker engine**

```bash
docker images
```

**Build an image from the Dockerfile in the current directory and tag the image**

```bash
docker build -t <image>:<version> .
```

**Pull an image from a registry**

```bash
docker pull <image>:<version>
```

**Stop a running container through SIGTERM**

```bash
docker stop <container_id>
```

**Stop a running container through SIGKILL**

```bash
docker kill <container_id>
```

**List the networks**

```bash
docker network ls
```

**List the running containers**

```bash
docker ps
```

**Delete all running and stopped containers**

```bash
docker rm -f $(docker ps -aq)
```

**Create a new bash process inside the container and connect it to the terminal**

```bash
docker exec -it <container_id> bash
```

**Print the last lines of a container's logs**

```bash
docker logs --tail 100 <container_id> | less
```

**Print the last lines of a container's logs and following its logs**

```bash
docker logs --tail 100 <container_id> -f
```

**Create new network**

```bash
docker network create <network_name>
```

## Docker-Compose

**Builds, (re)creates, starts, and attaches to containers for all services**

```bash
docker-compose up
```

**Builds, (re)creates, starts, and dettaches to containers for all services**

```bash
docker-compose up -d
```

**Builds, (re)creates, starts, and attaches to containers for a service**

```bash
docker-compose up -d <service_name>
```

**Builds, (re)creates, starts, and dettaches to containers for a service**

```bash
docker-compose up -d <service_name>
```

**Print the last lines of a service’s logs**

```bash
docker-compose logs --tail 100 <service_name> | less
```

**Print the last lines of a service's logs and following its logs**

```bash
docker-compose logs -f --tail 100 <service_name>
```

**Stops containers and removes containers, networks created by up**

```bash
docker-compose down
```
