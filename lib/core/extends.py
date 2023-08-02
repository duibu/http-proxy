from lib.core import common

def header(header = {}, data = None):
    script_list = common.get_value("extend_list")
    result = {}
    if script_list:
        for script in script_list:
            header_dict = common.get_value("extendinfo_dict")[script].inject_headers(header, data)
            if header_dict and isinstance(header_dict, dict):
                result.update(header_dict)
    return result

def data(header = {}, data = None):
    script_list = common.get_value("extend_list")
    return 