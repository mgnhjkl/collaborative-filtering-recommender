import math
import heapq

def pearson_correlation(user1, user2):
	collect1 = user_dict[user1]
	collect2 = user_dict[user2]
	r1 = sum([(float)(collect1[key]) for key in collect1]) / len(collect1)
	r2 = sum([(float)(collect2[key]) for key in collect2]) / len(collect2)
	intersect_items = set(collect1.keys()).intersection(set(collect2.keys()))
	dot_multi = 0.0
	numerator1 = 0.0
	numerator2 = 0.0
	for item in intersect_items:
		rating1 = (float)(collect1[item])
		rating2 = (float)(collect2[item])
		dot_multi += (rating1 - r1) * (rating2 - r2)
		numerator1 += pow((rating1 - r1), 2)
		numerator2 += pow((rating2 - r2), 2)
	return dot_multi / (math.sqrt(numerator1) * math.sqrt(numerator2))

def iterate_users(user1):
	for user in user_dict:
		if user != user1:
			yield pearson_correlation(user, user1), user

def K_nearest_neighbors(user1, k):
	k_heap = heapq.nlargest(k, iterate_users(user1))
	k_heap.sort(key = lambda tup : tup[1])
	k_heap.sort(key = lambda tup : tup[0], reverse = True)
	return [(tup[1], tup[0]) for tup in k_heap]

def Predict(user1, item, k_nearest_neighbors):
	pass

user_dict = dict()
item_dict = dict()
def readfile(filename):
	f = open(filename, "r")
	for line in  f.readlines():
		user_id, trating, movie_title = line.split("\t")
		user_dict.setdefault(user_id, dict())[movie_title] = trating
		item_dict.setdefault(movie_title, dict())[user_id] = trating

readfile("ratings-dataset.tsv")
pearson_correlation("Kluver", "JosephIsAwesome")
neighbors = K_nearest_neighbors("Kluver", 15)
for n in neighbors:
	print n