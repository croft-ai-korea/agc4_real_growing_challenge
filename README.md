# agc4_real_growing_challenge


## Requirements
- docker
- enough disk space (8~9GB)

## Reinstallation
- if you want to reinstall this repository, follow instruction below.
1. docker-compose down
2. docker-compose up --build -d
3. check if pm2 is working well (per_day, per_15min, per_5min process should be shown as below)
```
sudo docker exec -it agrifusion /bin/bash
pm2 list
pm2 logs per_5min
```
![image](https://github.com/user-attachments/assets/b2606d8d-1df0-4e60-ad43-722e8de2070a)


## Installation

```sh
sudo docker build -t agrifusion:1.1 .
# make database folder
mkdir tsdbdata
sudo docker-compose up -d
```

## pm2 scheduler check
```
sudo docker exec -it agrifusion /bin/bash
pm2 list
pm2 logs per_5min
```

## after first build
WARNING: Image for service ai_greenhouse_climate_controller was built because it did not already exist. 
To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.

