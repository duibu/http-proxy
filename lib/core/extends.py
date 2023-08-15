from lib.core import common
from lib.core.log import logger

def header(header = {}, data = None):
    script_list = common.get_value("extend_list")
    result = {}
    if script_list:
        try:
            current_script = ''
            for script in script_list:
                current_script = script
                header_dict = common.get_value("extendinfo_dict")[script].inject_headers(header, data)
                if header_dict and isinstance(header_dict, dict):
                    logger.info('[%s]脚本返回的header内容 -> [%s]' % (script, header_dict))
                    result.update(header_dict)
                else:
                    logger.error('[%s]脚本返回的header不是dict类型的数据' % script)
        except Exception as e:
            logger.error('扩展脚本 [%s] 出现错误 -> [%s]' % (current_script, e))
    return result

def data(header = {}, data = None):
    script_list = common.get_value("extend_list")
    return 