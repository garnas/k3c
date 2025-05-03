docker rmi -f $(docker images -aq)
docker volume rm $(docker volume ls -q --filter dangling=true)
