"""
    match_alerts.py

    A utility that we used to visualize our CAP report and Storm Event database matching algorithm.

    Runs query and outputs to CSV
"""

import logging
import MySQLdb as mdb
import csv
from config import *

logging.basicConfig(format='%(asctime)s;%(levelname)s:%(message)s', level=logging.DEBUG)

w = open('../matched.csv','w')
writer = csv.writer(w, delimiter=',')

con = mdb.connect(mysql_host, mysql_user, mysql_pass, mysql_db)
with con:
    cur = con.cursor()
    #cur.execute('SELECT * FROM `weather-severity`.cap c JOIN `weather-severity`.cap_fips capfips ON capfips.cap = c.id \
    #             JOIN `weather-severity`.storm_events se ON se.fips = capfips.fips \
    #             WHERE (c.begin_time >= se.begin_time AND c.expires <= se.end_time) \
    #             OR ( ABS(TIMESTAMPDIFF(MINUTE,c.begin_time,se.begin_time)) <= 0.25 * TIMESTAMPDIFF(MINUTE,se.end_time,se.begin_time) \
    #             AND ABS(TIMESTAMPDIFF(MINUTE,c.expires,se.end_time)) <= 0.25 * TIMESTAMPDIFF(MINUTE,se.end_time,se.begin_time))')
    cur.execute('SELECT * FROM `weather-severity`.cap c JOIN `weather-severity`.cap_fips capfips ON capfips.cap = c.id '
                'JOIN `weather-severity`.storm_events se ON se.fips = capfips.fips '
                'JOIN `weather-severity`.valid_events ve '
                'WHERE (ve.cap_type = c.event) AND (ve.se_type = se.event_type) AND (ve.valid = 1) AND ((c.begin_time >= se.begin_time AND c.expires <= se.end_time) '
                'OR ( ABS(TIMESTAMPDIFF(MINUTE,c.begin_time,se.begin_time)) <= 0.25 * TIMESTAMPDIFF(MINUTE,se.end_time,se.begin_time) '
                'AND ABS(TIMESTAMPDIFF(MINUTE,c.expires,se.end_time)) <= 0.25 * TIMESTAMPDIFF(MINUTE,se.end_time,se.begin_time)) '
                'OR (se.begin_time >= c.begin_time AND se.end_time <= c.expires) '
                'OR ( ABS(TIMESTAMPDIFF(MINUTE,c.begin_time,se.begin_time)) <= 0.25 * TIMESTAMPDIFF(MINUTE,c.expires,c.begin_time) '
                'AND ABS(TIMESTAMPDIFF(MINUTE,c.expires,se.end_time)) <= 0.25 * TIMESTAMPDIFF(MINUTE,c.expires,c.begin_time)))'
    )
    # CAP Fully Contained in Storm Event OR CAP start date is within a margin of 20% of the duration of the storm event

    for row in cur:
        writer.writerow(row)

w.close()