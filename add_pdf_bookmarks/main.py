#coding=utf-8

from pdf_utils import MyPDFHandler, PDFHandleMode as mode
import os
import sys

def main():
    print('工作目录：{}'.format(os.getcwd()))
    current_dir = os.path.dirname(__file__)  # 当前文件所在的目录
    print('当前文件目录：{}'.format(current_dir))
    pdf_file = u'Linux.pdf'
    pdf_file = os.path.join(current_dir, pdf_file)
    pdf_handler = MyPDFHandler(pdf_file, mode.NEWLY)
    tags_file = u'tags.txt'
    tags_file = os.path.join(current_dir, tags_file)
    pdf_handler.add_bookmarks_by_read_txt(tags_file)
    pdf_handler.save2file(u'linux就该这么学.pdf')


if __name__ == '__main__':
    print("python：{}".format(sys.version))
    print("默认编码格式：{}".format(sys.getdefaultencoding()))
    main()