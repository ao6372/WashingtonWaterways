
SELECT a.avgratio/b.avgratio as ratio, a.latitude, b.longitude
  from
      (SELECT avg(ratios) as AVGRATIO, year, latitude, longitude FROM fivepctla1
        WHERE year = 2099
      GROUP BY (year, latitude, longitude)
      ORDER BY (latitude, longitude)) a,
      (SELECT avg(ratios) as AVGRATIO, year, latitude, longitude FROM fivepctla1
      WHERE year =2016
      GROUP BY (year, latitude, longitude)
      ORDER BY (latitude, longitude)) b
 where a.latitude = b.latitude
   and a.longitude = b.longitude
 Order by ratio DESC;


SELECT avg(ratios) as AVGRATIO, year, latitude, longitude FROM fivepctla1
WHERE year = 2099 or year =2015
GROUP BY (year, latitude, longitude)
ORDER BY (latitude, longitude);


select avg(ratios) as AVG, year FROM fivepctlA1 GROUP BY year
ORDER by year ASC;


SELECT ratios, year, model,lat,lon FROM A1data
WHERE percentile = .05;
