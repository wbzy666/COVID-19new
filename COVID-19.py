import numpy as np
import pandas as pd
import requests
from lxml import etree
import json
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker


#获取数据
url='https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0'
res=requests.get(url)
res.encoding='utf-8'#指定编码格式
content=res.text
html=etree.HTML(content)
#/html/body/script[1]
con=html.xpath('/html/body/script[1]/text()')
print(con)
#print(type(con))
con=str(con)
with open('text.txt','w',encoding='utf-8') as f:
    f.write(content)
#转换格式
# 起点 [{"provinceName":"台湾",
# 重点 }catch(e){}']

begin=con.index('[{"provinceName":"台湾",')
end=con.index("}catch(e){}']")
con=con[begin:end]
ls=json.loads(con)

df_data=pd.DataFrame.from_dict(ls)

#显示所有列
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

#分析：
#各省份当前确诊柱状图
ls_province=[] #省份
ls_currentConfirmedCount=[] #当前确诊
ls_suspectedCount=[]#疑似确诊
for x in ls:
    province=x["provinceShortName"]
    ls_province.append(province)
    currentConfirmedCount=x['currentConfirmedCount']
    ls_currentConfirmedCount.append(currentConfirmedCount)
    suspectedCount=x['suspectedCount']
    ls_suspectedCount.append(suspectedCount)

x1=np.array(ls_province)
y1=np.array(ls_currentConfirmedCount)
y2=np.array(ls_suspectedCount)
print(type(x1))
#
# plt.rcParams['font.sans-serif'] = ['SimHei'] # 解决中文乱码
# plt.rcParams['axes.unicode_minus'] = False # 解决给负号不显示
#
# plt.bar(x1,y2)
#
# for i,j in zip(range(len(y2)),y2):
#     plt.text(i,j,j)
#
# plt.title("中国各省份疑似确诊人数统计")
# plt.xlabel("省份")
# plt.ylabel("单位：人")
# plt.show()
print(type(Faker.provinces))

c = (
    Map()
    .add("疫情分布图", [list(z) for z in zip(ls_province, ls_currentConfirmedCount)], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="疫情分布图"),
        visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True),
    )
    .render("map_visualmap_piecewise.html")
)
