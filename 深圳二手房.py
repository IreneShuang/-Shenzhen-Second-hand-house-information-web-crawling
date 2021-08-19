# -*- coding: utf-8 -*-
"""
深圳二手房信息爬虫

爬虫链接：https://sz.lianjia.com/ershoufang/

Created on Tue Aug 17 17:12:40 2021

@author: Irene Tan
"""

from selenium import webdriver #导入浏览器的功能
import re #正则表达式，内置
import time #用于处理延迟翻页
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

#创建webdriver
basic_url="https://sz.lianjia.com/ershoufang/pg"
scroll_down_js='document.documentElement.scrollTop = document.documentElement.scrollHeight'

#定义等会需要储存信息的list
name=[]
good_house_tag=[]
location=[]
structure=[]
area=[]
direction=[]
decoration=[]
floor=[]
building_construction_time=[]
building_situation=[]
hit_level=[]
price=[]
unit_price=[]


def shen_zhen_er_shou(pages):
    driver = webdriver.Chrome(r"C:\Users\Lenovo\Desktop\ChromeDriver\chromedriver.exe")
    for page_number in range(1,pages+1):
        
        driver.get(basic_url+str(page_number)+"/")
        driver.execute_script(scroll_down_js)
    
        #开始肝
        house_content_frame=driver.find_element_by_css_selector("ul.sellListContent")
        houses=house_content_frame.find_elements_by_css_selector("li.clear.LOGCLICKDATA")
        
        for house in houses:
            house_info=house.find_element_by_css_selector("div.info.clear")
            #名字
            name1=house_info.find_element_by_css_selector(".title").find_element_by_css_selector("a").text
            name.append(name1)
            
            #标签
            tag1=house_info.find_element_by_css_selector(".title").find_element_by_css_selector("span.goodhouse_tag.tagBlock").text
            good_house_tag.append(tag1)
            
            #地点
            location1=house_info.find_element_by_css_selector("div.positionInfo").text
            location.append(location1)
            
            #更多信息
            more_info1=house_info.find_element_by_css_selector(".address").text
            
           
            if more_info1.count("|")!=6:
                more_info1=more_info1+"|无"
            else: 
                more_info1=more_info1
                
            more_info2=more_info1.split("|")
            
            structure.append(more_info2[0])
            area.append(more_info2[1])
            direction.append(more_info2[2])
            decoration.append(more_info2[3])
            floor.append(more_info2[4])
            building_construction_time.append(more_info2[5])
            building_situation.append(more_info2[6])
            
            
        
            #热度
            hit_level1=house_info.find_element_by_css_selector(".followInfo").text
            hit_level.append(hit_level1)
            
            #价格
            try:
                price1=house_info.find_element_by_css_selector("div.totalPrice.totalPrice2").find_element_by_css_selector("span").text
            except NoSuchElementException:
                price1=house_info.find_element_by_css_selector("div.totalPrice").find_element_by_css_selector("span").text
                
            price.append(price1)
            
            #每平方价格
            unit_price1=house_info.find_element_by_css_selector(".unitPrice").text
            unit_price.append(unit_price1)
            
            
    #制作数据表格
    final_list=[name,good_house_tag,location,structure,area,direction,decoration,floor,building_construction_time,building_situation, hit_level,price, unit_price]
    
    df=pd.DataFrame(final_list)
    df_final=df.transpose()
    df_final.columns=["房屋名字","标签","地点",'住房结构','住房面积','朝向','装修情况','高/低楼层','楼层竣工时间','楼层情况', "热度","价格（万元）", "每平方米单价"]
    
    return df_final





if __name__ == "__main__":
    print("此项目用于爬取链家上深圳二手房的信息（包括房屋名称，价格，地点，室内结构，房屋面积，所在楼的楼层，所在楼楼层竣工时间，房屋热度）")
    print("This project is for getting all the infomation of Shenzhen's second-hand house(including name, price, location,structure, area, floor, etc.)")
    print("*************************")
    print("作者：双儿")
    print("Author:Irene Tan")
    print("*************************")
    print("仅供个人学习使用，欢迎批评指正！注：爬虫项目时效性短，请适当修改再运作")
    
    crawling_page=int(input("请输入你想要爬取的页数（每页有30个房源，最多100页,请键入数字）\ How many pages do you want to crawl? please enter a int:max:100 pages with 30 houses in each page:"))
    print("正在为您爬取.../crwarling data...")
    result=shen_zhen_er_shou(crawling_page)
    print(result)
    
    download=input("数据已经爬取完毕，需要将表格下载到本地吗？（y/n）\The data is ready, do you want a local copy? y/n:")
    if download=="y":
        result.to_csv("深圳二手房价.csv",encoding="utf_8_sig")
        print("您的数据已保存到本地/Your data is already download to your computer!")
        print("感谢使用！/ Thanks for using!")
    else:
        print("感谢使用！/Thanks for using!")
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
