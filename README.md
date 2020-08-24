# REST API Monitor


## Setup for development

### Prerequisites:

- npm
- pip 
- python 3
- docker 

```sh 
docker run --name some-redis -p 6379:6379 -d redis
celery -A tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery -A tasks woker -l info
```

## TODO

- User interface
- Socket push events
- Unit tests