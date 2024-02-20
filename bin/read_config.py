def get_config(filename):
    with open(filename, "rt", encoding="utf8") as file:
        lines = file.readlines()

    path = mode = ""
    start = lines.index("start\n")
    for i in range(start):
        line = lines[i]
        if line[0] != "#":
            line_read = line.removesuffix("\n").split(" ")
            if line_read[0] == "f":
                path = line_read[1]
            elif line_read[0] == "a":
                is_append = line_read[1]
                mode = "at" if is_append == "True" else "wt"
            else:
                print("Can't read line:")
                print(" ".join(line_read))

    start += 1
    names = [tuple(l.removesuffix("\n").split(" ")) for l in lines[start:]]  # noqa: E741

    return path, mode, names
