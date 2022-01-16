import numpy as np


class LaplaceLDP:

    def __init__(self, sensitivity, epsilon):
        self.sensitivity = sensitivity
        self.epsilon = epsilon

    def noise(self):
        return np.random.laplace(0, self.sensitivity / self.epsilon, 1)

    def laplace_perturb(self, data):
        return data + self.noise()


if __name__ == '__main__':
    data_list = [1., 2., 3.]
    sensitivty = 1
    epsilon = 5
    laplace_ldp = LaplaceLDP(sensitivty, epsilon)
    origin_list = []
    perturbed_list = []
    max_num = int(1e3)
    for idx in range(0, max_num):
        for data in data_list:
            origin_list.append(data)
            perturbed_list.append(laplace_ldp.laplace_perturb(data))

    origin_mean = sum(origin_list)/len(origin_list)
    perturbed_mean = sum(perturbed_list)/len(perturbed_list)
    print("origin_mean:{}  perturbed_mean:{}".format(origin_mean, perturbed_mean))