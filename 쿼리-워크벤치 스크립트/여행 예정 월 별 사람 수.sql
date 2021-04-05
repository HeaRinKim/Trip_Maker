select 검색기록.여행예정월 as '월', count(검색기록.검색기록번호) as '방문 예정 인원 수' 
from 검색기록, 고객 
where 검색기록.고객번호=고객.고객번호 
group by 검색기록.여행예정월;
