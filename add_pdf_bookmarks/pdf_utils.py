#coding=utf-8
#封装的pdf文档处理工具

from PyPDF2 import PdfReader as reader, PdfWriter as writer
import os
import sys
import re

class PDFHandleMode(object):
    '''
    处理pdf文件的模式
    '''
    # 保留源pdf文档的所有内容和，在此基础上修改
    COPY = 'copy'
    # 仅保留源pdf文档的页面内容，在此基础上修改
    NEWLY = 'newly'

class MyPDFHandler(object):
    '''
    封装pdf处理类
    '''
    def __init__(self, pdf_file_path, mode = PDFHandleMode.COPY) -> None:
        '''
        用一个pdf文件初始化
        :param pdf_file_path: pdf文件路路径
        :param mode: 文件处理模式, 默认模式为PDFHandleMode.COPY
        '''
    
        print('pdf文件：{}'.format(pdf_file_path))

        # 定义只读的pdf对象
        self.__pdf = reader(pdf_file_path)
        # 获取pdf文件名（不带路径）
        self.file_name = os.path.basename(pdf_file_path)
        #
        self.metadata = self.__pdf.xmp_metadata
        #
        self.doc_info = self.__pdf.metadata
        #
        self.pages_num = len(self.__pdf.pages)

        # 定义可写的pdf对象， 根据不同的模式进行初始化
        self.__writeable_pdf = writer()
        if mode == PDFHandleMode.COPY:
            self.__writeable_pdf.cloneDocumentFromReader(self.__pdf)
        elif mode == PDFHandleMode.NEWLY:
            for idx in range(self.pages_num):
                page = self.__pdf.pages[idx]
                self.__writeable_pdf.insert_page(page, idx)

    def save2file(self, new_file_name):
        '''
        保存为新的文件
        :param new_file_name: 新的文件名，不要和原来文件名相同
        :return: None
        '''

        with open(new_file_name, 'wb') as fout:
            self.__writeable_pdf.write(fout)
        fout.close()
        print ('save2file success!, new file is:{0}'.format(new_file_name))

    def add_one_bookmark(self, title, page, parent=None, color=None, bold = False, italic = False, fit='/XYZ'):
        '''
        往pdf增加单条标签，并保存为一个新的pdf文件
        :param str title: 书签标题
        :param int page: 书签跳转到的页码，表示的是pdf中绝对页码，值为1表示第一页
        :param parent: 父标签
        :param tuple color: 颜色元组
        :param bool bold: 是否加粗
        :param bool italic: 是否斜体
        :param str fit: 标签缩放方式，默认‘/Fit’
        :return: None 
        '''
        self.__writeable_pdf.add_outline_item(title, page, parent = parent, color = color, bold = bold, italic = italic, fit = None) # TODO： "fit = fit"类型转换错误
        print ('add_one_bookmark success!, new title is:{0}'.format(title))


    def add_bookmarks(self, bookmarks):
        '''
        批量添加书签
        :param tuple bookmarks: 书签元组列表
        :return: None
        '''
        for title, page in bookmarks:
            self.add_one_bookmark(title, page)
            print ('add_bookmarks success!, add {0} pieces of bookmarks to pdf file'.format(len(bookmarks)))

    def read_bookmarks_from_txt(self, txt_file_path, page_offset = 0):
        '''
        从文本文件中读取书签列表
        文本文件中有若干行，每行一个书签，格式为：
        书签标题@页码
        tips；中间用@隔开
        :param str txt_file_path: 书签文本文件路径
        :param page_offset: 页码偏移量，为0或正数，即由于封面、目录等页面的存在，在PDF中实际的绝对页码比在目录中写的页码多出的差值
        :return: 书签列表
        '''
        
        print('工作目录：{}'.format(os.getcwd()))
        current_dir = os.path.dirname(__file__)  # 当前文件所在的目录
        print('当前文件目录：{}'.format(current_dir))
        bookmarks = {}
        with open(os.path.join(current_dir, txt_file_path),encoding='utf-8') as fin:
            for line in fin:
                if not line or line.isspace():
                    continue
                print(line)
                try:
                    title = line.split('@')[0].strip()
                    page = line.split('@')[1].strip()
                except IndexError as msg:
                    print(msg)
                    continue

                if not title or not page:
                    continue
                page = int(page) + page_offset
                try:
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
                except Exception as msg:
                    print(msg)
                    continue
        return bookmarks

    def add_bookmarks_by_read_txt(self, txt_file_path, page_offset=0):
        '''
        通过读取书签文本文件，批量添加pdf标签
        :param txt_file_path: 书签文本路径
        :param page_offset 页码偏移量
        :return: None
        '''
        bookmarks = self.read_bookmarks_from_txt(txt_file_path, page_offset)
        self.add_bookmarks(bookmarks)
        print('add_bookmarks_by_read_txt success!')