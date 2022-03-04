import numpy as np

candidates = ['sad', 'happy', 'angry', 'annoyed']


def loop_shift(array, shift):
    return array[shift:] + array[:shift]


hashs = [
    {x: i for i, x in enumerate(candidates)},
    {x: i for i, x in enumerate(loop_shift(candidates, 1))},
    {x: i for i, x in enumerate(loop_shift(candidates, 2))},
    {x: i for i, x in enumerate(loop_shift(candidates, 3))},
]

num_hash_func = len(hashs)
num_hash_output = len(candidates)
epsilon = 5
num_diff = 1000
print("h1:{}  h2:{}".format(loop_shift(candidates,1), loop_shift(candidates, 2)))

def random_flip(x, prob):
    if np.random.uniform(0, 1) < prob:
        return -1 if x == 1 else 1
    return x


def client_cms(num_value, input_data, hash_funcs, epsilon):
    j = np.random.randint(0, num_hash_func)
    v = np.zeros(shape=[num_value], dtype=np.int32)
    prob = 1.0 / (np.exp(epsilon * 0.5) + 1)
    position = hash_funcs[j][input_data]
    v[position] = 1
    for i in range(num_value):
        if i != position:
            v[i] = -1
        v[i] = random_flip(v[i], prob)
    return j, v


def server_cms(j_v_array, hashs, epsilon):
    c_epsilon = (np.exp(epsilon * 0.5) + 1) / (np.exp(epsilon * 0.5) - 1)
    sum_a_s = np.zeros(shape=[num_hash_output], dtype=np.int32)
    res = np.zeros(shape=[num_hash_output], dtype=np.float)
    cnt_1_array = cnt_1(j_v_array, len(j_v_array), num_hash_output, num_hash_func)
    for l in range(num_hash_output):
        for j, v in j_v_array:
            h_j_d = hashs[j][candidates[l]]
            sum_a_s[l] += (v[h_j_d] + 1) / 2
        res[l] = c_epsilon * (sum_a_s[l] - len(j_v_array) * 1 / (np.exp(epsilon * 0.5) + 1))
        print("cnt_1_array[{}]: {} sum_a_s: {}".format(l, cnt_1_array[l], sum_a_s[l]))
    return res


def cnt_1(j_v_array, n, m, k):
    cnt_1_array = [0] * m
    for j, v in j_v_array:
        for d in range(m):
            if v[[hashs[j][candidates[d]]]] == 1:
                cnt_1_array[d] += 1
    return cnt_1_array


j_v_array = [client_cms(num_hash_output, 'sad', hashs, epsilon) for _ in range(num_diff * 4)]
# for j, v in j_v_array:
#     print("j: {}, v: {}".format(j, v))
j_v_array += [client_cms(num_hash_output, 'happy', hashs, epsilon) for _ in range(num_diff * 3)]
j_v_array += [client_cms(num_hash_output, 'angry', hashs, epsilon) for _ in range(num_diff * 2)]
j_v_array += [client_cms(num_hash_output, 'annoyed', hashs, epsilon) for _ in range(num_diff)]

res = server_cms(j_v_array, hashs, epsilon)
print('sad count: {} happy count: {} angry count:{} annoyed count: {}'.format(res[0], res[1], res[2], res[3]))
# print(client_cms(num_hash_func, num_hash_output, 'sad', hashs, 4))
