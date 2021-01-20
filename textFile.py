def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def unicode_truncate(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')


def write_to_file(file, text):
    with open(file, "a") as f:
        f.write(text + "\n")


def remove_newline(text):
    chars = []
    for i in range(len(text)):
        if not text[i] == "\n":
            chars.append(text[i])
    return "".join(chars)


def read_file(file, remove_line=True):
    with open(file, "r") as f:
        lines = f.readlines()
    new_text_list = []
    if remove_line:
        for line in lines:
            new_text_list.append(remove_newline(line))
        return new_text_list
    else:
        return lines


def separate_arguments(text):
    args = []
    while len(text) > 0:
        try:
            indexOf = text.index(";")
            args.append(text[:indexOf].strip())
            text = text[indexOf + 1:]
            # print(text)
        except ValueError:
            args.append(text.strip())
            break
    args[0] = int(args[0])
    return args


def add_new_user(file, new_user):
    try:
        args = [separate_arguments(i) for i in read_file(file)]
        last_entry = args[len(args) - 1]
        last_index = last_entry[0]
    except IndexError:
        last_index = 0
    actual_index = last_index + 1
    full_entry = str(actual_index) + ";" + new_user
    write_to_file(file, full_entry)


def get_user(file, username, param='username'):
    lines = (read_file(file))
    args = [separate_arguments(i) for i in lines]
    for arg in args:
        for elem in arg:
            if elem == username:
                return tuple(arg)


def get_all_users(file, chat_id):
    full_entry = []
    lines = read_file(file)
    for line in lines:
        args = separate_arguments(line)
        full_entry.append([args[1], args[2]])
    return full_entry


def get_user_id(file, username):
    return get_user(file, username)[0]


def delete_user(file, username):
    print(username)
    lines = read_file(file, False)
    print(username)
    id = get_user_id(file, str(username))
    with open(file, 'w') as f:
        for line in lines:
            if str(id) != line[0]:
                f.write(line)


def create_file(filename):
    with open(str(filename) + ".txt", 'w') as f:
        f.write("")


def get_file(chat_id):
    import os
    files = os.listdir(os.path.abspath(os.getcwd()))
    for filename in files:
        if filename == str(chat_id) + ".txt":
            return filename
    with open(str(chat_id) + ".txt", 'w') as f:
        f.write("")
    return str(chat_id) + ".txt"


def check_if_user_exists(file, userid):
    try:
        get_user_id(file, userid)
        return True
    except TypeError:
        return False


def main(file, raw_text):
    add_new_user(file, raw_text)
