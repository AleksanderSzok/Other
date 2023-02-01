import xml.etree.ElementTree as ET
from typing import Union


d = {
    "a": {
        "aa": [{"aaa": 1}, [1, 2]],
        "ab": 2,
    },
    "b": 3,
}


# change inner functions to not return None
def json_to_xml(json: dict) -> ET.Element:
    root = ET.Element("root")

    def add_node(
        tmp_root: ET.Element, element: Union[dict, list, str], xml_node_name: str
    ) -> None:
        tmp = ET.SubElement(tmp_root, xml_node_name)
        if isinstance(element, dict):
            to_xml(tmp, element)
        elif isinstance(element, list):
            to_xml(tmp, element, from_list=True)
        else:
            tmp.text = str(element)

    def to_xml(
        tmp_root: ET.Element, tmp_json: Union[dict, list], from_list: bool = False
    ) -> None:
        if from_list is True:
            for element in tmp_json:
                add_node(tmp_root, element, "element")
        else:
            for key in tmp_json:
                add_node(tmp_root, tmp_json[key], key)

    to_xml(root, json)
    return root


json_to_xml(d)
