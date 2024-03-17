from datetime import datetime
from datetime import date
import csv
from subprocess import Popen
import mysql.connector as msc
conn = msc.connect(host = "localhost", username = "root", password = "ahsirk", database = "restaurant")
c = conn.cursor()
print("\t\t\t\tWELCOME")
c.execute("select bf_id, name, rate from breakfast")
data1= c.fetchall()
c.execute("select soup_id, name, rate from soups")
data2 = c.fetchall()
c.execute("select str_id, name, rate from starters")
data3 = c.fetchall()
c.execute("select meal_id, name, rate from meals")
data4 = c.fetchall()
c.execute("select bry_id, name, rate from biriyani")
data5 = c.fetchall()
c.execute("select md_id, name, rate from mutton_delicacy")
data6 = c.fetchall()
c.execute("select cd_id, name, rate from chicken_delicacy")
data7 = c.fetchall()
c.execute("select sfd_id, name, rate from sea_food_delicacy")
data8 = c.fetchall()
c.execute("select fj_id, name, rate from fresh_juice")
data9 = c.fetchall()
c.execute("select ic_id, name, rate from ice_cream")
data10 = c.fetchall()

data = [("CODE","NAME","RATE")]+[("BREAKFAST",)]+data1+[("SOUPS",)]+data2+[("STARTERS",)]+data3+[("MEALS",)]+data4+[("BIRIYANI",)]+data5+[("MUTTON DELICACY",)]+data6+[("CHICKEN DELICACY",)]+data7+[("SEA FOOD DELICACY",)]+data8+[("FRESH JUICE",)]+data9+[("ICE CREAM",)]+data10
flag = False

#WRITING IN EXCEL
with open('Menu.csv', 'w') as csvfile:
    fwriter = csv.writer(csvfile)
    for x in data:
        fwriter.writerow(x)
        
#OPENING EXCEL
p = Popen('Menu.csv', shell=True)

# ORDER
while True:
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    if time >= "07:00:00" and time < "12:00:00":
        plotime = "Breakfast"
        print(plotime)
        flag = True
        user_order = []
        while True:
            order = input("Enter the code: ")
            if order != "":
                q = int(input("Enter the quantity: "))
                for row in data:
                    if str(row[0]).lower() == order.lower():
                        rate = q* row[2]
                        user_order.append([row[0], row[1], q, rate])               
            else:
                print(user_order)
                break 
                 
        break
    elif time >= "12:00:00" and time <= "16:30:00":
        plotime = "Lunch"
        print(plotime)
        flag = True
        user_order = []
        while True:
            order = input("Enter the code: ")
            if  order != "":
                q = int(input("Enter the quantity: "))
                for row in data:
                    if str(row[0]).lower() == order.lower():
                        rate = q* row[2]
                        user_order.append([row[0], row[1], q, rate])        
            else:
                print(user_order)
                break   
        break
    elif time >= "16:00:00" and time <= "23:00:00":
        plotime = "Dinner"
        print(plotime)
        flag = True
        user_order = []
        while True:
            order = input("Enter the code: ")
            if order != "":
                q = int(input("Enter the quantity: "))
                for row in data:
                    if str(row[0]).lower() == order.lower():
                        rate = q* row[2]
                        user_order.append([row[0], row[1], q, rate])  
            else:
                print(user_order)
                break 
                   
        break
    else:
        print("Sorry can not place order now")
        flag = False
        break

#EXTRA ORDER
if flag == True:
    extra = input("Do you want to order some more?(yes/no) ")
    if extra == "yes":
        while True:
            order = input("Enter the code: ")
            if order != "":
                q = int(input("Enter the quantity: "))
                for r in user_order:
                    if order.lower() == r[0].lower():
                        r[3]  = r[3] + (r[3]/r[2])*q
                        r[2]  = r[2] + q
                        break
                else:
                    for row in data:
                        if str(row[0]).lower() == order.lower():
                            rate = q* row[2]
                            user_order.append([row[0], row[1], q, rate])
            else:
                print(user_order)
                break

#ORDER CANCELLATION
if flag == True:
    cl = input("Do you want to cancel any order?(yes/no) ")
    if cl == "yes":
        while True:
            order = input("Enter the code: ")
            if order!= "":
                qr = int(input("Enter  the quantity: "))
                i=0
                for r in user_order:
                    i+=1
                    if order.lower() == r[0].lower():
                        old = r[2]
                        r[2] = r[2] - qr
                        if r[2] == 0:                            
                            user_order.remove(user_order[i-1])
                        else:
                            r[3] = r[2] * (r[3]/old)
                        break
            else:
                print(user_order)
                break
            
    print('OK')
    print("Please wait while the bill is being generated")

#GENERATING BILL
if flag == True:
    with open("Bill.csv",'w') as b:
        writer = csv.writer(b)
        writer.writerow(["Code","Name", "Quantity", "Rate"])
        total = 0
        for row in user_order:
            total += row[3]
            writer.writerow(row)
        gst = 0.05*total
        cgst = 0.05*total
        t = total+gst+cgst
        writer.writerow(["","","GST 5%", gst])
        writer.writerow(["","","CGST 5%",cgst ])       
        writer.writerow(["", "","TOTAL", t])
    p = Popen('Bill.csv', shell=True)
   

#GETTING DETAILS
if flag == True:
    date = date.today()
    cust_name = input("Enter your name: ")
    phno = input("Enter your phone number: ")
    qry = "insert into customer(name, date, total_bill, ph_no) values(%s, %s, %s, %s)"
    val = (cust_name, date, t, phno)
    c.execute(qry, val)
    conn.commit()
    print("\t\t\tTHANK YOU\tVISIT AGAIN")

#ADDING PLOT DETAILS
if flag == True:    
    query = "select count from plot where type = %s and date = %s"
    values = (plotime, date)
    c.execute(query,values)
    output = c.fetchall()
    if output == []:
        query = "insert into plot(date, type, count) values(%s, %s, %s)"
        values = (date, plotime, 1)
        c.execute(query, values)
        conn.commit()
    else:
        query = "update plot set count = count + 1 where type = %s and date = %s"
        values = (plotime, date)
        c.execute(query,values)
        conn.commit()

conn.close()
c.close()


    
    
