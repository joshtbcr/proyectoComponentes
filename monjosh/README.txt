Docker
    - Creacion de imagenes con una base
    Comandos
        - docker image ls => ver todas las imagenes existentes
        
Docker Compose
    - Servicios apartir de imagenes
    Comandos
        - docker-compose build => construir los servicios basados en las imagenes
        - docker-compose up -d => levanta los servicios y el -d significa detach, para correrlo en background
        - docker-compose ps => para ver los containers
        - docker-compose restart => reiniciar los servicios
        - docker-compose stop
        - docker-compose start
        - docker-compose logs => para ver los logs
        - docker-compose down => bajar todos los servicios

Pasos desde 0
    - docker-compose ps => para validar si existe algo
    - docker-compose build