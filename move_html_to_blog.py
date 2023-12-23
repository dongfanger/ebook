#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2021/02/04 19:32
@Desc    :  
"""

import shutil
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
blog_dir = os.path.join(os.path.dirname(base_dir), "blog")
os.chdir(blog_dir)
for dir_file in os.listdir(blog_dir):
    if dir_file != ".git":
        if os.path.isfile(dir_file):
            os.remove(dir_file)
        if os.path.isdir(dir_file):
            shutil.rmtree(dir_file)
html_dir = os.path.join(base_dir, "build", "html")
os.chdir(html_dir)
_sources_dir = os.path.join(html_dir, "_sources")
if os.path.exists(_sources_dir):
    shutil.rmtree(_sources_dir)
for dir_file in os.listdir(html_dir):
    if os.path.isfile(dir_file):
        shutil.copy2(dir_file, blog_dir)
    if os.path.isdir(dir_file):
        shutil.copytree(dir_file, os.path.join(blog_dir, dir_file))
print("move html to blog finished!")
