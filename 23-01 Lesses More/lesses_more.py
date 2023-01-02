from itertools import product
from time import time

def find_min_sum_max_f(upper_bound: int, print_answers: bool = False):
    start = time()
    
    def f(a, b, c, d):
        steps = 0
        while (a, b, c, d) != (0, 0, 0, 0):
            w = abs(a - b)
            x = abs(b - c)
            y = abs(c - d)
            z = abs(d - a)
            a, b, c, d = w, x, y, z
            steps += 1
        
        # Increment to include the final (0, 0, 0, 0) state
        steps += 1
        return steps

        # w = abs(a - b)
        # x = abs(b - c)
        # y = abs(c - d)
        # z = abs(d - a)
        # return 1 + f(w, x, y, z)


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


for upper_bound in range(1, 91):
    find_min_sum_max_f(upper_bound, print_answers=False)
    print()