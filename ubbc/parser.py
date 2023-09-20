from cmdhelper import wrapper
import re

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def convert_to_dic(data=""):
    lines = data.strip()

    # Create a dictionary to hold the data
    data_dict = {}
    # pattern = r"\[(.*?)\](.*?)\[/\1\]"
    pattern = r"\[([^]]+)\]([^\[]+?)\[/\1\]"
    matches = re.findall(pattern, lines)
    for match in matches:
        key = match[0]
        value = match[1]
        if not "DhtmlXQ_comment" in key:
            data_dict[key] = value
    ids = re.findall(r"id=(\d+)", data)
    if ids:
        data_dict["id"] = ids[0]
    return data_dict

@wrapper.jsonfy_this
@wrapper.process_parameter("data", read_file)
def __convert_to_json(data=""):
    """
    Convert ubb chess text to json
    """

    return convert_to_dic(data)

if __name__ == "__main__":
    wrapper.__name__ = "__main__"
    from clize import run
    run(__convert_to_json)
