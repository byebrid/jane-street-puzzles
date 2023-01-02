# Lesses More notes

- Decided to code up $f(a, b, c, d)$ since it sounded very easy.
- Turns out it was, just using a recursive solution. Could rewrite it as a while loop if I wanted to make it slightly more performant, as well as use numpy arrays instead of indivdually calculating each corner's value, but it really doesn't matter in this case.
- What does matter is the fact that there are a stupidly large number of permutations of corner values up to 10,000,000. There are some tricks we could use to reduce this sample space (e.g. note that *cyclic* permutations will have equivalent output), but I am sure there will be a nice trick for solving this problem. I doubt this is meant to be a matter of just letting my computer run for a couple of days lol.


## Example: Upper bound of 100
- Once I coded the function, I wanted to solve the problem for a much smaller upper bound of 100. 
- I just brute-forced every permutation, so there are duplicates in my final answer.
- The maximum of $f$ in this domain was 14.
- I didn't keep track of time, but I think it took a couple of minutes. This is very obviously infeasible then for the actual upper bound of 10,000,000!
- I decided to discard cyclic permutations after the fact. All of the solutions that gave an output of 14 are below.
- Then also found which of these final possible solutions led to the *minimum* sum. This turned out to be a sum of **71** with the corners $(0, 44, 20, 7)$ 
- Interestingly, this was the very first of the list of solutions below. This makes sense since I did the algorithm in ascending order of corner values (clearly later answers like $56, 100, 93, 80$ are way too large to be considered), but this does make it seem that we could use some sort of greedy algorithm to further reduce the sample space we need to check.
- However, I believe we would still need to know the maximum of $f$ ahead of time to use this fact, so I'm not sure it's actually useful.
- Ah, not only do we need to ignore cyclic permutations, we also need to ignore *symmetric* permutations. E.g. $(0, 1, 4, 9)$ will give the exact same result as $(9, 4, 1, 0)$!

