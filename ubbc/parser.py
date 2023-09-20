from cmdhelper import wrapper
import re

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def to_dic(data=""):
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

def to_ubb(ubbdic):
    result = "[DhtmlXQ] \n"

    for key, value in ubbdic.items():
        result += f"[{key}]{value}[/{key}]\n"

    result += "[/DhtmlXQ]\n"

    return result

import json
@wrapper.process_parameter("ubbdic", json.loads)
def __to_ubb(ubbdic):
    return to_ubb(ubbdic)


@wrapper.jsonfy_this
@wrapper.process_parameter("data", read_file)
def __to_json(data=""):
    """
    Convert ubb chess text to json
    """

    return to_dic(data)

if __name__ == "__main__":
    wrapper.__name__ = "__main__"
    from clize import run
    run(__to_json, __to_ubb)
