import re
import chardet


class DecodingUtil(object):
    """解码工具类"""
    @staticmethod
    def decode(content):
        """
        读取字节数据判断其编码，并正确解码
        :param content: 传入的字节数据
        :return: 正确解码后的数据
        """
        # print(chardet.detect(content))
        the_encoding = chardet.detect(content)['encoding']
        try:
            return content.decode(the_encoding)
        except UnicodeDecodeError:
            print('解码Error!')
            try:
                return content.decode('utf-8')
            except:
                return '未能成功解码的文章内容！'


def rep_invalid_char(old:str):
    """mysql插入操作时，有无效字符，替换"""
    invalid_char_re = r"[/?\\[\]*:]"
    return re.sub(invalid_char_re, "_", old)


