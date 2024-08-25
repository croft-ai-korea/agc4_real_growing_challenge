# agc4_real_growing_challenge


## Requirements
- docker
- enough disk space (8~9GB)


## Installation

```sh
sudo docker build -t agrifusion:1.1 .
# make database folder
mkdir tsdbdata
sudo docker-compose up -d
```

## scheduler check
```
sudo docker exec -it agrifusion /bin/bash
pm2 list
pm2 logs stragety_5min
```


