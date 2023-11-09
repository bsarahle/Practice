## Understanding Environment variables
- Explain why do we need env variables using wp-mysql stack and moving to different environments
- Create an wordpress container: `sudo docker run --rm --name wp -d -p 8081:80 wordpress`
- Exec into container and try to echo an env var: `echo $WORDPRESS_DB` (no output)
- Now expose this env var at runtime: `sudo docker run --rm --name wp -d -p 8081:80 -e WORDPRESS_DB=wp_db wordpress`
- Now echo it and may be access it from php:
```
# cat test.php
<?php
echo getenv('WORDPRESS_DB');
echo "\n";
?>

php test.php
```

### Understating networking
#### Default Bridge Network
- Create *MariaDB* dockerfile Dockerfile_db:
```
FROM mariadb:10.6.4-focal

ENV MYSQL_ROOT_PASSWORD=somewordpress
ENV MYSQL_DATABASE=wordpress
ENV MYSQL_USER=wordpress
ENV MYSQL_PASSWORD=wordpress

EXPOSE 3306 33060
```
- Build the image: `sudo docker build -t db . -f Dockerfile_db`

- Create the container: `sudo docker run --rm -d --name db db`

- Create *Wordpress* dockerfile Dockerfile_wp:
```
FROM wordpress:latest

RUN apt-get update && \
  apt-get install -y mariadb-client vim

ENV WORDPRESS_DB_HOST=db
ENV WORDPRESS_DB_USER=wordpress
ENV WORDPRESS_DB_PASSWORD=wordpress
ENV WORDPRESS_DB_NAME=wordpress

EXPOSE 80
```

- Build Image: `sudo docker build -t wp . -f Dockerfile_wp`

- Create container: `sudo docker run --rm --name wp -d -p 8081:80 wp`

- Now try to browse wordpress home page: `http://192.168.56.3:8081`
  - It should show db connection error. why?
  - Containers, by default, attached to default bridge network and they can communicate with their IP address but not their name. also security wise its not good practice as each container in that default bridge network knows which ports are exposed by other containers

- Now inspect the db container and find the IP: `sudo docker inspect db | grep IPAddress`

- Now use the IP to set `WORDPRESS_DB_HOST` env variable of `wp` container, so that it can connect to db container: `sudo docker run --rm --name wp -d -p 8081:80 -e WORDPRESS_DB_HOST="172.17.0.3" wp`

- Now try loading the wordpress: `http://192.168.56.3:8081`

#### Custom Network
- Stop the DB and WP cotainers

- Create network: `sudo docker network create wp-net`
```
$ sudo docker network list
NETWORK ID     NAME      DRIVER    SCOPE
c52e5ae4f2cc   bridge    bridge    local
cdf393cf6837   host      host      local
8e5a7cdb4b77   none      null      local
dbc3a0661e54   wp-net    bridge    local
```

- Create the wp and db containers now in `wp-net` network
```
sudo docker run --rm --name wp -d -p 8081:80 --network=wp-net wp

sudo docker run --rm --name db -d --network=wp-net db
```

- Inspect the containers to check their network

### Composer
- Create a composer file ` wp-compose.yaml` combining both wp and db dockerfiles

- Create the containers: `sudo docker compose -f wp-compose.yaml up -d`

- New Containers are up and they are attached to a new network `docker-compose_default`:
```
$ sudo docker network list
NETWORK ID     NAME                     DRIVER    SCOPE
c52e5ae4f2cc   bridge                   bridge    local
e3a34983658d   docker-compose_default   bridge    local
cdf393cf6837   host                     host      local
8e5a7cdb4b77   none                     null      local
dbc3a0661e54   wp-net                   bridge    local
```
- Stop the contaienrs: `sudo docker compose -f wp-compose.yaml down`
```
[+] Running 3/3
 ✔ Container docker-compose-wordpress-1  Removed                      1.2s
 ✔ Container docker-compose-db-1         Removed                      0.6s
 ✔ Network docker-compose_default        Removed                      0.1s
```

#### Composer using multiple containers
- Create composer file: `wp-compose-scale.yaml`
- To view logs: `sudo docker compose -f wp-compose-scale.yaml logs -f`
