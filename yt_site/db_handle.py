import psycopg2
isError=False
cursor="blah"

try:
	connection = psycopg2.connect(user = "postgres",
								  password = "jaxtek",
								  host = "127.0.0.1",
								  port = "5432",
								  database = "postgres")
	cursor = connection.cursor()

except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)
	isError=True


def get_n_image_hashes_and_tags(offset):
	offset=int(offset)-1 #If pageNo is 2,we should skip first "10" images.And offset 0 doesn't produce an error
	offset=offset*10
	cursor.execute("select hash_id from yt_table order by time_of_upload desc limit 10 offset %s;",(offset,))
	hashes_from_db=cursor.fetchall()
	hashes_and_tags=[]
	# raw_hashes=[]
	for hash_ in hashes_from_db:
		hash_and_tag=[]
		hash_and_tag.insert(0,f"{hash_[0]}")
		tags=get_tags_from_hash(f"{hash_[0]}")
		for i,tag in enumerate(tags):
			hash_and_tag.insert(i+1,tag)
		hashes_and_tags.insert(len(hashes_and_tags),hash_and_tag)
		print(hashes_and_tags)
	return hashes_and_tags
	# hashes_and_tags=[['hash','tag1','tag3','tag4','tag5'],['hash','tag1','tag3','tag4','tag5'],.....]

def get_tags_from_hash(hash_id):
	cursor.execute("select tags from yt_table where hash_id=%s",(hash_id,))
	tags_from_db=cursor.fetchall()
	return tags_from_db[0][0]
	# return raw_hashes
# get_tags_from_hash("dcccccd2c8c7c3cc")

def add_to_db(hash_id,tags):
	try:
		# test_list=["wonders","are","done","in","rooms"]
		cursor.execute("INSERT into yt_table(hash_id,time_of_upload,tags) values(%s,current_timestamp,%s)",(hash_id,tags,))
		connection.commit()#DND
		return None
	except Exception as e:
		print(e)
		connection.commit()#Do not remove.If you remove this,all insertions will be cancelled if one primary key violation occurs.
		return e