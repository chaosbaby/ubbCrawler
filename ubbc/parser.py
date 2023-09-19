from cmdhelper import wrapper
import re

def read_file(file_path):
    with open(file_path, "r", encoding="GBK") as file:
        content = file.read()
    return content


@wrapper.jsonfy_this
@wrapper.process_parameter("data", read_file)
def convert_to_json(data=""):
    """TODO: Docstring for convert_to_json.
    :param data: datastring
    :returns: json format data
    """
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


if __name__ == "__main__":
    wrapper.__name__ = "__main__"
    from clize import run

    run(convert_to_json)
