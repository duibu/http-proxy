from lib.core.settings import BANNER
from lib.core.log import logger
import os, importlib
import platform

def banner():
    print(BANNER)

def init():
    global _global_dict
    _global_dict = {}

def set_value(key, value):
    _global_dict[key] = value

def get_value(key):
    try:
        return _global_dict[key]
    except Exception as e:
        return False

# 递归调用extends目录下文件返回每条extend的绝对路径
def get_dir_files(base_path):           
    file_list = []
    if os.path.isdir(base_path):
        for each_file_or_dir in os.listdir(base_path):
            current_path = os.path.join(base_path, each_file_or_dir)
            # 只加载py形式的extends文件
            if os.path.isfile(current_path) and each_file_or_dir.split('.')[-1] != 'py':        
                continue
            each_path = get_dir_files(current_path)
            for file in each_path:
                file_list.append(file)
    else:
        file_list.append(base_path)
    return file_list


# 传入相对路径返回模块导入路径
def path_to_modolepath(path): 
    if 'Windows' in platform.system():
        path = path.lstrip('\\')
        modole_path = path.replace('\\', '.')
    else:
        path = path.lstrip('/')
        modole_path = path.replace('/', '.')
    modole_path = modole_path.replace('.py', '')
    return modole_path

# 根据路径获取文件名
def get_filename_by_path(path):         
    if 'Windows' in platform.system():
        filename = path.split('\\')[-1]
    else:
        filename = path.split('/')[-1]
    return filename

# 调用此函数获取 /extends 下的全部 extend
def get_extend_modole_list():              
    extend_module_list = []
    current_path = os.path.abspath('.')
    extends_base_path = os.path.join(current_path, 'extends')
    extend_path_list = get_dir_files(extends_base_path)
    for extend_path in extend_path_list:
        extend_path = extend_path.replace(current_path, '')
        extend_modole_path = path_to_modolepath(extend_path)
        try:
            extend_module_list.append(importlib.import_module(extend_modole_path))
        except:
            pass
    return extend_module_list

# 获取extends info字典
def get_extendinfo_dict():              
    extendinfo_dict = {}
    current_path = os.path.abspath('.')
    extends_base_path = os.path.join(current_path, 'extends')
    extends_path_list = get_dir_files(extends_base_path)
    for extend_path in extends_path_list:
        extend_path = extend_path.replace(current_path, '')
        extend_modole_path = path_to_modolepath(extend_path)
        try:
            extend_name = get_filename_by_path(extend_path)
            extend_modole = importlib.import_module(extend_modole_path)
            if extend_modole.inject_headers:
                extendinfo_dict[extend_name] = extend_modole
        except:
            pass
    return extendinfo_dict

# 此函数通过搜索extend文件名调用相应的扩展, 传入extends文件名列表, 返回由extends对象的列表
def get_extend_scriptname_list_by_search(path, search_keys_list):
    search_flag = True if len(search_keys_list) > 0 else False
    extend_scriptname_list = []
    current_path = os.path.abspath('.')
    extends_base_path = os.path.join(current_path, path)
    extend_path_list = get_dir_files(extends_base_path)
    if not search_flag:
        for extend_path in extend_path_list:
            script_name = get_filename_by_path(extend_path.replace(current_path, ''))
            if script_name in get_value("extendinfo_dict").keys():
                logger.info('成功检测到extend文件: {0}'.format(script_name))
                extend_scriptname_list.append(get_filename_by_path(extend_path.replace(current_path, '')))
        if not extend_scriptname_list:
            logger.info('没有添加任何extend文件')
        return extend_scriptname_list
    for search_key in search_keys_list:
        for extend_path in extend_path_list:
            script_name = get_filename_by_path(extend_path.replace(current_path, ''))
            if search_key == script_name and search_flag:
                if script_name in get_value("extendinfo_dict").keys():
                    logger.info('成功检测到extend文件: {0}'.format(script_name))
                    extend_scriptname_list.append(script_name)
                    search_flag = False
                    break
                else:
                    search_flag = True
                    logger.error('加载失败: {0}'.format(search_key))
                    break
        if search_flag:
            logger.warning('未检测到extends文件: {0}'.format(search_key))

        search_flag = True
    return extend_scriptname_list

def do_path(path = ''):
    base_path = "extends"
    if path:
        if "\\" in path or "/" in path:
            if 'Windows' in platform.system():
                path = path.replace("/", "\\")
            else:
                path = path.replace('\\', "/")
            if path[0] == "/":
                path = path.lstrip("/")
            return path, []
        else:
            return base_path, path.split(',')
    else:
        return base_path, []

def file_is_exits(path):
    return os.path.exists(path) and os.path.isfile(path)