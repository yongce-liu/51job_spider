# _*_ coding: utf-8 _*_
from bs4 import BeautifulSoup
import re
import requests
import xlwt
import time
import random
import sqlite3
import json


url_job = ["python", "java", "C", "web", "html", "UI", "javascript"]
job_head_list = ['job_href', 'job_name', 'company_href', 'company_name',
                 'providesalary_text', 'workarea_text', 'updatedate',
                 'companytype_text', 'jobwelf', 'attribute_text',
                 'companysize_text', 'companyind_text']
db_path = "51_job.db"


# 创建 main 函数以供调用函数
def main():
    job_dict = deal_url()
    total_data = get_all_data(job_dict)
    # for job in total_data:
    #     for item_list in total_data[job]:
    #         for index in range(len(item_list)):
    #             print(item_list[index])
    # for job in total_data:
    #     print("-" * 20)
    #     print(total_data[job])
    #     print("-" * 20)
    # print(total_data)
    # print(total_data)
    # print(job_head_list)
    # 表格形式
    # save_data1(total_data)
    # 数据库形式
    save_data2(total_data)
    print("白嫖完毕, 我们 Python 实在是太厉害啦!")
    # 在字典中 遍历出 key
    # for key in total_data:
    #     # 输出每一种工作的信息
    #     print('\n\n\n')
    #     print(key)
    #     for data in total_data[key]:
    #         print(data)


# 1. 循环处理多个 url
def deal_url():
    # 创建具有一般性的 url 构造
    url_base = "https://search.51job.com/list/000000,000000,0000,32,9,99,"
    # 储存多个工作 html 信息的字典
    job_dict = {}
    # 循环遍历
    for job in url_job:
        # 储存一个工作 html 信息
        page_list = []
        for url_page in range(1, 51):
            url = url_base + job + ",2," + str(url_page) + ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
            page_html = get_html(url)
            page_list.append(page_html)
        # 设置间隔时间
        time.sleep(random.random() * 3)
        job_dict[job] = page_list

    # 测试
    # print(type(job_list))
    # print(type(html_sum))
    # print(job_list[0])

    return job_dict


# 2. 解析一个 url 获得网页 html.text
def get_html(url):
    html_text = ""
    # 创建头代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}

    try:
        # GET 方式访问, 创建对象
        response = requests.get(url, headers=headers)
        # 获得网页信息
        html_text = response.text
        # 测试
        # print(html)
    # 异常检测
    except:
        print("访问网页出错, 请尝试修改访问信息.")

    return str(html_text)


# 2. 创造正则表达式, 构造抓取信息
# 由于网站特殊性, 且本人经验不足, 莫名其妙的居然是字典类型
# find_title = re.compile(r'r<span title="(.*?)".*?</span>', re.S)
# find_release_time =
# find_address =
# find_company_name =
# find_company_rank =
# find_salary =
# find_request =
# find_tip =


# 3. 分析 html 内容, 获得想要的信息 , 以列表形式储存每个字典,
def get_data(html):
    # 创建一个列表用作返回数据
    data_list = []
    try:
        # 创建一碗靓丽的汤, 以供我们好好享用
        soup = BeautifulSoup(html, "html.parser")
        # print(soap)
        data = str(soup.find_all("script", type="text/javascript"))
        # print(data)#, 此时data为类对象
        precise_data_list = re.findall('({"type".*?})', data)
        # print(precise_data_list)

    except:
        return

    for data_temp in precise_data_list:
        # print(data_temp)
        # 转换为字典
        data_dict = json.loads(data_temp)
        # print(data_dict)
        # 为字典类型
        # print(type(data_dict))
        # 处理字典, 留下我们想要的数据
        data_dict.pop("type")
        data_dict.pop("jt")
        data_dict.pop("tags")
        data_dict.pop("ad_track")
        data_dict.pop("jobid")
        data_dict.pop("coid")
        data_dict.pop("effect")
        data_dict.pop("is_special_job")
        data_dict.pop("job_title")
        data_dict.pop("workarea")
        data_dict.pop("iscommunicate")
        data_dict.pop("degreefrom")
        data_dict.pop("workyear")
        data_dict.pop("issuedate")
        data_dict.pop("isFromXyz")
        data_dict.pop("isIntern")
        data_dict.pop("jobwelf_list")
        data_dict.pop("adid")

        data_list_singular = []
        # print('*' * 10)
        # print(data_dict)
        # print('*' * 10)
        # break

        for key in data_dict:
            # 将字典, 转换为列表添加到我们想要返回的列表中来
            if data_dict[key] == "":
                data_dict[key] = " "
            data_list_singular.append(str(data_dict[key]))
        # print(data_list_singular)

        data_list.append(data_list_singular)

    return data_list


# 4. 利用循环遍历,获得所有页面的信息
def get_all_data(job_dict):
    job_data_dict = {}
    # 在列表的列表遍历出每一种工作的列表
    for job in job_dict:
        job_data_list = []
        # 在工作列表中遍历出页面字符串
        for page_html in job_dict[job]:
            # 得到每一页的数据
            page_data = get_data(page_html)
            # 储存一种工作所有页数据的列表
            job_data_list.extend(page_data)
        # 储存每一种工作的字典
        job_data_dict[job] = job_data_list

    return job_data_dict


# 5. 保存数据到 表格
def save_data1(data_dict):
    # 创建 workbook 对象, 可以理解为一个 .xls 文件
    workbook = xlwt.Workbook(encoding="UTF-8")
    # 创建工作表, 可以理解为 sheet, 同时写入表头
    for job in data_dict:
        # 设置 sheet 名字
        job_sheet = workbook.add_sheet(job)
        # 写入表头
        row = 0
        for job_head in job_head_list:
            job_sheet.write(0, row, job_head)
            row += 1
        # 写入数据
        # 找出每一个具体的工作信息 --> 字典
        # print(key)
        line = 1
        for item_list in data_dict[job]:
            row = 0
            # print(item_list)
            for item in item_list:
                if item == "":
                    job_sheet.write(line, row, "  ")
                    row += 1
                else:
                    job_sheet.write(line, row, item)
                    # print(item)
                    row += 1
            line += 1

    # sheet, workbook, 输入数据完毕后, 进行保存
    workbook.save("job_data.xls")


# 6. 创建数据表的初始化方法
def init_db(name):
    # 创建数据表
    # 12 个表头
    sql = '''
            CREATE TABLE IF NOT EXISTS %s
            (
            id integer primary key autoincrement,
            job_href text, job_name text, company_href text, company_name text,
            providesalary_text text, workarea_text text, updatedate text,
            companytype_text text, jobwelf text, attribute_text text,
            companysize_text text, companyind_text text
            );
    ''' % name

    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute(sql)
    connect.commit()

    cursor.close()
    connect.close()


# 7. 保存数据到数据库
def save_data2(data_dict):

    for key in data_dict:
        init_db(key)
        # 链接 数据库
        conn = sqlite3.connect(db_path)
        # 获取 游标
        cur = conn.cursor()
        for item_list in data_dict[key]:
            for index in range(len(item_list)):
                item_list[index] = str('"' + str(item_list[index]) + '"')

            string = ",".join(item_list)
            sql = '''INSERT INTO  %s
            values (NULL, %s)
            ''' % (key, string)

            cur.execute(sql)
            conn.commit()

        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
