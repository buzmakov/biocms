__author__ = 'makov'

import os
import errno
import pytils.translit as translit

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise exc


def load_plan(f_name):
    plan = []
    with open(f_name) as f:
        for l in f.readlines():
            s = l.replace('\n', '').replace('* ', '')
            plan.append(s)
    return plan


def count_tabs(s):
    n = 0
    while s.startswith('\t'):
        n += 1
        s = s[1:]
    return n


def make_paths(plan):
    prev_lvl = 0
    last_dir = ''
    counters = [0]
    dir_stack = []
    for s in plan:
        new_lvl = count_tabs(s)
        if new_lvl > prev_lvl:
            counters.append(0)
            dir_stack.append(last_dir)
        elif new_lvl < prev_lvl:
            for i in range(prev_lvl - new_lvl):
                dir_stack.pop()
                counters.pop()
        counters[-1] += 1
        new_dir = s.decode('utf-8').strip()
        new_dir = u'{0}. {1}{2}'.format(counters[-1],new_dir[0].upper(),new_dir[1:])
        dir_stack.append(new_dir)
        yield '/'.join(dir_stack).encode('utf-8')
        dir_stack.pop()
        prev_lvl = new_lvl
        last_dir = new_dir


if __name__ == '__main__':
    plan = load_plan('plan.md')
    for p in make_paths(plan):
        print 'mkdir -p "' + p + '"'