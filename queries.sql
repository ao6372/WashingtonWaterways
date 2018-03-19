--takes .5 percentile and the average over all years for each coordinate
select AVG(ratios), lat, lon from a1data where percentile=.5 GROUP BY lat,lon;

--Takes the ratio of 2099 over 2019
SELECT a.avgratio/b.avgratio as ratio, a.lat, b.lon
  from
      (SELECT avg(ratios) as AVGRATIO, year, lat, lon FROM a1data
        WHERE year = 2099
      GROUP BY (year, lat, lon)
      ORDER BY (lat, lon)) a,
      (SELECT avg(ratios) as AVGRATIO, year, lat, lon FROM a1data
      WHERE year =2019
      GROUP BY (year, lat, lon)
      ORDER BY (lat, lon)) b
 where a.lat = b.lat
   and a.lon = b.lon
 Order by ratio DESC;

--takes avg of all the ratios from the .05 percentile (implicltly averaged across models)
SELECT avg(ratios) as AVG, year FROM a1data
WHERE percentile=.05
GROUP BY year
ORDER by year ASC;

SElECT avg(ratios) as AVG, lat,lon, year FROM a1data
WHERE percentile=.05
GROUP BY lat,lon, year
ORDER by year ASC;
