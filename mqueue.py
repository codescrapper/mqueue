import memcache, random, string
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

HEAD_KEY = "mqueueheadpointer"
TAIL_KEY = "mqueuetailpointer"
SEPARATOR = "___"
VALUE_KEY = "value"
LINK_KEY = "link"


def random_id():
	rid = ''
	for x in range(8): rid += random.choice(string.ascii_letters + string.digits)
	return rid

class MQueue:
	def __init__(self):
		pass

	def is_empty(self):
		if self.get_head():
			return False
		return True

	def queue(self, value):
		new_key = random_id()
		mc.set(new_key + SEPARATOR + VALUE_KEY, value)
		if not self.get_head():
			mc.set(HEAD_KEY, new_key)
		if self.get_tail():
			mc.set(self.get_tail()+SEPARATOR+LINK_KEY, new_key)
		mc.set(TAIL_KEY, new_key)

	def dequeue(self):
		if self.is_empty():
			return None
		head = self.get_head()
		val = mc.get(head+SEPARATOR+VALUE_KEY)
		nxt = mc.get(head+SEPARATOR+LINK_KEY)
		mc.delete(head+SEPARATOR+LINK_KEY)
		mc.delete(head+SEPARATOR+VALUE_KEY)
		if not nxt:
			mc.delete(HEAD_KEY)
			mc.delete(TAIL_KEY)
		else:
			mc.set(HEAD_KEY, nxt)
		return val

	def get_head(self):
		return mc.get(HEAD_KEY)

	def get_tail(self):
		return mc.get(TAIL_KEY)



