import sys
import math

EPSILON = 0.001


class Cluster:
    def __init__(self, vector):
        self.centroid = [num for num in vector]
        self.prev_centroid = None
        self.d = len(vector)
        self.sum_vector = [0] * self.d
        self.size = 0


    def reset(self):
        self.sum_vector = [0] * self.d
        self.size = 0

    def add(self, x_vector):
        self.size += 1
        for i in range(self.d):
            self.sum_vector[i] += x_vector[i]

    def update(self):
        self.prev_centroid = [num for num in self.centroid]
        self.centroid = [(sum / self.size) for sum in self.sum_vector]
        self.reset()

    def __repr__(self):
        res = ""
        for num in self.centroid:
            res = f"{res},{num:.4f}"    #in c maybe need to add \n
        return res[1:]


# vectors are arrays with fixed lengths, with floats in each index
def distance(u, v):
    n = len(u)
    if n != len(v):
        print("error in d func: vector lengths are incompatible")
        return -1

    sum_under_root = 0
    for i in range(n):
        sum_under_root += (u[i] - v[i]) ** 2
    return math.sqrt(sum_under_root)

def is_int(num):
    try:
        if int(num) != float(num):
            return 1
        return 0
    except:
        return 2

def check_numeric_validity(k, iter):
    if is_int(k) == 1:
        print("Invalid number of clusters!")
        return False
    elif is_int(k) == 2:
        print("Non numeric number of clusters!")  ### only invalid texts needed?
        return False
    if is_int(iter) == 1:
        print("Invalid maximum iteration!")
        return False
    elif is_int(iter) == 2:
        print("Non numeric maximum iteration!")  ### only invalid texts needed?
        return False
    return True

def check_range_validity(k, iter, N):
    if k <= 1 or k >= N:
        print("Invalid number of clusters!")
        return False
    if iter <= 1 or iter >= 1000:
        print("Invalid maximum iteration!")
        return False
    return True

def get_lines_from_file(input):
    try:
        f = open(input, "r")
        input_lines = [line.strip() for line in f.readlines()]
        input_lines.pop()  # check for last item
        f.close()
        return input_lines
    except:
        print("error in opening file")
        return -1

# n_mat = matrix of all input vectors
def init_n_mat(input_lines):
    res = []
    for line in input_lines:
        res.append([float(num) for num in line.split(",")])
    return res


# k_mat[i] = Cluster
def init_k_mat(n_mat, k):
    k_mat = []
    for i in range(k):
        k_mat.append(Cluster(n_mat[i]))
    return k_mat


# return the cluster index of the closet cluster to x_vector
def find_min_cluster(k_mat, x_vector):
    min_cluster = k_mat[0]
    min_d = distance(x_vector, k_mat[0].centroid)  # maybe k_mat is empty?
    for i in range(1, len(k_mat)):
        curr_d = distance(x_vector, k_mat[i].centroid)
        if curr_d < min_d:
            min_cluster = k_mat[i]
            min_d = curr_d
    return min_cluster


# presumes cluster.size and sum is updated, updates cluster vectors, needs to reset clusters at end
def update_clusters(k_mat):
    for cluster in k_mat:
        cluster.update()


# returns true iff conv is true
def check_conv(k_mat):
    # check k_mat.len = preclust.len
    for cluster in k_mat:
        if distance(cluster.centroid, cluster.prev_centroid) >= EPSILON:
            return False
    return True


def main():
    conv = False
    k = sys.argv[1]
    input = sys.argv[-1]
    iter = sys.argv[2] if len(sys.argv) == 4 else 200
    if not check_numeric_validity(k, iter):
        return -1
    input_lines = get_lines_from_file(input)
    if input_lines == -1:
        return -1
    N = len(input_lines)
    k = int(k)
    iter = int(iter)
    if not check_range_validity(k, iter, N):
        return -1
    n_mat = init_n_mat(input_lines)
    d = len(n_mat[0])  # check for empty n_mat || check d is uniform in n_mat
    k_mat = init_k_mat(n_mat, k)
    iter_count = 1
    while iter_count <= iter and not conv:
        for x_vector in n_mat:
            min_cluster = find_min_cluster(k_mat, x_vector)
            # presumes k_mat is resetted
            min_cluster.add(x_vector)
        update_clusters(k_mat)
        iter_count += 1
        conv = check_conv(k_mat)
    for cluster in k_mat:
        print(cluster)
