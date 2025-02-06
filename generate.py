from markdown import markdown
import os
from json import load
tree = {"/pages/":[None,[]]}
alias = {}
bg = {}
titlecolor = {}
desc = {}
title = {}
template = open("template.html","r",encoding="UTF-8").read()
mdmodules = ["markdown.extensions.extra","markdown.extensions.codehilite","markdown.extensions.tables","markdown.extensions.toc"]#,"markdown_katex"
mdconfigs = {}
def build(dir,todir,webdir):
    subfiles = []
    subdirs = []
    for name in os.listdir(dir):
        fullname = dir + "/" + name
        fulltoname = todir + "/" + name
        fullwebdir = webdir + name + "/"
        if os.path.isfile(fullname) and name.endswith(".md"):
            fullwebdir = "".join(list(fullwebdir)[:-4]) + "/"
            fulltoname = "".join(list(fulltoname)[:-3])
            os.mkdir(fulltoname)
            tree[fullwebdir] = [webdir,[]]
            tree[webdir][1].append(fullwebdir)
            generate(fullname,fulltoname + "/index.html",fullwebdir)
            subfiles.append(name)
        elif os.path.isdir(fullname):
            tree[fullwebdir] = [webdir,[]]
            tree[webdir][1].append(fullwebdir)
            initdir(fullname,fulltoname,fullwebdir)
            build(fullname,fulltoname,fullwebdir)
            subdirs.append(name)
        gen_dir_page(dir,todir,webdir,subfiles,subdirs)
def generate(file,tofile,webdir):
    r = tree[webdir][0]
    breadcrumb = f'<li class="breadcrumb-item active">{webdir.split("/")[-2]}</li>'
    while r:
        breadcrumb = f'<li class="breadcrumb-item"><a href="{r}">{alias[r]}</a></li>' + breadcrumb
        r = tree[r][0]
    with open(file,"r",encoding="UTF-8") as f:
        title[webdir] = f.readline()
        content = template
        content = content.replace("{{content}}",markdown(f.read(),extensions=mdmodules,extension_configs=mdconfigs))
        content = content.replace("{{title}}",title[webdir])
        content = content.replace("{{titlecolor}}",titlecolor[tree[webdir][0]])
        content = content.replace("{{bg}}",bg[tree[webdir][0]])
        content = content.replace("{{breadcrumb}}",breadcrumb)
        with open(tofile,"w",encoding="UTF-8") as tof:
            tof.write(content)
def gen_dir_page(dir,todir,webdir,subfiles,subdirs):
    r = webdir
    breadcrumb = ""
    while r:
        breadcrumb = f'<li class="breadcrumb-item"><a href="{r}">{alias[r]}</a></li>' + breadcrumb
        r = tree[r][0]
    html = '<ul class="list-group">'
    for dir in subdirs:
        subwebname = webdir + dir + "/"
        html += f'<a class="list-group-item list-group-item-action" href="{subwebname}">{alias[subwebname]}/</a>'
    for file in subfiles:
        subwebname = webdir + "".join(list(file)[:-3]) + "/"
        html += f'<a class="list-group-item list-group-item-action" href="{subwebname}">{title[subwebname]}</a>'
    with open(todir + "/index.html","w",encoding="UTF-8") as file:
        content = template
        content = content.replace("{{content}}",html)
        content = content.replace("{{title}}",alias[webdir])
        content = content.replace("{{titlecolor}}",titlecolor[webdir])
        content = content.replace("{{bg}}",bg[webdir])
        content = content.replace("{{breadcrumb}}",breadcrumb)
        file.write(content)
def initdir(odir,todir,webdir):
    os.mkdir(todir)
    if os.path.isfile(odir + "/prop.json"):
        json = load(open(odir + "/prop.json","r",encoding="UTF-8"))
        alias[webdir] = json["name"]
        bg[webdir] = json.get("bg") if json.get("bg") else bg["/".join(webdir.split("/")[:-2]) + "/"]
        titlecolor[webdir] = json.get("titlecolor") if json.get("titlecolor") else titlecolor["/".join(webdir.split("/")[:-2]) + "/"]
        desc[webdir] = json.get("desc")
    else:
        alias[webdir] = odir.split("/")[-1]
        bg[webdir] = bg["/".join(webdir.split("/")[:-2]) + "/"]
        titlecolor[webdir] = titlecolor["/".join(webdir.split("/")[:-2]) + "/"]
        desc[webdir] = ""
print("将要执行命令 rm -r pages，确认执行吗？")
input("请按下 Enter 键以执行...")
os.system("rm -r pages")
initdir("markdown","pages","/pages/")
build("markdown","pages","/pages/")
print(tree,alias)