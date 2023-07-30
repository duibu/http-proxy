from lib.core import common
import platform

def init_all():
    common.init()
    extend_path, extend_list = common.do_path()
    common.set_value("tr0uble_mAker", True)
    common.set_value("os", "windows" if "Windows" in platform.system() else "linux")
    common.set_value("extendinfo_dict", common.get_extendinfo_dict())
    common.set_value("extend_list", common.get_extend_scriptname_list_by_search(extend_path, extend_list))
    common.set_value("current_times", 0)
    common.set_value("success_times", 0)
    common.set_value("success_list", [])
