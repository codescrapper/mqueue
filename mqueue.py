import memcache, random, string
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

HEAD_KEY = "mqueuehead"
TAIL_KEY = "mqueuetail"
SEPARATOR = "___"
VALUE_KEY = "value"
LINK_KEY = "link"


def random_id():
	rid = ''
	for x in range(8): rid += random.choice(string.ascii_letters + string.digits)
	return rid

class MQueue:
	def __init__(self):
		self.head = mc.get(HEAD_KEY)
		self.tail = mc.get(TAIL_KEY)

	def is_empty(self):
		if self.head:
			return False
		return True

	def queue(self, value):
		new_key = random_id()
		mc.set(new_key + SEPARATOR + VALUE_KEY, value)
		if not self.head:
			self.head = new_key
		if self.tail:
			mc.set(self.tail+SEPARATOR+LINK_KEY, new_key)
		self.tail = new_key
		mc.set(TAIL_KEY, self.tail)

	def dequeue(self):
		if self.is_empty():
			return None
		val = mc.get(self.head+SEPARATOR+VALUE_KEY)
		nxt = mc.get(self.head+SEPARATOR+LINK_KEY)
		mc.delete(self.head+SEPARATOR+LINK_KEY)
		mc.delete(self.head+SEPARATOR+VALUE_KEY)
		if not nxt:
			self.head = None
			mc.delete(HEAD_KEY)
		else:
			self.head = nxt
			mc.set(HEAD_KEY, self.head)
		return val



