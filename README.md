# arbicoin
A Proof of Concept CryptoCurrency Implementation

## Overview
This is the repo for the backend. The frontend repo is [here](https://github.com/zawan-ila/arbicoin-frontend) <br>

The app is live at `http://arbicoin.centralindia.cloudapp.azure.com`

## Build locally

1. Clone this repo `git clone https://github.com/zawan-ila/arbicoin.git`
2. Clone the frontend `git clone https://github.com/zawan-ila/arbicoin-frontend.git`
3. Inside both cloned repos checkout the container branch `git checkout remotes/origin/final`
4. Inside this repo run `docker-compose -f docker_compose_dev.yml --verbose up -d --build`
5. Your application is live at `localhost:3000`
