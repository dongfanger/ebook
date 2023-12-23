# coding:utf-8
import os
import platform
# import commands
import re
import shutil
import subprocess
import sys

osName = platform.system()
base_dir = os.path.dirname(os.path.abspath(__file__))
catalog_path = os.path.join(base_dir, "source", "catalog.json")
blog_path = os.path.join(base_dir, "source")
blog_source_path = os.path.join(os.path.dirname(base_dir), "blog-source")
index_path = os.path.join(base_dir, "README.md")
base_link = "https://dongfanger.gitee.io/blog/"
readme_header = """

"""
readme_tooter = """

"""


def get_file_info(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        first_line = file.readline().replace("#", "").strip()
    return first_line.split(' ', 1)


def make_line(chapter, file):
    page_name, _ = os.path.splitext(file)
    (index, title) = get_file_info(file)
    url = base_link + chapter + "/" + page_name + ".html"
    item_list = ["-", index, "[{}]({})\n".format(title, url)]
    return " ".join(item_list)


def render_index_page(index_info):
    """
    生成 readme.md 索引文件，包含所有文件目录
    """
    # 重新排序
    index_info = sorted(index_info.items(), key=lambda item: item[0], reverse=False)

    # 写入文件
    with open(index_path, 'w+', encoding="utf-8") as file:
        file.write(readme_header)
        for chp, info in index_info:
            chp_name = info["name"]
            file.write("## " + chp_name + "\n")
            for line in info["contents"]:
                file.write(line)
            file.write("\n")
        file.write(readme_tooter)


def convert_md5_to_rst(file):
    """
    转换格式：md5转换成rst
    """
    (filename, extension) = os.path.splitext(file)
    convert_cmd = 'pandoc -V mainfont="SimSun" -f markdown -t rst {md_file} -o {rst_file}'.format(
        md_file=filename + '.md', rst_file=filename + '.rst'
    )
    # status, output = commands.getstatusoutput(convert_cmd)
    status = subprocess.call(convert_cmd.split(" "))
    if status != 0:
        print("命令执行失败: " + convert_cmd)
        exit(1)
    if status == 0:
        print(file + ' 处理完成')
    else:
        print(file + '处理失败')


def get_all_dir():
    """
    获取所有的目录
    """
    dir_list = [blog_path]
    file_list = os.listdir(blog_path)
    for item in file_list:
        abs_path = os.path.join(blog_path, item)
        if os.path.isdir(abs_path):
            dir_list.append(abs_path)
    return dir_list


def init_index_info():
    """
    初始化索引
    """
    index_info = {}
    chapter_dir = os.path.join(blog_path, "chapters")
    os.chdir(chapter_dir)
    for file in os.listdir(chapter_dir):
        name, _ = os.path.splitext(file)
        with open(file, 'r', encoding="utf-8") as f:
            chapter_name = f.readlines()[1].strip()
        index_info[name] = {"name": chapter_name, "contents": []}
    return index_info


def replace_md(file):
    wanggang_png = "wanggang.png"
    filename, extension = os.path.splitext(file)
    with open(file, 'r', encoding='utf-8') as f:
        md = f.read()
        md_links = re.findall("!\\[.*?\\]\\(.*?\\)", md)
        md_links += re.findall('<img src=.*/>', md)
        for ml in md_links:
            img_url = re.findall("!\\[.*?\\]\\((.*?)\\)", ml)
            img_url += re.findall('<img src="(.*?)"', ml)
            img_url = img_url[0]
            img_name = img_url.split("/")[-1]
            if img_name != wanggang_png:
                md = md.replace(ml, f"![]({filename}/{img_name})")
        file_data = md
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)

    names = filename.split("-")
    no = names[0].lstrip("0")
    title = "".join(names[1:])
    file_data = ""
    line_no = 1
    second_line = "![](../wanggang.png)\n\n"
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if line_no == 1 and title not in line:
                file_data += f"# {title}\n"
                # if line_no == 2 and wanggang_png not in line:
                file_data += second_line
            file_data += line
            line_no += 1
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def adjust_title_level(file):
    filename, extension = os.path.splitext(file)
    names = filename.split("-")
    title = "".join(names[1:])
    file_data = f""
    line_no = 1
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if line_no == 1 and title in line:
                f.close()
                return
            if line.startswith("# "):
                line = "## " + line[2:]
            elif line.startswith("## "):
                line = "### " + line[3:]
            elif line.startswith("### "):
                line = "#### " + line[4:]
            file_data += line
            line_no += 1
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def replace_first_line(file):
    filename, extension = os.path.splitext(file)
    names = filename.split("-")
    title = "".join(names[1:])
    file_data = f""
    line_no = 1
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if line_no == 1 and title in line:
                line = f"# {title}\n"
            file_data += line
            line_no += 1
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def count_question(file):
    filename, extension = os.path.splitext(file)
    names = filename.split("-")
    title = "".join(names[1:])
    count = 0
    file_data = f""
    line_no = 1
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("**"):
                count += 1
            if line_no > 1:
                file_data += line
            line_no += 1
    file_data = f"# {title} {count}题\n" + file_data
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def main():
    is_adjust = "n" if len(sys.argv) == 1 else sys.argv[1:][0]
    for folder in get_all_dir():
        os.chdir(folder)
        chapter = os.path.split(folder)[1]
        all_file = os.listdir(folder)
        all_md_file = sorted([file for file in all_file if file.endswith('md')])

        for file in all_md_file:
            adjust_title_level(file)
            # replace_first_line(file)
            # line = make_line(chapter, file)
            # index_info[chapter.replace("c", "")]["contents"].append(line)
            replace_md(file)
            if folder.endswith("面试题"):
                count_question(file)
            convert_md5_to_rst(file)


def debug():
    file = r"D:\dongfanger\blog-maker\source\JMeter\003-JMeter英文版界面介绍.md"
    adjust_title_level(file)
    # line = make_line(chapter, file)
    # index_info[chapter.replace("c", "")]["contents"].append(line)
    replace_md(file)
    convert_md5_to_rst(file)


if __name__ == '__main__':
    index_info = init_index_info()
    main()
    # debug()
    # render_index_page(index_info)
    # count_video()
    print("OK")
