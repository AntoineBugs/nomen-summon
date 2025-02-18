import logging

def get_config(filename):
    """
    Reads a configuration file and extracts the path, mode, and names.
    The configuration file is expected to have the following format:
    - Lines starting with '#' are comments and are ignored.
    - A line with 'f <path>' specifies the file path.
    - A line with 'a <True/False>' specifies whether to append or write to the file.
    - A line with 'start' marks the beginning of the names section.
    - Lines after 'start' contain names in the format 'name1 name2'.
    Args:
        filename (str): The path to the configuration file.
    Returns:
        tuple: A tuple containing:
            - path (str): The file path extracted from the configuration.
            - mode (str): The file mode ('at' for append, 'wt' for write).
            - names (list of tuples): A list of tuples, each containing two names.
    """
    with open(filename, "rt", encoding="utf8") as file:
        lines = file.readlines()

    path = mode = ""
    try:
        start = lines.index("start\n")
    except ValueError:
        raise ValueError("The configuration file is missing the 'start' line.")
    for i in range(start):
        line = lines[i]
        if line and line[0] != "#":
            line_read = line.removesuffix("\n").split(" ")
            if line_read[0] == "f":
                path = line_read[1]
            elif line_read[0] == "a":
                is_append = line_read[1]
                mode = "at" if is_append == "True" else "wt"
            else:
                logging.error("Can't read line: %s", " ".join(line_read))

    names = []
    for l in lines[start:]:
        name_pair = l.removesuffix("\n").split(" ")
        if len(name_pair) != 2:
            raise ValueError(f"Invalid format in names section: {l.strip()}")
        names.append(tuple(name_pair))
    names = [tuple(l.removesuffix("\n").split(" ")) for l in lines[start:]]  # noqa: E741

    return path, mode, names
