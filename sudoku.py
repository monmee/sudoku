#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def solve(sudoku):
    candidates = []
    old_candidates = []

    while(True):
        # 候補作成
        for x in range(9):
            candidates_row = []
            for y in range(9):
                if sudoku[x][y] != 0:
                    candidates_row.append([])
                    continue
                boxes = square(sudoku)
                cand = calc_candidate(sudoku, boxes, x, y)
                if len(cand) == 1:
                    sudoku[x][y] = cand[0]
                    candidates_row.append([])
                else:
                    candidates_row.append(cand)
            candidates.append(candidates_row)

        # 行に対して候補から数字を確定
        decide_num_row(sudoku, candidates)
        # 列に対して候補から数字を確定
        sudoku_trans = transpose(sudoku)
        candidates_trans = transpose(candidates)
        decide_num_row(sudoku_trans, candidates_trans)
        sudoku = transpose(sudoku_trans)
        candidates = transpose(candidates_trans)

        if old_candidates == candidates or is_complete(sudoku):
            break

        old_candidates = candidates
        candidates = []
    return sudoku


def transpose(sudoku):
    return list(map(list, zip(*sudoku)))


def square(sudoku):
    boxes = []
    for i in range(3):
        rows = sudoku[i*3:(i+1)*3]
        box_temp= [[], [], []]
        for row in rows:
            for j in range(3):
                box_temp[j].append(row[j*3:(j+1)*3])
        boxes.extend(box_temp)
    return boxes


def is_complete(sudoku):
    for sudoku_row in sudoku:
        if 0 in sudoku_row: return False
    return True


def get_box(boxes, i, j):
    x = int(i / 3)
    y = int(j / 3)
    return boxes[x*3 + y]


def flatten(lst):
    ex = []
    for s in lst:
        ex.extend(s)
    return ex


def calc_candidate(sudoku, boxes, i, j):
    candidate = set([x+1 for x in range(9)])
    row = set(list(filter(lambda num: num != 0, sudoku[i])))
    col = set(list(filter(lambda num: num != 0, transpose(sudoku)[j])))
    box = set(list(filter(lambda num: num != 0, flatten(get_box(boxes, i, j)))))
    return list(candidate - row - col - box)


def decide_num_row(sudoku, candidates):
    for x in range(9):
        sudoku_row = list(filter(lambda num: num != 0, sudoku[x]))
        candidates_row = candidates[x]
        for y in range(9):
            cand = decide_num_by_candidates(sudoku_row, y, candidates_row[:])
            if len(cand) == 1:
                sudoku[x][y] = cand[0]
                candidates[x][y] = []


def decide_num_by_candidates(sudoku_row, j, candidates):
    target_cand = set(candidates[j]) - set(sudoku_row)
    del candidates[j]
    for candidate in candidates:
        target_cand -= set(candidate)
    return list(target_cand)


def print_sudoku(sudoku):
    for row in sudoku:
        sys.stdout.write('|')
        for num in row:
            if num == 0:
                print(' ', end = '')
            else:
                print(num, end = '')
            sys.stdout.write('|')
        print('')
    return


if __name__ == '__main__':
    sudoku1 = transpose([[0, 0, 0, 2, 0, 1, 0, 0, 0],
                         [0, 0, 5, 9, 0, 4, 2, 0, 0],
                         [0, 9, 1, 0, 0, 0, 6, 5, 0],
                         [0, 8, 9, 4, 0, 5, 7, 1, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 5, 7, 1, 0, 8, 9, 3, 0],
                         [0, 1, 4, 0, 0, 0, 5, 6, 0],
                         [0, 0, 2, 6, 0, 9, 8, 0, 0],
                         [0, 0, 0, 5, 0, 3, 0, 0, 0]])

    sudoku3 = transpose([[9, 0, 0, 0, 0, 0, 0, 0, 3],
                         [0, 1, 0, 0, 2, 4, 0, 0, 0],
                         [4, 0, 0, 0, 0, 0, 1, 0, 0],
                         [2, 0, 7, 8, 9, 0, 6, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 6, 0, 4, 2, 7, 0, 5],
                         [0, 0, 5, 0, 0, 0, 0, 0, 7],
                         [0, 0, 0, 9, 6, 0, 0, 3, 0],
                         [7, 0, 0, 0, 0, 0, 0, 0, 2]])
    # print_sudoku(sudoku1)
    # print(square(sudoku1))
    # print(calc_candidate(sudoku1, square(sudoku1), 0, 0))
    # print_sudoku(solve(sudoku1))
    print_sudoku(solve(sudoku3))
