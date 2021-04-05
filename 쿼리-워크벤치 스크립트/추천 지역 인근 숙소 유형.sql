select 숙소.업종명 as '숙소 유형', count(숙소.업종명) as '유형 별 숙소 개수' 
from 숙소, 지역, 검색기록, 고객 where 검색기록.고객번호=고객.고객번호 and 검색기록.추천결과=숙소.지역코드 
and 검색기록.추천결과=지역.지역코드 and 숙소.지역코드='Q01' 
group by 숙소.업종명;
