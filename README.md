# REST API Monitor

A service to monitor microservice REST APIs. The service provides the following functionality:

- Send EMAIL Alerts when monitoring service(s) go down
- Dashboard Webpage to monitor the response time(s)
- Status Webpage to show the service(s) status

## Screenshots 

![Dashboard](/docs/dashboard.png)
![Status](/docs/status.png)

## Configure and run the service 

```sh 
docker run -p 80:80 --name sharp-eye \
-e EMAIL_HOST=<hostname> \
-e EMAIL_USE_TLS=<True|False> \
-e EMAIL_PORT=<email_port> \
-e EMAIL_HOST_USER=<EMAIL_HOST_USER> \
-e EMAIL_HOST_PASSWORD=<EMAIL_HOST_PASSWORD> \
-d sharp-eye:latest
```

By default all the micro-services need to be monitored are stored in a file `config.json`. In order to pass your 
configuration, create a file like below:

```sh 
{
  "config": {
    "retention": "30 minutes",
    "total_consecutive_failures_2_alert": 3,
    "destination_email": "romaank@gmail.com"
  },
  "monitor": {
    "service-1": {
      "request": {
        "url": "https://jsonplaceholder.typicode.com/posts/",
        "method": "get"
      },
      "frequency": "7 seconds",
      "expected_response": {
        "status_code": 200
      }
    }
  }
}
```

and mount it to docker file like below:

```sh 
docker run -p 80:80 --name sharp-eye \
-e EMAIL_HOST=<hostname> \
-e EMAIL_USE_TLS=<True|False> \
-e EMAIL_PORT=<email_port> \
-e EMAIL_HOST_USER=<EMAIL_HOST_USER> \
-e EMAIL_HOST_PASSWORD=<EMAIL_HOST_PASSWORD> \
-v config.json/opt/webapp/config.json \
-d sharp-eye:latest
```

## Build

All the build scripts and configurations are located in `build` directory. Following the below steps will build a 
ready to run docker image:

```sh 
cd build 
./build.sh
```

## Execute

Run the below command:

```sh
docker run -d -p 80:80 --name sharp-eye sharp-eye
```

## Setup for development

### Prerequisites:

- node v12.16.1
- pip 3
- python 3
- docker 

In order to start development, please run redis:
```sh 
docker run --name redis -p 6379:6379 -d redis
```

Start Celery Beat:

```sh
celery -A tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Start Celery Worker:

```sh
celery -A tasks woker -l info
```