```
[(0, 7, 20, 44), (0, 10, 29, 64), (0, 12, 34, 75), (0, 13, 37, 81), (0, 13, 38, 84), (0, 14, 40, 88), (0, 15, 43, 95), (0, 24, 37, 44), (0, 35, 54, 64), (0, 41, 63, 75), (0, 44, 20, 7), (0, 44, 37, 24), (0, 44, 68, 81), (0, 46, 71, 84), (0, 48, 74, 88), (0, 52, 80, 95), (0, 64, 29, 10), (0, 64, 54, 35), (0, 75, 34, 12), (0, 75, 63, 41), (0, 81, 37, 13), (0, 81, 68, 44), (0, 84, 38, 13), (0, 84, 71, 46), (0, 88, 40, 14), (0, 88, 74, 48), (0, 95, 43, 15), (0, 95, 80, 52), (1, 8, 21, 45), (1, 11, 30, 65), (1, 13, 35, 76), (1, 14, 38, 82), (1, 14, 39, 85), (1, 15, 41, 89), (1, 16, 44, 96), (1, 25, 38, 45), (1, 36, 55, 65), (1, 42, 64, 76), (1, 45, 21, 8), (1, 45, 38, 25), (1, 45, 69, 82), (1, 47, 72, 85), (1, 49, 75, 89), (1, 53, 81, 96), (1, 65, 30, 11), (1, 65, 55, 36), (1, 76, 35, 13), (1, 76, 64, 42), (1, 82, 38, 14), (1, 82, 69, 45), (1, 85, 39, 14), (1, 85, 72, 47), (1, 89, 41, 15), (1, 89, 75, 49), (1, 96, 44, 16), (1, 96, 81, 53), (2, 9, 22, 46), (2, 12, 31, 66), (2, 14, 36, 77), (2, 15, 39, 83), (2, 15, 40, 86), (2, 16, 42, 90), (2, 17, 45, 97), (2, 26, 39, 46), (2, 37, 56, 66), (2, 43, 65, 77), (2, 46, 22, 9), (2, 46, 39, 26), (2, 46, 70, 83), (2, 48, 73, 86), (2, 50, 76, 90), (2, 54, 82, 97), (2, 66, 31, 12), (2, 66, 56, 37), (2, 77, 36, 14), (2, 77, 65, 43), (2, 83, 39, 15), (2, 83, 70, 46), (2, 86, 40, 15), (2, 86, 73, 48), (2, 90, 42, 16), (2, 90, 76, 50), (2, 97, 45, 17), (2, 97, 82, 54), (3, 10, 23, 47), (3, 13, 32, 67), (3, 15, 37, 78), (3, 16, 40, 84), (3, 16, 41, 87), (3, 17, 43, 91), (3, 18, 46, 98), (3, 27, 40, 47), (3, 38, 57, 67), (3, 44, 66, 78), (3, 47, 23, 10), (3, 47, 40, 27), (3, 47, 71, 84), (3, 49, 74, 87), (3, 51, 77, 91), (3, 55, 83, 98), (3, 67, 32, 13), (3, 67, 57, 38), (3, 78, 37, 15), (3, 78, 66, 44), (3, 84, 40, 16), (3, 84, 71, 47), (3, 87, 41, 16), (3, 87, 74, 49), (3, 91, 43, 17), (3, 91, 77, 51), (3, 98, 46, 18), (3, 98, 83, 55), (4, 11, 24, 48), (4, 14, 33, 68), (4, 16, 38, 79), (4, 17, 41, 85), (4, 17, 42, 88), (4, 18, 44, 92), (4, 19, 47, 99), (4, 28, 41, 48), (4, 39, 58, 68), (4, 45, 67, 79), (4, 48, 24, 11), (4, 48, 41, 28), (4, 48, 72, 85), (4, 50, 75, 88), (4, 52, 78, 92), (4, 56, 84, 99), (4, 68, 33, 14), (4, 68, 58, 39), (4, 79, 38, 16), (4, 79, 67, 45), (4, 85, 41, 17), (4, 85, 72, 48), (4, 88, 42, 17), (4, 88, 75, 50), (4, 92, 44, 18), (4, 92, 78, 52), (4, 99, 47, 19), (4, 99, 84, 56), (5, 12, 25, 49), (5, 15, 34, 69), (5, 17, 39, 80), (5, 18, 42, 86), (5, 18, 43, 89), (5, 19, 45, 93), (5, 20, 48, 100), (5, 29, 42, 49), (5, 40, 59, 69), (5, 46, 68, 80), (5, 49, 25, 12), (5, 49, 42, 29), (5, 49, 73, 86), (5, 51, 76, 89), (5, 53, 79, 93), (5, 57, 85, 100), (5, 69, 34, 15), (5, 69, 59, 40), (5, 80, 39, 17), (5, 80, 68, 46), (5, 86, 42, 18), (5, 86, 73, 49), (5, 89, 43, 18), (5, 89, 76, 51), (5, 93, 45, 19), (5, 93, 79, 53), (5, 100, 48, 20), (5, 100, 85, 57), (6, 13, 26, 50), (6, 16, 35, 70), (6, 18, 40, 81), (6, 19, 43, 87), (6, 19, 44, 90), (6, 20, 46, 94), (6, 30, 43, 50), (6, 41, 60, 70), (6, 47, 69, 81), (6, 50, 26, 13), (6, 50, 43, 30), (6, 50, 74, 87), (6, 52, 77, 90), (6, 54, 80, 94), (6, 70, 35, 16), (6, 70, 60, 41), (6, 81, 40, 18), (6, 81, 69, 47), (6, 87, 43, 19), (6, 87, 74, 50), (6, 90, 44, 19), (6, 90, 77, 52), (6, 94, 46, 20), (6, 94, 80, 54), (7, 14, 27, 51), (7, 17, 36, 71), (7, 19, 41, 82), (7, 20, 44, 88), (7, 20, 45, 91), (7, 21, 47, 95), (7, 31, 44, 51), (7, 42, 61, 71), (7, 48, 70, 82), (7, 51, 27, 14), (7, 51, 44, 31), (7, 51, 75, 88), (7, 53, 78, 91), (7, 55, 81, 95), (7, 71, 36, 17), (7, 71, 61, 42), (7, 82, 41, 19), (7, 82, 70, 48), (7, 88, 44, 20), (7, 88, 75, 51), (7, 91, 45, 20), (7, 91, 78, 53), (7, 95, 47, 21), (7, 95, 81, 55), (8, 15, 28, 52), (8, 18, 37, 72), (8, 20, 42, 83), (8, 21, 45, 89), (8, 21, 46, 92), (8, 22, 48, 96), (8, 32, 45, 52), (8, 43, 62, 72), (8, 49, 71, 83), (8, 52, 28, 15), (8, 52, 45, 32), (8, 52, 76, 89), (8, 54, 79, 92), (8, 56, 82, 96), (8, 72, 37, 18), (8, 72, 62, 43), (8, 83, 42, 20), (8, 83, 71, 49), (8, 89, 45, 21), (8, 89, 76, 52), (8, 92, 46, 21), (8, 92, 79, 54), (8, 96, 48, 22), (8, 96, 82, 56), (9, 16, 29, 53), (9, 19, 38, 73), (9, 21, 43, 84), (9, 22, 46, 90), (9, 22, 47, 93), (9, 23, 49, 97), (9, 33, 46, 53), (9, 44, 63, 73), (9, 50, 72, 84), (9, 53, 29, 16), (9, 53, 46, 33), (9, 53, 77, 90), (9, 55, 80, 93), (9, 57, 83, 97), (9, 73, 38, 19), (9, 73, 63, 44), (9, 84, 43, 21), (9, 84, 72, 50), (9, 90, 46, 22), (9, 90, 77, 53), (9, 93, 47, 22), (9, 93, 80, 55), (9, 97, 49, 23), (9, 97, 83, 57), (10, 17, 30, 54), (10, 20, 39, 74), (10, 22, 44, 85), (10, 23, 47, 91), (10, 23, 48, 94), (10, 24, 50, 98), (10, 34, 47, 54), (10, 45, 64, 74), (10, 51, 73, 85), (10, 54, 30, 17), (10, 54, 47, 34), (10, 54, 78, 91), (10, 56, 81, 94), (10, 58, 84, 98), (10, 74, 39, 20), (10, 74, 64, 45), (10, 85, 44, 22), (10, 85, 73, 51), (10, 91, 47, 23), (10, 91, 78, 54), (10, 94, 48, 23), (10, 94, 81, 56), (10, 98, 50, 24), (10, 98, 84, 58), (11, 18, 31, 55), (11, 21, 40, 75), (11, 23, 45, 86), (11, 24, 48, 92), (11, 24, 49, 95), (11, 25, 51, 99), (11, 35, 48, 55), (11, 46, 65, 75), (11, 52, 74, 86), (11, 55, 31, 18), (11, 55, 48, 35), (11, 55, 79, 92), (11, 57, 82, 95), (11, 59, 85, 99), (11, 75, 40, 21), (11, 75, 65, 46), (11, 86, 45, 23), (11, 86, 74, 52), (11, 92, 48, 24), (11, 92, 79, 55), (11, 95, 49, 24), (11, 95, 82, 57), (11, 99, 51, 25), (11, 99, 85, 59), (12, 19, 32, 56), (12, 22, 41, 76), (12, 24, 46, 87), (12, 25, 49, 93), (12, 25, 50, 96), (12, 26, 52, 100), (12, 36, 49, 56), (12, 47, 66, 76), (12, 53, 75, 87), (12, 56, 32, 19), (12, 56, 49, 36), (12, 56, 80, 93), (12, 58, 83, 96), (12, 60, 86, 100), (12, 76, 41, 22), (12, 76, 66, 47), (12, 87, 46, 24), (12, 87, 75, 53), (12, 93, 49, 25), (12, 93, 80, 56), (12, 96, 50, 25), (12, 96, 83, 58), (12, 100, 52, 26), (12, 100, 86, 60), (13, 20, 33, 57), (13, 23, 42, 77), (13, 25, 47, 88), (13, 26, 50, 94), (13, 26, 51, 97), (13, 37, 50, 57), (13, 48, 67, 77), (13, 54, 76, 88), (13, 57, 33, 20), (13, 57, 50, 37), (13, 57, 81, 94), (13, 59, 84, 97), (13, 77, 42, 23), (13, 77, 67, 48), (13, 88, 47, 25), (13, 88, 76, 54), (13, 94, 50, 26), (13, 94, 81, 57), (13, 97, 51, 26), (13, 97, 84, 59), (14, 21, 34, 58), (14, 24, 43, 78), (14, 26, 48, 89), (14, 27, 51, 95), (14, 27, 52, 98), (14, 38, 51, 58), (14, 49, 68, 78), (14, 55, 77, 89), (14, 58, 34, 21), (14, 58, 51, 38), (14, 58, 82, 95), (14, 60, 85, 98), (14, 78, 43, 24), (14, 78, 68, 49), (14, 89, 48, 26), (14, 89, 77, 55), (14, 95, 51, 27), (14, 95, 82, 58), (14, 98, 52, 27), (14, 98, 85, 60), (15, 22, 35, 59), (15, 25, 44, 79), (15, 27, 49, 90), (15, 28, 52, 96), (15, 28, 53, 99), (15, 39, 52, 59), (15, 50, 69, 79), (15, 56, 78, 90), (15, 59, 35, 22), (15, 59, 52, 39), (15, 59, 83, 96), (15, 61, 86, 99), (15, 79, 44, 25), (15, 79, 69, 50), (15, 90, 49, 27), (15, 90, 78, 56), (15, 96, 52, 28), (15, 96, 83, 59), (15, 99, 53, 28), (15, 99, 86, 61), (16, 23, 36, 60), (16, 26, 45, 80), (16, 28, 50, 91), (16, 29, 53, 97), (16, 29, 54, 100), (16, 40, 53, 60), (16, 51, 70, 80), (16, 57, 79, 91), (16, 60, 36, 23), (16, 60, 53, 40), (16, 60, 84, 97), (16, 62, 87, 100), (16, 80, 45, 26), (16, 80, 70, 51), (16, 91, 50, 28), (16, 91, 79, 57), (16, 97, 53, 29), (16, 97, 84, 60), (16, 100, 54, 29), (16, 100, 87, 62), (17, 24, 37, 61), (17, 27, 46, 81), (17, 29, 51, 92), (17, 30, 54, 98), (17, 41, 54, 61), (17, 52, 71, 81), (17, 58, 80, 92), (17, 61, 37, 24), (17, 61, 54, 41), (17, 61, 85, 98), (17, 81, 46, 27), (17, 81, 71, 52), (17, 92, 51, 29), (17, 92, 80, 58), (17, 98, 54, 30), (17, 98, 85, 61), (18, 25, 38, 62), (18, 28, 47, 82), (18, 30, 52, 93), (18, 31, 55, 99), (18, 42, 55, 62), (18, 53, 72, 82), (18, 59, 81, 93), (18, 62, 38, 25), (18, 62, 55, 42), (18, 62, 86, 99), (18, 82, 47, 28), (18, 82, 72, 53), (18, 93, 52, 30), (18, 93, 81, 59), (18, 99, 55, 31), (18, 99, 86, 62), (19, 26, 39, 63), (19, 29, 48, 83), (19, 31, 53, 94), (19, 32, 56, 100), (19, 43, 56, 63), (19, 54, 73, 83), (19, 60, 82, 94), (19, 63, 39, 26), (19, 63, 56, 43), (19, 63, 87, 100), (19, 83, 48, 29), (19, 83, 73, 54), (19, 94, 53, 31), (19, 94, 82, 60), (19, 100, 56, 32), (19, 100, 87, 63), (20, 27, 40, 64), (20, 30, 49, 84), (20, 32, 54, 95), (20, 44, 57, 64), (20, 55, 74, 84), (20, 61, 83, 95), (20, 64, 40, 27), (20, 64, 57, 44), (20, 84, 49, 30), (20, 84, 74, 55), (20, 95, 54, 32), (20, 95, 83, 61), (21, 28, 41, 65), (21, 31, 50, 85), (21, 33, 55, 96), (21, 45, 58, 65), (21, 56, 75, 85), (21, 62, 84, 96), (21, 65, 41, 28), (21, 65, 58, 45), (21, 85, 50, 31), (21, 85, 75, 56), (21, 96, 55, 33), (21, 96, 84, 62), (22, 29, 42, 66), (22, 32, 51, 86), (22, 34, 56, 97), (22, 46, 59, 66), (22, 57, 76, 86), (22, 63, 85, 97), (22, 66, 42, 29), (22, 66, 59, 46), (22, 86, 51, 32), (22, 86, 76, 57), (22, 97, 56, 34), (22, 97, 85, 63), (23, 30, 43, 67), (23, 33, 52, 87), (23, 35, 57, 98), (23, 47, 60, 67), (23, 58, 77, 87), (23, 64, 86, 98), (23, 67, 43, 30), (23, 67, 60, 47), (23, 87, 52, 33), (23, 87, 77, 58), (23, 98, 57, 35), (23, 98, 86, 64), (24, 31, 44, 68), (24, 34, 53, 88), (24, 36, 58, 99), (24, 48, 61, 68), (24, 59, 78, 88), (24, 65, 87, 99), (24, 68, 44, 31), (24, 68, 61, 48), (24, 88, 53, 34), (24, 88, 78, 59), (24, 99, 58, 36), (24, 99, 87, 65), (25, 32, 45, 69), (25, 35, 54, 89), (25, 37, 59, 100), (25, 49, 62, 69), (25, 60, 79, 89), (25, 66, 88, 100), (25, 69, 45, 32), (25, 69, 62, 49), (25, 89, 54, 35), (25, 89, 79, 60), (25, 100, 59, 37), (25, 100, 88, 66), (26, 33, 46, 70), (26, 36, 55, 90), (26, 50, 63, 70), (26, 61, 80, 90), (26, 70, 46, 33), (26, 70, 63, 50), (26, 90, 55, 36), (26, 90, 80, 61), (27, 34, 47, 71), (27, 37, 56, 91), (27, 51, 64, 71), (27, 62, 81, 91), (27, 71, 47, 34), (27, 71, 64, 51), (27, 91, 56, 37), (27, 91, 81, 62), (28, 35, 48, 72), (28, 38, 57, 92), (28, 52, 65, 72), (28, 63, 82, 92), (28, 72, 48, 35), (28, 72, 65, 52), (28, 92, 57, 38), (28, 92, 82, 63), (29, 36, 49, 73), (29, 39, 58, 93), (29, 53, 66, 73), (29, 64, 83, 93), (29, 73, 49, 36), (29, 73, 66, 53), (29, 93, 58, 39), (29, 93, 83, 64), (30, 37, 50, 74), (30, 40, 59, 94), (30, 54, 67, 74), (30, 65, 84, 94), (30, 74, 50, 37), (30, 74, 67, 54), (30, 94, 59, 40), (30, 94, 84, 65), (31, 38, 51, 75), (31, 41, 60, 95), (31, 55, 68, 75), (31, 66, 85, 95), (31, 75, 51, 38), (31, 75, 68, 55), (31, 95, 60, 41), (31, 95, 85, 66), (32, 39, 52, 76), (32, 42, 61, 96), (32, 56, 69, 76), (32, 67, 86, 96), (32, 76, 52, 39), (32, 76, 69, 56), (32, 96, 61, 42), (32, 96, 86, 67), (33, 40, 53, 77), (33, 43, 62, 97), (33, 57, 70, 77), (33, 68, 87, 97), (33, 77, 53, 40), (33, 77, 70, 57), (33, 97, 62, 43), (33, 97, 87, 68), (34, 41, 54, 78), (34, 44, 63, 98), (34, 58, 71, 78), (34, 69, 88, 98), (34, 78, 54, 41), (34, 78, 71, 58), (34, 98, 63, 44), (34, 98, 88, 69), (35, 42, 55, 79), (35, 45, 64, 99), (35, 59, 72, 79), (35, 70, 89, 99), (35, 79, 55, 42), (35, 79, 72, 59), (35, 99, 64, 45), (35, 99, 89, 70), (36, 43, 56, 80), (36, 46, 65, 100), (36, 60, 73, 80), (36, 71, 90, 100), (36, 80, 56, 43), (36, 80, 73, 60), (36, 100, 65, 46), (36, 100, 90, 71), (37, 44, 57, 81), (37, 61, 74, 81), (37, 81, 57, 44), (37, 81, 74, 61), (38, 45, 58, 82), (38, 62, 75, 82), (38, 82, 58, 45), (38, 82, 75, 62), (39, 46, 59, 83), (39, 63, 76, 83), (39, 83, 59, 46), (39, 83, 76, 63), (40, 47, 60, 84), (40, 64, 77, 84), (40, 84, 60, 47), (40, 84, 77, 64), (41, 48, 61, 85), (41, 65, 78, 85), (41, 85, 61, 48), (41, 85, 78, 65), (42, 49, 62, 86), (42, 66, 79, 86), (42, 86, 62, 49), (42, 86, 79, 66), (43, 50, 63, 87), (43, 67, 80, 87), (43, 87, 63, 50), (43, 87, 80, 67), (44, 51, 64, 88), (44, 68, 81, 88), (44, 88, 64, 51), (44, 88, 81, 68), (45, 52, 65, 89), (45, 69, 82, 89), (45, 89, 65, 52), (45, 89, 82, 69), (46, 53, 66, 90), (46, 70, 83, 90), (46, 90, 66, 53), (46, 90, 83, 70), (47, 54, 67, 91), (47, 71, 84, 91), (47, 91, 67, 54), (47, 91, 84, 71), (48, 55, 68, 92), (48, 72, 85, 92), (48, 92, 68, 55), (48, 92, 85, 72), (49, 56, 69, 93), (49, 73, 86, 93), (49, 93, 69, 56), (49, 93, 86, 73), (50, 57, 70, 94), (50, 74, 87, 94), (50, 94, 70, 57), (50, 94, 87, 74), (51, 58, 71, 95), (51, 75, 88, 95), (51, 95, 71, 58), (51, 95, 88, 75), (52, 59, 72, 96), (52, 76, 89, 96), (52, 96, 72, 59), (52, 96, 89, 76), (53, 60, 73, 97), (53, 77, 90, 97), (53, 97, 73, 60), (53, 97, 90, 77), (54, 61, 74, 98), (54, 78, 91, 98), (54, 98, 74, 61), (54, 98, 91, 78), (55, 62, 75, 99), (55, 79, 92, 99), (55, 99, 75, 62), (55, 99, 92, 79), (56, 63, 76, 100), (56, 80, 93, 100), (56, 100, 76, 63), (56, 100, 93, 80)]
```

