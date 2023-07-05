'''
author: Ujjal Das
github: ujjaldas132
date: July, 2023
<p>

'''

import mysql.connector
import time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
database="TRACKER"
)


e = [i for i in range(70)]
s = [i for i in range(70)]
total_combinations = len(e)*len(s)
print("total number of combination possible for the query is : ", total_combinations)

### simple indivitual query
t= time.time()
for x in e:
  for y in s:
    sql = "SELECT * from timeTest where start="+str(x)+ " and  end ="+str(y)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
simple_query_time = time.time()- t
print("time taken by simple query : ", simple_query_time, "secs")




s  = "("+",".join(map(str, s))+")"
e  = "("+",".join(map(str, e))+")"
t= time.time()
sql = "SELECT * from timeTest where start in "+str(e)+ " and  end in "+str(s)
mycursor = mydb.cursor()
mycursor.execute(sql)
myresult = mycursor.fetchall()
inClause_time = time.time()- t
print("time taken by in clause query : ", inClause_time, "secs")
print("in clause query is ", simple_query_time/inClause_time, " times faster")

print("in clause query is taking  ", (simple_query_time-inClause_time)/total_combinations, " sec less per each row")

