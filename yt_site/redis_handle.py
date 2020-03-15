import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
from io import BytesIO

def is_redis_working(arg1,arg2):
	try:
		redis_client.set(arg1,arg2)
	except Exception as e:
		return e
	return True


def add_to_redis_feed(hash_of_image,image_data):
	try:
		redis_client.set(hash_of_image,image_data)
	except Exception as e:
		print(e)
		print("image "+hash_of_image+" Not saved to redis due to the above error")

def get_from_redis_feed(hash_of_image):
	if redis_client.exists(hash_of_image):
		buff=BytesIO(redis_client.get(hash_of_image))
		return buff.getvalue()
	else:
		return None
