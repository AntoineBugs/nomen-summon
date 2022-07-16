
def get_config(filename):
    with open(filename, 'rt', encoding='utf8') as file:
        lines = file.readlines()
    
    path = mode = ''
    start = lines.index('start\n')
    for i in range(start):
        line = lines[i]
        if line[0] != '#':
            l = line.removesuffix('\n').split(' ')
            if l[0] == 'f':
                path = l[1]
            elif l[0] == 'a':
                is_append = bool(l[1])
                mode = 'at' if is_append else 'wt'
            else:
                print("Can't read line:")
                print(' '.join(l))
    
    start += 1
    names = [tuple(l.removesuffix('\n').split(' ')) for l in lines[start:]]
    
    return path, mode, names