import mongo
import motordb
import redis
from config import config
import log


def get_redis(db=0):
    redis_cli = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=db,
                            password=config.REDIS_PASSWORD)
    return redis_cli


def get_col_account_member():
    return motordb.mongo_collection('account', 'member', config.DB_HOST, config.DB_PORT)

