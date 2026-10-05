select merchant, country, count(*) as txns,
       sum(case when score > 0.6 then 1 else 0 end) as flagged,
       round(avg(score), 3) as avg_score
from {{ source('bronze', 'txn') }}
group by 1, 2
