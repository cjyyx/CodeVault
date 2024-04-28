from fake_useragent import UserAgent
def ranheaders():
    '''随机产生含有User-Agent的请求头'''
    headers={
        'User-Agent':UserAgent().chrome
    }
    return headers

def security_filename(name:str)->str:
    '''移除非法文件名字符'''
    replace_char='''/\:*?"<>|.'''
    for char in replace_char:
        while char in name:
            name=name.replace(char,'')
    return name