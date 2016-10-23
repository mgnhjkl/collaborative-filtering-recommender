 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import math
import heapq
import sys

def pearson_correlation(user1, user2):
	collect1 = user_dict[user1]
	collect2 = user_dict[user2]
	intersect_items = set(collect1.keys()).intersection(set(collect2.keys()))
	r1 = avg_ratings(user1, intersect_items)
	r2 = avg_ratings(user2, intersect_items)
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

def iterate_users(user1, item):
	for user in user_dict:
		if user != user1 and argv[3] in user_dict[user]:
			yield pearson_correlation(user, user1), user

def K_nearest_neighbors(user1, k, item):
	k_heap = heapq.nlargest(k, iterate_users(user1, item))
	k_heap.sort(key = lambda tup : tup[1])
	k_heap.sort(key = lambda tup : tup[0], reverse = True)
	return [(tup[1], tup[0]) for tup in k_heap]

def avg_ratings(user, intersect_items):
	collect = user_dict[user]
	return sum([(float)(collect[key]) for key in intersect_items]) / len(intersect_items)

def Predict(user1, item, k_nearest_neighbors):
	a_items = user_dict[user1].keys()
	a_items = set(a_items)
	ra = avg_ratings(user1, a_items)
	pai = 0.0
	numerator = 0.0
	denominator = 0.0
	for user, pc in k_nearest_neighbors:
		if item in user_dict[user]:
			collect1 = user_dict[user1]
			collect2 = user_dict[user]
			intersect_items = set(collect1.keys()).intersection(set(collect2.keys()))
			numerator += pc * ((float)(user_dict[user][item]) - avg_ratings(user, intersect_items))
			denominator += abs(pc)
	return ra + numerator / denominator

user_dict = dict()
def readfile(filename):
	f = open(filename, "r")
	for line in  f.readlines():
		user_id, trating, movie_title = line.split("\t")
		movie_title = movie_title.strip()
		user_id = user_id.strip()
		user_dict.setdefault(user_id, dict())[movie_title] = trating

def main(argv):
	filename = argv[1]
	user = argv[2]
	item = argv[3]
	k = (int)(argv[4])
	readfile("ratings-dataset.tsv")
	neighbors = K_nearest_neighbors(user, k, item)
	p = Predict(user, item, neighbors)
	for n in neighbors:
		print str(n[0]) + " " + str(n[1])
	print str(p)


if __name__ == '__main__':
	argv = sys.argv
	main(argv)
