import numpy as np

candidates = ['sad', 'happy']

hashs = [
    {x: i for i, x in enumerate(candidates)},
    {x: i + 2 for i, x in enumerate(candidates)},
    {x: i + 4 for i, x in enumerate(candidates)},
]
num_hash_func = 3
num_hash_output = 6


def random_flip(x, prob):
    if np.random.uniform(0, 1) < prob:
        return 0 if x == 1 else 1
    return x


def client_cms(num_hash, num_value, input_data, hash_funcs, epsilon):
    j = np.random.randint(0, len(hash_funcs))
    col = hash_funcs[j][input_data]
    sketch = np.zeros(shape=[num_hash, num_value], dtype=np.int32)
    sketch[j][col] = 1
    for i in range(num_value):
        prob = 1.0 / (np.exp(epsilon * 0.5) + 1)
        sketch[j][i] = random_flip(sketch[j][i], prob)
    return sketch


def server_cms(sketch, input, hashs):
    return sum([sketch[i][hash_func[input]] for i, hash_func in enumerate(hashs)])


sketches = [client_cms(num_hash_func, num_hash_output, 'sad', hashs, 4) for _ in range(1000)]
sketches += [client_cms(num_hash_func, num_hash_output, 'happy', hashs, 4) for _ in range(1000)]

# sketch_tot = sum(sketches)

# print('sad count: {}'.format(server_cms(sketch_tot, 'sad', hashs)))
# print('happy count: {}'.format(server_cms(sketch_tot, 'happy', hashs)))
print(client_cms(num_hash_func, num_hash_output, 'sad', hashs, 4))
