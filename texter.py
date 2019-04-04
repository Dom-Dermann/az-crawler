## module for conveniently writing to files

def array_to_text_file (array, filename):
    if not isinstance(filename, str):
        raise TypeError
    if not isinstance(array, list):
        raise TypeError

    with open (filename, 'w') as f:
        for u in array:
            f.write(f'{u} \n')

def text_file_to_array(filename):
    links = []
    with open(filename, 'r') as lks:
        for link in lks:
            links.append(link)
    return links

def write_to_file(input, filename):
    with open(filename, "w") as f:
        f.write(input)