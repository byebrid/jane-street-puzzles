from itertools import product
from time import time
import numpy as np

def f(a, b, c, d):
    steps = 0
    while (a, b, c, d) != (0, 0, 0, 0):
        print(a, b, c, d)
        w = abs(a - b)
        x = abs(b - c)
        y = abs(c - d)
        z = abs(d - a)
        a, b, c, d = w, x, y, z
        steps += 1
    
    # Increment to include the final (0, 0, 0, 0) state
    steps += 1
    return steps

def find_min_sum_max_f(upper_bound: int, print_answers: bool = False):
    start = time()

    total_iterations = (upper_bound) ** 4
    answers = []
    f_max = 0
    for i, (a, b, c, d) in enumerate(product(range(upper_bound), range(upper_bound), range(upper_bound), range(upper_bound))):
        result = f(a, b, c, d)
        if result > f_max:
            f_max = result
            answers = [(a, b, c, d)]
        elif result == f_max:
            answers.append((a, b, c, d))

        # if (i + 1) % (total_iterations // 100) == 0:
        #     print(f"{i + 1}/{total_iterations} ({(i + 1)/total_iterations * 100:.2f}%)")

    # Reduce to only the *unique* solutions
    answers_copy = answers.copy()
    answers = []
    for (a, b, c, d) in answers_copy:
        # Discard cyclic permutations
        if (b, c, d, a) in answers or (c, d, a, b) in answers or (d, a, b, c) in answers:
            continue
        # Discard reflections (and their cyclic permutations)
        if (d, c, b, a) in answers or (c, b, a, d) in answers or (b, a, d, c) in answers or (a, d, c, b) in answers:
            continue

        answers.append((a, b, c, d))

    print(f"Found {len(answers)} unique candidates that yield a maximum $f$ of {f_max}. Finding minimum sum of corners now...")
    if print_answers:
        print(answers)

    min_sum = upper_bound * 4
    min_sol = None
    for answer in answers:
        # if sum(answer) == min_sum:
            # print(f"Found *another* answer that summed to {min_sum}: {answer}")
        if sum(answer) < min_sum:
            min_sum = sum(answer)
            min_sol = answer
            # print(f"Found smaller sum {min_sum}: {answer}")

    end = time()
    duration_seconds = end - start
    print(f"Upper bound of {upper_bound:>4}: min sum = {min_sum}: {min_sol}    [{duration_seconds:.2f} seconds]")


def f2(l):
    # return np.ndarray([
    #     l[1] - l[0],
    #     l[2] - l[1],
    #     l[3] - l[2],
    #     l[0] - l[3]
    # ])

    l_shifted = np.roll(l, shift=-1, axis=0)
    # l[-1] *= -1
    # l_shifted[-1] *= -1
    next_l = l_shifted - l
    next_l[-1] *= -1
    return next_l


if __name__ == "__main__":
    # for upper_bound in range(1, 91):
    #     find_min_sum_max_f(upper_bound, print_answers=False)
    #     print()

    np.set_printoptions(precision=3)
    l = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    start = (0, 7, 20, 44) 
    bcd = np.array(start[1:]).transpose()
    wanted_y = np.array([100, 100, 100]).transpose()
    for i in range(100):
        l = f2(l)
        # print(f"\n{i=}")
        # print(l)
        l_only_positive = l[[0,2,3]]
        required_start = np.linalg.solve(l_only_positive, wanted_y).astype(int)
        if all(np.matmul(l_only_positive, required_start) == wanted_y):
            print(f"YES! {i=}")
            # print(required_start)

        # print(np.matmul(l, bcd))


    # f(*start)