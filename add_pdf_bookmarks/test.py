#coding=utf-8
import re
import os
def get_bookmarks():
    print('工作目录：{}'.format(os.getcwd()))
    current_dir = os.path.dirname(__file__)  # 当前文件所在的目录
    print('当前文件目录：{}'.format(current_dir))
    txt_file = '1.txt'
    bookmarks = {}
    with open(os.path.join(current_dir, txt_file),encoding='utf-8') as fout:
        for line in fout:
            if not line or line.isspace():
                continue
            print(line)
            title = line.split('@')[0].strip()
            page = line.split('@')[1].strip()
            if not title or not page:
                continue
            
            match = re.search(r"(?<=第).*?(?=章)", title)
            if match:
                digit = match.group()
                digit = digit.strip()
                print(digit)
                bookmarks[digit] = {"title":title, "page":page, "sub":{}}
            else:
                serial_num = title.split()[0].strip()
                print(serial_num)
                serials = serial_num.split('.')
                print(serials)
                '''
                从第二个位置开始遍历，到最终要插入的节点
                例如: 0.1.2, 最终找到第三级节点'2'
                '''
                node = bookmarks[serials[0]]
                for serial in serials[1:]:
                    if serial not in node['sub']:
                        # 节点不存在则创建
                        node['sub'][serial] = {}
                    node = node['sub'][serial]
                node['title'] = title
                node['page'] = page
                node['sub'] = {}
    
    print(bookmarks)
    return bookmarks

def print_bookmark(title, page, parent):
    '''
    :param str title:标题
    :param str page:页码
    :param dictionary parent:父标签
    '''
    print(f"title: {title}, page: {page}")
    if not parent['sub']:
        return
    for bookmark in parent['sub'].values():
        title = bookmark['title']
        page = bookmark['page']
        parent = bookmark
        print_bookmark(title, page, parent)

def read_bookmarks():
    bookmarks = get_bookmarks()
    for bookmark in bookmarks.values():
        title = bookmark['title']
        page = bookmark['page']
        print_bookmark(title, page, bookmark)

read_bookmarks()