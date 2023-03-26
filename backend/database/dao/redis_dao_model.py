import redis

default_time_out = 3 * 60 * 60
tredis = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


