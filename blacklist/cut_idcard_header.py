# coding=utf-8

with open('idcard_heard_1_6', 'r') as f:
    for line in f:
        for i in range(10):
            if line.startswith(str(i)):
                with open('idcard' + str(i) + '.txt', 'a') as f:
                    f.write(line)

