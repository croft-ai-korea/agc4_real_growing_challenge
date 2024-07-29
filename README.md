# agc4_real_growing_challenge

## Installation

```
sudo docker build -t agrifusion:1.0 .
sudo docker-compose up -d
```

## scheduler check
```
sudo docker exec -it agrifusion /bin/bash
pm2 list
pm2 logs stragety_5min
```