## Example: Upper bound of 10
- Maximum of $f$ was 9.
- Minimum sum was $14$, using corners $(0, 1, 4, 9)$
  - Those are all square values? I don't know if that's important or not.
  - Absolute difference is tangentially related to squares (it's equivalent to square-rooting the squared difference), but don't think that's relevant here?


## Example: upper bounds from 0 to 39
- Noticing some patterns.
- At least for these smaller upper bounds, we always have at least one zero. This make sense since 0 gives you the maximal absolute difference when paired with any other integer.
- Also note that solutions are often identical for some number of consecutive upper bounds. E.g. $(0, 2, 6, 13)$ is the solution for an upper bound of 14 all the way up to 31!
- When we increase the upper bound by one, if we still have the same solution, then we always find a further **2** candidates that give the maximal value of $f$. However, these extra candidates are obviously invalid because their sum is larger than the first solution we find.
- I will note that I reckon I could probably enter one of the sequences I'm finding (e.g. the thresholds for when the solution changes, $1, 2, 4, 5, 10, 13, \ldots$, or more likely the sequence of minimum sums we get) into the OEIS, but that feels like cheating so I won't do it. Want to discover the pattern for myself.

```
Found 0 unique candidates that yield a maximum $f$ of 0. Finding minimum sum of corners now...
Upper bound of    0: min sum = 0: None

Found 1 unique candidates that yield a maximum $f$ of 1. Finding minimum sum of corners now...
Upper bound of    1: min sum = 0: (0, 0, 0, 0)

Found 2 unique candidates that yield a maximum $f$ of 5. Finding minimum sum of corners now...
Upper bound of    2: min sum = 1: (0, 0, 0, 1)

Found 10 unique candidates that yield a maximum $f$ of 5. Finding minimum sum of corners now...
Upper bound of    3: min sum = 1: (0, 0, 0, 1)

Found 2 unique candidates that yield a maximum $f$ of 7. Finding minimum sum of corners now...
Upper bound of    4: min sum = 4: (0, 0, 1, 3)

Found 2 unique candidates that yield a maximum $f$ of 8. Finding minimum sum of corners now...
Upper bound of    5: min sum = 7: (0, 1, 2, 4)

Found 4 unique candidates that yield a maximum $f$ of 8. Finding minimum sum of corners now...
Upper bound of    6: min sum = 7: (0, 1, 2, 4)

Found 8 unique candidates that yield a maximum $f$ of 8. Finding minimum sum of corners now...
Upper bound of    7: min sum = 7: (0, 1, 2, 4)

Found 16 unique candidates that yield a maximum $f$ of 8. Finding minimum sum of corners now...
Upper bound of    8: min sum = 7: (0, 1, 2, 4)

Found 28 unique candidates that yield a maximum $f$ of 8. Finding minimum sum of corners now...
Upper bound of    9: min sum = 7: (0, 1, 2, 4)

Found 2 unique candidates that yield a maximum $f$ of 9. Finding minimum sum of corners now...
Upper bound of   10: min sum = 14: (0, 1, 4, 9)

Found 4 unique candidates that yield a maximum $f$ of 9. Finding minimum sum of corners now...
Upper bound of   11: min sum = 14: (0, 1, 4, 9)

Found 2 unique candidates that yield a maximum $f$ of 10. Finding minimum sum of corners now...
Upper bound of   12: min sum = 18: (0, 2, 5, 11)

Found 4 unique candidates that yield a maximum $f$ of 10. Finding minimum sum of corners now...
Upper bound of   13: min sum = 18: (0, 2, 5, 11)

Found 2 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   14: min sum = 21: (0, 2, 6, 13)

Found 4 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   15: min sum = 21: (0, 2, 6, 13)

Found 6 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   16: min sum = 21: (0, 2, 6, 13)

Found 8 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   17: min sum = 21: (0, 2, 6, 13)

Found 10 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   18: min sum = 21: (0, 2, 6, 13)

Found 12 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   19: min sum = 21: (0, 2, 6, 13)

Found 16 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   20: min sum = 21: (0, 2, 6, 13)

Found 20 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   21: min sum = 21: (0, 2, 6, 13)

Found 24 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   22: min sum = 21: (0, 2, 6, 13)

Found 30 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   23: min sum = 21: (0, 2, 6, 13)

Found 36 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   24: min sum = 21: (0, 2, 6, 13)

Found 44 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   25: min sum = 21: (0, 2, 6, 13)

Found 54 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   26: min sum = 21: (0, 2, 6, 13)

Found 66 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   27: min sum = 21: (0, 2, 6, 13)

Found 78 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   28: min sum = 21: (0, 2, 6, 13)

Found 92 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   29: min sum = 21: (0, 2, 6, 13)

Found 106 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   30: min sum = 21: (0, 2, 6, 13)

Found 122 unique candidates that yield a maximum $f$ of 11. Finding minimum sum of corners now...
Upper bound of   31: min sum = 21: (0, 2, 6, 13)

Found 2 unique candidates that yield a maximum $f$ of 12. Finding minimum sum of corners now...
Upper bound of   32: min sum = 50: (0, 5, 14, 31)

Found 4 unique candidates that yield a maximum $f$ of 12. Finding minimum sum of corners now...
Upper bound of   33: min sum = 50: (0, 5, 14, 31)

Found 6 unique candidates that yield a maximum $f$ of 12. Finding minimum sum of corners now...
Upper bound of   34: min sum = 50: (0, 5, 14, 31)

Found 8 unique candidates that yield a maximum $f$ of 12. Finding minimum sum of corners now...
Upper bound of   35: min sum = 50: (0, 5, 14, 31)

Found 10 unique candidates that yield a maximum $f$ of 12. Finding minimum sum of corners now...
Upper bound of   36: min sum = 50: (0, 5, 14, 31)

Found 12 unique candidates that yield a maximum $f$ of 12. Finding minimum sum of corners now...
Upper bound of   37: min sum = 50: (0, 5, 14, 31)

Found 2 unique candidates that yield a maximum $f$ of 13. Finding minimum sum of corners now...
Upper bound of   38: min sum = 60: (0, 6, 17, 37)

Found 4 unique candidates that yield a maximum $f$ of 13. Finding minimum sum of corners now...
Upper bound of   39: min sum = 60: (0, 6, 17, 37)
```


## Example: Upper bounds of 40-59
```
Found 6 unique candidates that yield a maximum $f$ of 13. Finding minimum sum of corners now...
Upper bound of   40: min sum = 60: (0, 6, 17, 37)    [2.42 seconds]

Found 8 unique candidates that yield a maximum $f$ of 13. Finding minimum sum of corners now...
Upper bound of   41: min sum = 60: (0, 6, 17, 37)    [2.71 seconds]

Found 10 unique candidates that yield a maximum $f$ of 13. Finding minimum sum of corners now...
Upper bound of   42: min sum = 60: (0, 6, 17, 37)    [2.97 seconds]

Found 12 unique candidates that yield a maximum $f$ of 13. Finding minimum sum of corners now...
Upper bound of   43: min sum = 60: (0, 6, 17, 37)    [3.26 seconds]

Found 14 unique candidates that yield a maximum $f$ of 13. Finding minimum sum of corners now...
Upper bound of   44: min sum = 60: (0, 6, 17, 37)    [3.60 seconds]

Found 2 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   45: min sum = 71: (0, 7, 20, 44)    [3.94 seconds]

Found 4 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   46: min sum = 71: (0, 7, 20, 44)    [4.34 seconds]

Found 6 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   47: min sum = 71: (0, 7, 20, 44)    [4.76 seconds]

Found 8 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   48: min sum = 71: (0, 7, 20, 44)    [5.24 seconds]

Found 10 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   49: min sum = 71: (0, 7, 20, 44)    [5.69 seconds]

Found 12 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   50: min sum = 71: (0, 7, 20, 44)    [6.14 seconds]

Found 14 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   51: min sum = 71: (0, 7, 20, 44)    [6.67 seconds]

Found 16 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   52: min sum = 71: (0, 7, 20, 44)    [7.26 seconds]

Found 18 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   53: min sum = 71: (0, 7, 20, 44)    [7.89 seconds]

Found 20 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   54: min sum = 71: (0, 7, 20, 44)    [8.49 seconds]

Found 22 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   55: min sum = 71: (0, 7, 20, 44)    [9.25 seconds]

Found 24 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   56: min sum = 71: (0, 7, 20, 44)    [9.89 seconds]

Found 26 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   57: min sum = 71: (0, 7, 20, 44)    [10.61 seconds]

Found 28 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   58: min sum = 71: (0, 7, 20, 44)    [11.30 seconds]

Found 30 unique candidates that yield a maximum $f$ of 14. Finding minimum sum of corners now...
Upper bound of   59: min sum = 71: (0, 7, 20, 44)    [12.19 seconds]
```


## Example: 40-44 with all candidates included
- Decided to print out all unique *candidates* before I find the one with the minimal sum.
- Wanted to examine that pattern of the number of candidates increasing by 2 each time a solution was repeated.
- I understand it now. The extra 2 solutions is coming from the fact that adding the *same* constant to each corner value yields an identical set of corners for the next iteration.
  - E.g. starting from $(0, 6, 17, 37)$, you can simply add 1 to each corner to get $(1, 7, 18, 38)$, which will yield the exact same set of subsequent corners. All of the differences between corners are preserved, but this obviously increases the sum (by $4 \times \text{constant}$), which is why these extra candidates are always useless.
- The reason it's incrementing by *2* each time must be because we have 2 distinct solutions to start with. Not sure why that seems to be the case every time though! This may just be true for these smaller upper bounds, and might change for much larger values.
- In fact, yeah. Checking all of our solutions so far, they all follow that pattern of *starting with 2 candidates*, and then increasing by 2 at each step (by our logic above). That's very curious to me.
  - Ah, checked upper bound of 40 as example. This starts with the 2 solutions $(0, 6, 17, 37), (0, 20, 31, 37)$ which then lead to the corners of $(6,11,20,37), (20, 11, 6, 37)$. We can see the next set of corners are clearly equivalent, so I've simply missed this scenario when I check for unique solutions. Though the starting corner values themselves are different, so I'm going to leave this as is for the moment.
    - Just out of curiosity, what if I subtract 6 from all of those corners in $(6,11,20,37)$? I'm thinking this might give a solution for a smaller upper bound, since this is all feels very recursive.
    - We get $(0, 5, 14, 31)$.
    - Aha! This is the solution that comes just before $(0, 6, 17, 37)$. The solution switch happens when the upper bound goes from 37 to 38.