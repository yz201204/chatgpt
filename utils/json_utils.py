import re
import jsonpath
from utils.Log import logger


def get_json_value(values, key, *, print_error=True):
    # 支持jsonpath，并兼容自研取值表达式
    if '$' in key:
        # jsonpath取值
        value = jsonpath.jsonpath(values, key)[0]
        return value
    elif '@' in key:
        # 通过同级其他key对应的value辅助定位要找的key的value
        if not re.search(r'^@(\w+)\[(\w+)=([^,\'\"]+)(?:,(\w+)=([^,\'\"])+)*\]$', key):
            if print_error:
                logger.error('参数依赖表达式格式不规范，表达式为【' + key + '】')
                return None
            else:
                pass
        target_key = re.findall(r'^@(\w+)', key)[0]
        args = re.findall(r'(\w+)=([^,\'\"]+)', key[:-1])
        value = get_value_with_assist_key(values, target_key, args)
        if value is None:
            if print_error:
                logger.error('接口返回值中没有找到符合参数表达式的参数，表达式为【' + key + '】，接口返回值为' + str(values))
            else:
                pass
        else:
            logger.info('接口返回值中，表达式【' + key + '】对应的实际返回值为' + str(value))
        return value
    else:
        logger.info('get_json_value方法没有values传入')


def get_value_with_assist_key(data, target_key, args):
    """
    通过同级其他key对应的value，辅助定位依赖的目标key的value
    :param data: 接口返回值，dict
    :param target_key: 目标key
    :param args: 目标key同级的其他key和对应的value,格式 [(key1,value1),(key2,value2),...]
    :return: 目标key对应的value，data中找不到目标key或辅助定位的key，则返回None
    """
    if not isinstance(data, dict):
        if isinstance(data, list):
            flag = True
            for d in data:
                if not isinstance(d, dict):
                    flag = False
                    break
            if flag:
                data = {"data": data}
        else:
            return None
    if target_key in data:
        for arg in args:
            if arg[0] not in data:
                break
        else:
            for arg in args:
                if str(data[arg[0]]) != arg[1]:
                    break
            else:
                return str(data[target_key])
    # 如果这一层级的key不包含目标key，则在这一层级的value中寻找目标key
    for v in data.values():
        # 如果这一层级的value是个list，则将数组的每一个元素作为新的data，递归
        if isinstance(v, list):
            for element in v:
                result = get_value_with_assist_key(element, target_key, args)
                if result is not None:
                    return result
        if isinstance(v, dict):
            result = get_value_with_assist_key(v, target_key, args)
            if result is not None:
                return result
    return None
