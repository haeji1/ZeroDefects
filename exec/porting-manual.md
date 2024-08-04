# Project Porting Manual

<br>

## Contents
1. [Development Environment](#1-development-environment)
1. [Port Information](#2-port-information)
1. [Docker Installation](#3-docker-installation)
1. [Docker Image Build](#4-docker-image-build)
1. [Docker Network Setting](#5-docker-network-setting)
1. [Docker Container Execution](#6-docker-container-execution)
1. [InfluxDB API Token Setting](#7-influxdb-api-token-setting)
1. [Environment Variables Setting](#8-environment-variables-setting)

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
![image](https://github.com/user-attachments/assets/73be1c4b-7bab-450c-998a-643a24ebc672)

#### 7.2.2.<br>
![image](https://github.com/user-attachments/assets/23fd3b65-7ab8-4586-a939-4c1f786d32b7)

#### 7.2.3.<br>
![image](https://github.com/user-attachments/assets/f37abf0d-0942-4d06-be03-8791f05c2ea6)

#### 7.2.4.<br>
![image](https://github.com/user-attachments/assets/4253912c-7ee6-4c8e-8f72-b5caccc95f68)

<br>

## 8. Environment Variables Setting
### 8.1. Connect Backend Container
```
$ sudo docker exec -it backend bash
```
### 8.2. Create .env File
```
# vim .env
```
### 8.3. .env File Contents
```
ENVIRONMENT=dev

MONGO_FURL=mongodb://[MongoDB Username]:[MongoDB Password]@mongodb:27017

INFLUXDB_URL=http://influxdb:8086
INFLUXDB_ORG=ssafy
INFLUXDB_BUCKET=facility
INFLUXDB_TOKEN=[Copied API Token]
```
### 8.4. Restart Backend Container
```
# exit
$ sudo docker restart backend
```
