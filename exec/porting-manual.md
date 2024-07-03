# Project Porting Manual

<br>

## Contents
1. [Development Environment](#1-Development-Environment)
1. [Port Information](#2-Port-Information)
1. [Docker Installation](#3-Docker-Installation)
1. [Docker Image Build](#4-Docker-Image-Build)
1. [Docker Network Setting](#5-Docker-Network-Setting)
1. [Docker Container Execution](#6-Docker-Container-Execution)
1. [InfluxDB API Token Setting](#7-InfluxDB-API-Token-Setting)
1. [Environment Variables Setting](#8-Environment-Variables-Setting)

<br>

## 1. Development Environment
- Frontend IDE: Visual Studio Code 1.90.2
- Backend IDE: Pycharm Professional 2024.1.4
- Frontend: React 18.2.0, Node.js 20.11.0
- Backend: FastAPI 0.110.2, Python 3.11.9
- DB: InfluxDB 2.7.6, MongoDB 7.0.9
- Deployment: Docker 24.0.5
- OS: Ubuntu 22.04.4 LTS

<br>

## 2. Port Information
| Port | Name |
|:---:|:---:|
| 3000 | Frontend Docker Container |
| 8000 | Backend Docker Container |
| 8086 | InfluxDB Docker Container |
| 27017 | MongoDB Docker Container |

<br>

## 3. Docker Installation
```
$ sudo apt update && sudo apt upgrade -y
$ curl -fsSL https://get.docker.com -o dockerSetter.sh
$ chmod 711 dockerSetter.sh
$ ./dockerSetter.sh
```

<br>

## 4. Docker Image Build
### 4.1. Frontend
```
$ sudo docker build -t frontend-image:0.1 .
```
### 4.2. Backend
```
$ sudo docker build -t backend-image:0.1 .
```

<br>

## 5. Docker Network Setting
### 5.1. Create Docker Network
```
$ sudo docker network create -d bridge ssafy-network
```
### ※ Delete Docker Network
```
$ sudo docker network rm ssafy-network
```

<br>

## 6. Docker Container Execution
### 6.1. Start Docker Container
```
$ sudo docker compose up -d
```
### ※ Stop Docker Container
```
$ sudo docker compose down -v
```

<br>

## 7. InfluxDB API Token Setting
### 7.1. InfluxDB UI
```
http://localhost:8086/
```
### 7.2. Create API Token and copy

#### 7.2.1.<br>
![image](/uploads/4476cbce85e33c153e43a9e4cdcf1bf7/image.png)

#### 7.2.2.<br>
![image](/uploads/b47173b8000d32f4b2a489be59dadfe3/image.png)

#### 7.2.3.<br>
![image](/uploads/c12f9b18791ce76de0e0cd29c9f3ad19/image.png)

#### 7.2.4.<br>
![image](/uploads/7abfa5204b71e79688619c526bdef406/image.png)

<br>

## 8. Environment Variables Setting
### 8.1. Connect Backend Container
```
$ sudo docker exec -it backend bash
# vim .env
```
### 8.2. .env
```
ENVIRONMENT=dev

MONGO_FURL=mongodb://[MongoDB Username]:[MongoDB Password]@mongodb:27017

INFLUXDB_URL=http://influxdb:8086
INFLUXDB_ORG=ssafy
INFLUXDB_BUCKET=facility
INFLUXDB_TOKEN=[Copied API Token]
```
### 8.3. Restart Backend Container
```
# exit
$ sudo docker restart backend
```
