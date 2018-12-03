# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import os, sys
# 将django项目根目录加入环境变量
parent_path = os.path.dirname('E:\python\wxproject\homepage')
sys.path.append(parent_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wxproject.settings")