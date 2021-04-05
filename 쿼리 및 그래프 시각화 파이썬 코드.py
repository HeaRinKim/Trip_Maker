#!/usr/bin/env python
# coding: utf-8

# ## Import libraries

# In[1]:


# -*- coding: utf-8 -*-


# In[2]:


import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np


# ## Connect to database using PyMySQL

# In[3]:


conn = pymysql.connect(host='localhost', user='root', password='autoset', db='travel', charset='utf8')


# In[4]:


cursor = conn.cursor(pymysql.cursors.DictCursor)


# In[5]:


import pandas as pd


# ## 쿼리 1: 여행 예정 월 당 사람 수

# In[6]:


sql="select 검색기록.여행예정월 as '월', count(검색기록.검색기록번호) as '방문 예정 인원 수' from 검색기록, 고객 where 검색기록.고객번호=고객.고객번호 group by 검색기록.여행예정월;"
cursor.execute(sql)
query1=cursor.fetchall()


# In[7]:


query1=pd.DataFrame(query1)
query1


# ## 쿼리1 시각화 

# In[8]:


import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

print("Matplotlib version", matplotlib.__version__)
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")


# ## 글자 깨짐 수정코드

# In[9]:


import matplotlib
from matplotlib import font_manager, rc
import platform

if platform.system() == 'Windows':
# 윈도우인 경우
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)


# ## 월 별 방문 예정 인원 수 시각화 -  막대그래프

# In[10]:


import matplotlib.pyplot as pls 

query1.plot(x='월', y='방문 예정 인원 수', kind='bar') 
plt.show()


# ## 단일 그래프

# In[11]:


query1.plot(x='월', y='방문 예정 인원 수', kind='line')


# ## 파이그래프

# In[68]:


from matplotlib import pyplot 

query1['방문 예정 인원 수'].plot.pie(autopct='%0.1f%%')
categories=['3월','4월','5월','7월','8월','9월','10월','12월']
pyplot.legend(categories)
pyplot.show()


# ## 쿼리2: 추천 지역에 들어있는 관광지 (예시: 검색기록 번호가 5번일 때)

# In[43]:


query2=pd.DataFrame(columns=['고객 이름','추천 지역 명','관광지 취향', '추천 지역의 관광지'])


# In[44]:


sql="select 고객.고객이름 as 고객이름, 지역.지역명 as 추천지역명, 검색기록.관광지취향, 관광지.관광지명 as 추천지역의관광지 from 검색기록, 관광지, 지역,고객 where 검색기록.추천결과=관광지.지역코드 and 검색기록.관광지취향=관광지.소분류 and 검색기록.고객번호=고객.고객번호 and 지역.지역코드=관광지.지역코드 and 검색기록.검색기록번호=5;"
cursor.execute(sql)
query2=cursor.fetchall()


# In[45]:


query2=pd.DataFrame(query2)
query2


# ## 쿼리3: 추천 지역에서 개최되는 축제 (예시: 검색기록 번호가 5번 일 때)

# In[48]:



sql="select 고객.고객이름 as 고객이름, 지역.지역명 as 추천지역명, 검색기록.여행예정월 as 여행예정월, 검색기록.축제취향, 축제.축제명 as 추천지역의축제 from 검색기록, 축제, 지역,고객 where 검색기록.추천결과=축제.지역코드 and 검색기록.축제취향=축제.소분류 and 검색기록.고객번호=고객.고객번호 and 지역.지역코드=축제.지역코드 and 검색기록.여행예정월=축제.축제기간 and 검색기록.검색기록번호=5; "

cursor.execute(sql)
query3=cursor.fetchall()
query3=pd.DataFrame(query3)
query3


# ## 쿼리 2+3: 검색 결과를 바탕으로 관광 요소 조합 (관광지 , 축제) 목록 (예시: 검색기록 번호가 5번일 때)

# In[49]:



sql="select 관광지.관광지명 as 추천지역의관광지, 축제.축제명 as 추천지역의축제 from 검색기록, 관광지, 지역,고객, 축제 where 검색기록.추천결과=관광지.지역코드 and 검색기록.관광지취향=관광지.소분류 and 검색기록.고객번호=고객.고객번호 and 지역.지역코드=관광지.지역코드 and 검색기록.추천결과=축제.지역코드 and 검색기록.축제취향=축제.소분류 and 지역.지역코드=축제.지역코드 and 검색기록.여행예정월=축제.축제기간 and 검색기록.검색기록번호=5;"

