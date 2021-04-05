select 고객.고객이름 as 고객이름, 지역.지역명 as 추천지역명, 검색기록.여행예정월 as 여행예정월, 검색기록.축제취향, 축제.축제명 as 추천지역의축제 
from 검색기록, 축제, 지역,고객 where 검색기록.추천결과=축제.지역코드 and 검색기록.축제취향=축제.소분류 
and 검색기록.고객번호=고객.고객번호 and 지역.지역코드=축제.지역코드 and 검색기록.여행예정월=축제.축제기간 
and 검색기록.검색기록번호=5; 
