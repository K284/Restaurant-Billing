import csv
import numpy as np
import matplotlib.pyplot as plt
from subprocess import Popen
import mysql.connector as msc

#GRAPH MAKING
#fig = plt.figure()
#ax = fig.add_axes([0,0,1,1])
range = np.arange(1,21)
plt.xlabel("Date")
plt.ylabel("Count")
plt.yticks(range)



#DISPLAYING DETAILS
conn = msc.connect(host = "localhost", username = "root", password = "ahsirk", database = "restaurant")
c = conn.cursor()
c.execute("select date, count from plot where type = '%s'"%("Breakfast",))
bf = c.fetchall()

c.execute("select date, count from plot where type = '%s'"%("Lunch",))
lunch = c.fetchall()

c.execute("select date, count from plot where type = '%s'"%("Dinner",))
dinner = c.fetchall()

data = [("Dateb", "Breakfast")]+bf+[("Datel", "Lunch")]+lunch+[("Dated", "Dinner")]+dinner
with open("Plot.csv", "w") as plot:
    writer = csv.writer(plot)
    writer.writerows(data)

#OPENING CSV FILE    
#p = Popen("Plot.csv", shell = True)

#GRAPH CREATION FOR BREAKFAST
x = []
y = []
for row in bf:
    x.append(row[0].strftime('%y-%m-%d'))
    y.append(row[1])


#GRAPH CREATION FOR LUNCH
a = []
b = []
for row in lunch:
    a.append(row[0].strftime('%y-%m-%d'))
    b.append(row[1])


#GRAPH CREATION FOR DINNER
c= []
d = []
for row in dinner:
    c.append(row[0].strftime('%y-%m-%d'))
    d.append(row[1])

W = np.arange(len(x))
plt.xticks(W, x)
plt.bar(W, y, color = "violet", label = "Breakfast", width = 0.25)
plt.bar(W+0.25, b, color = "orange", label = "Lunch", width = 0.25)
plt.bar(W+0.5, d, color = "red", label ="Dinner", width = 0.25)
plt.legend()
plt.show()











    