cursor.execute(sql)
query23=cursor.fetchall()
query23=pd.DataFrame(query23)
query23


# ## 쿼리4: 추천 지역 인근의 숙소의 유형 (예시: 검색기록 번호가 5번 일 때)

# In[56]:


sql="select 숙소.업종명 as '숙소 유형', count(숙소.업종명) as '유형 별 숙소 개수' from 숙소, 지역, 검색기록, 고객 where 검색기록.고객번호=고객.고객번호 and 검색기록.추천결과=숙소.지역코드 and 검색기록.추천결과=지역.지역코드 and 숙소.지역코드='Q01' group by 숙소.업종명;"
cursor.execute(sql)
query4=cursor.fetchall()
query4=pd.DataFrame(query4)
query4


# In[57]:


import matplotlib.pyplot as pls 

query4.plot(x='숙소 유형', y='유형 별 숙소 개수', kind='bar') 
plt.show()


# ## 민박 제외 막대그래프

# In[59]:


sql="select 숙소.업종명 as '숙소 유형', count(숙소.업종명) as '유형 별 숙소 개수' from 숙소, 지역, 검색기록, 고객 where 검색기록.고객번호=고객.고객번호 and 검색기록.추천결과=숙소.지역코드 and 검색기록.추천결과=지역.지역코드 and 숙소.지역코드='Q01' group by 숙소.업종명 having count(숙소.업종명)<1000;"
cursor.execute(sql)
query4_s=cursor.fetchall()
query4_s=pd.DataFrame(query4_s)
query4_s


# In[60]:


import matplotlib.pyplot as pls 

query4_s.plot(x='숙소 유형', y='유형 별 숙소 개수', kind='bar') 
plt.show()


# In[69]:


from matplotlib import pyplot 


query4_s['유형 별 숙소 개수'].plot.pie(autopct='%0.1f%%', x='숙소 유형', y='유형 별 숙소 개수')
categories=['가족호텔업','관광호텔업','소형호텔업','콘도','한국전통호텔','호스텔']
pyplot.legend(categories)

pyplot.show()


# ## 쿼리5: 매칭 목록 - 여행 예정 월과 지역이 같은 사람 (7월에 제주도)

# In[70]:


sql="select 고객.고객이름 as 추천후보, 고객.나이대 as 연령대, 검색기록.여행예정월, 지역.지역명 as 추천_여행지, 검색기록.관광지취향 as 관광지_취향, 검색기록.음식점취향 as 음식점_취향, 검색기록.축제취향 as 축제_취향 from 고객, 검색기록, 지역 where 검색기록.여행예정월=7 and 검색기록.추천결과='Q01' and 검색기록.고객번호=고객.고객번호 and 검색기록.추천결과=지역.지역코드 group by 고객.고객이름 ;"
cursor.execute(sql)
query5=cursor.fetchall()
query5=pd.DataFrame(query5)
query5


# ## 쿼리5-1: 매칭 목록의 연령대 별 분포

# In[62]:


sql="select 고객.고객이름 as 추천후보, 고객.나이대 as 연령대 from 고객, 검색기록, 지역 where 검색기록.여행예정월=7 and 검색기록.추천결과='Q01' and 검색기록.고객번호=고객.고객번호 and 검색기록.추천결과=지역.지역코드 ;"
cursor.execute(sql)
query5_1=cursor.fetchall()
query5_1=pd.DataFrame(query5_1)
query5_1


# In[27]:


import matplotlib.pyplot as pls 

query5_1_sample=query5_1.iloc[:,[1]]
query5_1_sample


# ## 쿼리6: 추천 지역의 숙소 중 내국인 전용 숙소 (추천지역 대구일 때)

# In[67]:


sql="Select 업소명 AS '숙소명 내국인 전용', 숙소.업종명 AS '숙소 구분', 숙소.소재지도로명주소 AS '숙소 주소' FROM 숙소,검색기록,지역,고객 where 숙소.지역코드=검색기록.추천결과 and 서비스대상구분 = '내국인' and 검색기록.추천결과='C01' and 검색기록.추천결과=지역.지역코드 and 고객.고객번호=검색기록.고객번호;"

cursor.execute(sql)
query6=cursor.fetchall()
query6=pd.DataFrame(query6)
query6

