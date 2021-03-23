import sqlite3
import datetime
import sys
import getpass
import random
import time

#connect with the test database
db = sys.argv[1]
conn= sqlite3.connect(db)
cursor = conn.cursor()
print("Opened database successfully")

#if user type==a, jump to agentManu
#if user type==o, jump to officeManu
def main():
    while True:
        user=login()
        if user!=None:
            break
    if user[0]=="a":
        agentTurn(user[1])
    elif user[0]=="o":
        officeTurn()
    else:
        print("Invalid user type, something wrong in db.")

#login to database
def login():
    trueUser=False
    while trueUser==False:
        user = validateUser()

        #let user prompt again if needed or just quit
        if user==None:
            tmp=input("Wrong id or password, exit (press q) or try again (press any other key) :").lower()
            if  tmp=="q":
                exit()
            else:
                break
        else:
            trueUser=True

    return user

#validate the userName and the password
def validateUser():
    username = input("User ID is: ")
    password = getpass.getpass("Password is:")
    #pass username and password to users table and validate
    cursor.execute("""SELECT utype,uid FROM users WHERE uid = ? AND pwd = ? COLLATE NOCASE""", (username, password))
    user=cursor.fetchone()
    return user

#agent main menu,back to here when function are done
def agentTurn(userId):
    print("Welcome agent user!")
    print("which function do you want to select?")
    print("")
    print("1:Register a birth")
    print("2:Register a marriage")
    print("3:Renew a vehincle registration")
    print("4:Process a bill of sale.")
    print("5:Process a payment.")
    print("6:Get a driver abstract.")
    print("7:Exit")
    print("")
    Enter_num=input("Please enter the number that you want to choose:")
    if Enter_num=="1":
        register_birth(userId)
    elif Enter_num=="2":
        register_marriage(userId)
    elif Enter_num=="3":
        renew_veh_reg(userId)
    elif Enter_num=="4":
        bill_of_sell(userId)
    elif Enter_num=="5":
        payment(userId)
    elif Enter_num=="6":
        get_driver_abstract(userId)
    elif Enter_num=="7":
        exit()
    else:
        print("wrong input")
        agentTurn(userId)

#check if the person already exists in the database
def findPerson(firstName,lastName):
    cursor.execute("""SELECT fname,lname FROM persons WHERE fname =:fnameInput AND lname =:lnameInput COLLATE NOCASE""" ,{"fnameInput":firstName, "lnameInput":lastName})
    personExistence=bool(cursor.fetchone())
    return personExistence

#if person not in databse, add person to database with this func
def addPerson(firstName,lastName,userId):
    print("")
    print("Person you find not in database,provide these information if u want")
    birthDay=checkBirthDate()

    #confirm if user willing to input birth place, address, phoneNo
    #and check the right format
    while True:
        bplace = input("Input birth place or press n to neglect: ").lower()
        if bplace=="n":
            bplace =None
            break
        else:
            if not checkLength(bplace,20):
                print("Wrong legth of birth place")
            elif checkLength(bplace,20):
                break

    while True:
        address = input("Address or press n to neglect: ").lower()
        if address=="n":
            address=None
            break
        else:
            if not checkLength(address,30):
                print("Wrong legth of address")
            elif checkLength(address,30):
                break

    while True:
        phoneNo = input("Phone number or press n to neglect: ").lower()
        if phoneNo=="n":
            phoneNo =None
            break
        else:
            if not (checkLength(phoneNo,12) or checkDigit(phoneNo)) :
                print("Wrong length or including nondigit in phone number")
            elif (checkLength(phoneNo,12) and checkDigit(phoneNo)) :
                break

    #commit the collected data into db file, create the new person profile
    cursor.execute("""INSERT INTO persons VALUES (:fname,:lname,:bdate,:bplace,:add,:phone COLLATE NOCASE)""",{"fname":firstName,"lname":lastName,"bdate":birthDay,"bplace":bplace,"add":address, "phone":phoneNo})
    conn.commit()
    print("add %s %s successfully."%(firstName,lastName))

#check if the str all digits, if the requirements not meet, return to main manu
def checkDigit(value):
    if not value.isdigit():
        print("Do not include nonDigit characters.")
        print("")
        return False
    return True

#check if the name meet the requirements, if the requirements not meet, return to main manu
def checkName(value):
    #check different situations described in eclass form of person`s name
    for i in value:
        if i.isalpha():
            pass
        elif i.isdigit():
            pass
        elif i=="-":
            pass
        else:
            print("i")
            print("Do not input illegal characters")
            return False
    return True

#check the legth of the value, if the length exceed, return to main manu
def checkLength(value,length):
    if len(value)>length:
        print("Too long")
        print("")
        return False
    return True

#check if the str all digits, if the requirements not meet, return to main manu
def checkAlpha(value):
    if not value.isalpha():
        print("Do not include nonAlpha characters.")
        print("")
        return False
    return True

#create the date data and check if the user input illegal
def checkBirthDate():
    None_Leap_Year_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    Leap_Year_days = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    while True:
        date=input("Please input the date of birth(like 20191231) or press n to neglect input:")
        date=date.lower()
        if date=="n":
            break
        if not date.isdigit():
            print("do not enter nondigit")
            continue
        if len(date)!=8:
            print("please enter date with format YYYYMMDD")
            continue
        else:
            year=int(date[0:4])
            month=int(date[4:6])
            day=int(date[6:])

        #check the date is in leap year or not and modify the regulation of the days by leap year
        isLeap_Year = False
        if (year % 4 ==0 and year % 100 !=0) or (year % 100 ==0 and year %400 ==0):
            isLeap_Year=True

        if month<1 or month>12:
            print("Illegal month")
            continue
        if isLeap_Year:
            if day<1 or day>Leap_Year_days[month]:
              print("Illegal day")
              continue

        else:
            if day<1 or day>None_Leap_Year_days[month]:
                print("Illegal day")
                continue
        date=str(year)+"-"+str(month)+"-"+str(day)
        return date

def register_birth(userId):
    #enter basic information of baby and do the check
    while True:
        print("Please enter following information:")

        fname = input("First name: ").lower()
        if not checkLength(fname,12):
            print("First name format not right, return to main menu")
            break
        if not checkName(fname):
            print("First name format not right, return to main menu")
            break

        lname = input("Last name: ").lower()
        if not checkLength(lname,12):
            print("Last name format not right, return to main menu")
            break
        if not checkName(lname):
            print("Last name format not right, return to main menu")
            break

        #find if the baby already exists, since we assume same name baby can not exist(not case sensitive)
        #if new born exists, jump back to main menu
        newBornExistence=findPerson(fname,lname)
        if newBornExistence==False:
            pass
        else:
            print("Newborn exists, cant proceed, return to main menu")
            break

        gender = input("Gender: ").lower()
        if not checkLength(gender,1):
            print("Gender format not right, return to main menu")
            break
        if not checkAlpha(gender):
            print("Gender format not right, return to main menu")
            break

        birthDate=checkBirthDate()
        if birthDate=="Back to main menu":
            break

        regDay=datetime.date.today()

        #find unused regNo use while loop
        while True:
            randint=random.randint(0,99999)
            cursor.execute("""SELECT * FROM births WHERE regno =:randint""",{"randint":randint})
            if (not bool(cursor.fetchone())):
                regNo=randint
                break

        #find registration place
        cursor.execute("""Select city From users Where uid =:userId""",{"userId":userId})
        temp=cursor.fetchone()
        rPlace=temp[0].lower()

        #check birth place format
        bplace = input("Birth Place: ").lower()
        if not checkLength(bplace,20):
            print("Birth Place format not right, return to main menu")
            break

        #check parent`s format
        ffname = input("First Name of Father: ").lower()
        if not checkLength(ffname,12):
            print("Father first name format not right, return to main menu")
            break
        if not checkName(ffname):
            print("Father first name format not right, return to main menu")
            break

        flname = input("Last Name of Father: ").lower()
        if not checkLength(flname,12):
            print("Father last name format not right, return to main menu")
            break
        if not checkName(flname):
            print("Father last name format not right, return to main menu")
            break

        #check father exists in database or not, if not exists, insert into database
        if findPerson(ffname,flname)==False:
                    addPerson(ffname,flname,userId)

        #same for mother
        mfname = input("First Name of Mother: ").lower()
        if not checkLength(mfname,12):
            print("Mother first name format not right, return to main menu")
            break
        if not checkName(mfname):
            print("Mother first name format not right, return to main menu")
            break

        mlname = input("Last Name of Mother: ").lower()
        if not checkLength(mlname,12):
            print("Mother last name format not right, return to main menu")
            break
        if not checkName(mlname):
            print("Mother last name format not right, return to main menu")
            break

        if findPerson(mfname,mlname)==False:
            addPerson(mfname,mlname,userId)

        #find address and phone number by using mother`s address and phone number
        cursor.execute("""SELECT address, phone FROM persons WHERE fname =:mfname AND lname =:mlname COLLATE NOCASE""",{"mfname":mfname,"mlname":mlname})
        temp=cursor.fetchone()
        address,phone=temp[0],temp[1]

        #fill info to births table
        cursor.execute("""INSERT INTO births VALUES (:regno,:fname,:lname,:regdate,:regplace,:gender,:f_fname,:f_lname,:m_fname,:m_lname)""",
                        {"regno":regNo,"fname":fname,"lname":lname,"regdate":regDay,"regplace":rPlace,"gender":gender,"f_fname":ffname,
                        "f_lname":flname,"m_fname":mfname,"m_lname":mlname})
        conn.commit()

        #fill info ot persons table
        cursor.execute("""INSERT INTO persons VALUES (:fname,:lname,:bdate,:bplace,:address,:phone)""",
              {"fname":fname,"lname":lname,"bdate":birthDate,"bplace":bplace,"address":address,"phone":phone})
        conn.commit()
        print("Birth record succesfully added")
        print("")
        break
    agentTurn(userId)

def register_marriage(userId):
    while True:
        print("Please enter following information:")
        #find unused regNo
        while True:
            randint=random.randint(0,99999)
            cursor.execute("""SELECT * FROM marriages WHERE regno =:randint""",{"randint":randint})
            if (not bool(cursor.fetchone())):
                regNo=randint
                break

        #find registration date
        regDay=datetime.date.today()

        #find registration place
        cursor.execute("""Select city From users Where uid =:userId""",{"userId":userId})
        temp=cursor.fetchone()
        rPlace=temp[0]

        #check p1 and p2 existent in database, append if not exist
        p1_fname=input("First Name of p1:").lower()
        if not checkLength(p1_fname,12):
            print("p1_fname format error, return to main menu")
            break
        if not checkName(p1_fname):
            print("p1_fname format error, return to main menu")
            break

        p1_lname=input("Last Name of p1:").lower()
        if not checkLength(p1_lname,12):
            print("p1_lname format error, return to main menu")
            break
        if not checkName(p1_lname):
            print("p1_lname format error, return to main menu")
            break

        if findPerson(p1_fname,p1_lname)==False:
            addPerson(p1_fname,p1_lname,userId)

        p2_fname=input("First Name of p2:").lower()
        if not checkLength(p2_fname,12):
            print("p2_fname format error, return to main menu")
            break
        if not checkName(p2_fname):
            print("p2_fname format error, return to main menu")
            break

        p2_lname=input("Last Name of p2:").lower()
        if not checkLength(p2_lname,12):
            print("p2_lname format error, return to main menu")
            break
        if not checkName(p2_lname):
            print("p2_lname format error, return to main menu")
            break

        if findPerson(p2_fname,p2_lname)==False:
            addPerson(p2_fname,p2_lname,userId)

        cursor.execute("""Insert INTO marriages VALUES (:regno,:regdate,:regplace,:p1_fname,:p1_lname,:p2_fname,:p2_lname)""",
                  {"regno":regNo,"regdate":regDay,"regplace":rPlace,"p1_fname":p1_fname,"p1_lname":p1_lname,"p2_fname":p2_fname,"p2_lname":p2_lname})
        conn.commit()
        print("Regist successfully, wish you two always be in love")
        print("")
        break
    agentTurn(userId)

def renew_veh_reg(userId):
    while True:
        #get the registration number and check
        regno=input("Please input the registration number:")
        if not checkDigit(regno):
            print("regno cant include nondigit, return to main menu")
            break

        regno=int(regno)
        cursor.execute("""SELECT regno, expiry FROM registrations WHERE regno=:regno""",{"regno":regno})
        tmp=cursor.fetchone()
        if not bool(tmp):
            print("Curret database do not include your registration number, can not proceed, return to manu")

        #find the expiry date and compare it with the date of today
        expiryDate=tmp[1]
        print(type(expiryDate))
        expiryYear=expiryDate[0:4]
        expiryMonth=expiryDate[5:7]
        expiryDay=expiryDate[9:11]
        tmpIntExpiryDate=int(expiryYear+expiryMonth+expiryDay)
        print(tmpIntExpiryDate)

        toDay=datetime.date.today()
        toDay=str(toDay)
        toDayYear=toDay[0:4]
        toDayMonth=toDay[5:7]
        toDayDay=toDay[9:11]
        tmpIntRegDate=int(toDayYear+toDayMonth+toDayDay)
        print(tmpIntRegDate)

        #do the comparison and apply the calulated expiryDate to the new expiryDate
        if tmpIntExpiryDate<=tmpIntRegDate:
            toDayYear=int(toDayYear)
            toDayYear+=1
            expiryDate=str(toDayYear)+"-"+toDayMonth+"-"+toDayDay
        else:
            expiryYear=int(expiryYear)
            expiryYear+=1
            expiryDate=str(expiryYear)+"-"+expiryMonth+"-"+expiryDay

        #commit the data
        cursor.execute("""UPDATE registrations SET expiry =:expiryDate WHERE regno =:regno""",{"expiryDate":expiryDate, "regno":tmp[0]})
        conn.commit()
        print("registration updated successfully")
        print("")
        break
    agentTurn(userId)


def bill_of_sell(userId):
    #judgment whether input name is exist in registrations
    while True:
        while True:
            cname=input("the name of current owner:")
            flag=checkName(cname)
            if not flag:
                pass
            else:
                break
        today_date = time.strftime('%Y-%m-%d')

        cursor.execute("""select fname||lname, vin from registrations where fname||lname=:name COLLATE NOCASE and expiry !=:expiry """,{"name":cname,"expiry":today_date})
        e_cname=cursor.fetchall()

        if len(e_cname) == 0:
            print('WORNING: NAME DOES NOT EXIST')
            continue
        else:
            break
    #judgment whether input vin is exist in registrations
    while True:
        flag = False
        vin = input('the vin of a car:')
        for i in e_cname:
            if flag == True:
                break
            for j in i:
                if vin.lower() != j.lower():
                    flag = False
                    continue
                else:
                    flag = True
                    correct_vin = j
                    break
        if flag == True:
            break
        if flag == False:
            print('WORNING: VIN DOES NOT EXIST')



    #judgment input length
    while True:
        while True:
            n_name=input("the name of new owner(like:JohnSnow [no space between first name and last name])):")
            flag=checkName(n_name)
            if not flag:
                pass
            else:
                break

        today_date = time.strftime('%Y-%m-%d')
        cursor.execute("""select fname, lname from persons where fname||lname=:name COLLATE NOCASE""",{"name":n_name})
        e_n_name=cursor.fetchone()
        if e_n_name == None:
            print('WORNING: NAME DOES NOT EXIST')
            continue
        elif cname.lower() == n_name.lower():
            print('You Cannot buy your car')
            continue
        else:
            break

    #judgment input length
    while True:
        new_p_number = input('plate number for the new registration:')
        if len(new_p_number)>7:
            print('plate number too long')
            continue
        elif len(new_p_number)==0:
            print('Cannot enter anything')
            continue
        else:
            break
    #let year +1
    today_date=datetime.datetime.now()
    new_date=datetime.datetime(today_date.year+1,today_date.month,today_date.day)
    new_date=new_date.strftime('%Y-%m-%d')
    today_date=today_date.strftime('%Y-%m-%d')


    cursor.execute('update registrations set expiry = ? where fname||lname=? and vin=? COLLATE NOCASE;',(today_date,e_cname[0][0],vin))
    conn.commit()
    #produce a new regno
    cursor.execute('select MAX(regno) from registrations')
    row_regno=cursor.fetchone()
    row_regno=','.join(map(str,row_regno))
    new_regno=int(row_regno)+1
    #print(new_regno)
    #insert new owner information
    cursor.execute('insert into registrations values(?,?,?,?,?,?,?)',(new_regno,today_date,new_date,new_p_number,correct_vin,e_n_name[0],e_n_name[1]))
    conn.commit()
    print('Success! You have finished')
    agentTurn(userId)

def payment(userId):
    #judge whether inout tno is int type and whether this tno has paid today, if paid, we pass and pay another
    while True:
        try:
            while True:

                tno=int(input('please enter the tickets number:'))
                today_date = time.strftime('%Y-%m-%d')
                cursor.execute("""select pdate from payments where pdate=:pdate and tno=:tno""",{"pdate":today_date,"tno":tno})
                judge1=cursor.fetchone()
                if judge1!=None:
                    print('you have paid today, please pay another')
                    continue
                else:
                    break
                break
        except ValueError:
            print('Please enter integer')
            continue
        cursor.execute("""select * from tickets where tno=:tno""",{"tno":tno})
        ticket_num= cursor.fetchone()
        if ticket_num == None:
            print('WORNING: TICKET NUMBER DOES NOT EXIST')
            continue
        else:
            break
        break
    #judge whether input amount is integer and cant input 0
    while True:
        try:
            amount=int(input('please enter the payment amount:'))
        except ValueError:
            print('Please enter integer')
            continue
        if amount == 0:
            print('WORNING: you cant pay 0')
            continue
        else:
            break
        break
    #calculate fine that we need to pay and total_payment(past pay add this times amount)
    cursor.execute("""select fine from tickets where tno=:tno""",{"tno":tno})
    fine=cursor.fetchone()
    fine=','.join(map(str,fine))
    print('')
    print('Fine that you need to pay:'+fine)
    fine=int(fine)
    cursor.execute("""select SUM(amount) from payments where tno=:tno""",{"tno":tno})
    paid_amount = cursor.fetchone()
    paid_amount=','.join(map(str,paid_amount))
    if paid_amount=='None':
        print('The amount that you have paid:0')
        paid_amount=0
    else:
        print("The amount that you have paid:"+paid_amount)
    total_payment =int(paid_amount)+int(amount)
    print('The total payment that added this times payment:'+str(total_payment))
    print('')
    today_date = time.strftime('%Y-%m-%d')
    #three case that between amount , fine, and total payment
    if  total_payment==fine:
        cursor.execute('insert into payments(tno,pdate,amount) VALUES(?,?,?);',(tno,today_date,amount))
        conn.commit()
        print('Congratulation!!! You have pay all fine.')

    elif total_payment<fine:
        print('You have paid:'+str(amount))
        cursor.execute('insert into payments(tno,pdate,amount) VALUES(?,?,?);',(tno,today_date,amount))
        conn.commit()
    else:
        print('Your payment exceed fine')
    agentTurn(userId)

def get_driver_abstract(userId):
    #judge whether name in registration
    while True:
        while True:
            fname=input('Enter a first name:')
            lname=input('Enter a last name:')
            name=fname+lname
            flag=checkName(name)
            if not flag:
                pass
            else:
                break
        cursor.execute("""select fname||lname from registrations where fname||lname=:name COLLATE NOCASE""",{"name":name})
        e_cname=cursor.fetchone()
        if e_cname == None:
            print('WORNING: NAME DOES NOT EXIST')
            continue
        else:
            break
    #the number of tickets, the number of demerit notices, the total number of demerit points received within the past two years
    cursor.execute("""select COUNT(tno) from tickets left outer join registrations using(regno) where fname||lname =:name and date(vdate)>date('now','-2 years') COLLATE NOCASE""",{"name":name})
    num_tickets1=cursor.fetchone()
    num_tickets1=','.join(map(str,num_tickets1))
    cursor.execute("""select COUNT(ddate) from demeritNotices where fname||lname  =:name and date(ddate)>date('now','-2 years') COLLATE NOCASE""",{"name":name})
    num_d_notice1=cursor.fetchone()
    num_d_notice1=','.join(map(str,num_d_notice1))
    cursor.execute("""select SUM(points) from demeritNotices where fname||lname  =:name and date(ddate)>date('now','-2 years') COLLATE NOCASE""",{"name":name})
    num_d_points1=cursor.fetchone()
    num_d_points1=','.join(map(str,num_d_points1))
    print('')
    print('abstract for past two years:')
    print('number of tockets='+ num_tickets1)
    print('number of demerit notices='+ num_d_notice1)
    print('total number of demerit points ='+ num_d_points1)
    #the number of tickets, the number of demerit notices, the total number of demerit points received within lifetime
    cursor.execute("""select COUNT(tno) from tickets left outer join registrations using(regno) where fname||lname =:name COLLATE NOCASE""",{"name":name})
    num_tickets2=cursor.fetchone()

    num_tickets2=','.join(map(str,num_tickets2))
    cursor.execute("""select COUNT(ddate) from demeritNotices where fname||lname  =:name COLLATE NOCASE""",{"name":name})
    num_d_notice2=cursor.fetchone()
    num_d_notice2=','.join(map(str,num_d_notice2))
    cursor.execute("""select SUM(points) from demeritNotices where fname||lname  =:name COLLATE NOCASE""",{"name":name})
    num_d_points2=cursor.fetchone()
    num_d_points2=','.join(map(str,num_d_points2))
    print('')
    print('abstract within lifetime:')
    print('number of tockets='+ num_tickets2)
    print('number of demerit notices='+ num_d_notice2)
    print('total number of demerit points ='+ num_d_points2)
    # show the ticket number, the violation date, the violation description, the fine,and
    # the registration number and the make and model of the car for which the ticket is issued
    #also let uesr choose whether see more than 5 information
    while True:
        try_again=input('Do you want to see the tickets ordered from the latest to the oldest? if yes press 1, if no press 2:')
        if try_again=='1':
            cursor.execute("""select tno, vdate, violation, fine, regno, make, model from\
            tickets left outer join registrations using (regno) left outer join vehicles using(vin)\
            where fname||lname =:name COLLATE NOCASE order by vdate desc""",{"name":name})
            row=cursor.fetchall()
            if len(row)>=5:
                print(row[0:5])
                while True:
                    option=input('Do you want to see more?(enter 1 for yes or 2 for no):')
                    if option=='1':
                        print(row)
                        break
                    elif option=='2':
                        print('Abstract has already show')
                        break
                    else:
                        print('Error: wrong input')
                        continue
            elif len(row)==0:
                print('No tickets')
            else:
                print(row)
            break
        elif try_again=='2':
            cursor.execute("""select tno, vdate, violation, fine, regno, make, model from\
            tickets left outer join registrations using (regno) left outer join vehicles using(vin)\
             where fname||lname =:name COLLATE NOCASE order by vdate """,{"name":name})
            row=cursor.fetchall()
            if len(row)>=5:
                while True:
                    option=input('Do you want to see more?(enter 1 for yes or 2 for no):')
                    if option=='1':
                        print(row)
                        break
                    elif option=='2':
                        print('Abstract has already show')
                        break
                    else:
                        print('Error: wrong input')
                        continue
            elif len(row)==0:
                print('No tickets')
            else:
                print(row)
            break
        else:
            print('Errow: wrong input')
            continue
    agentTurn(userId)

def officeTurn():
    trueSelect = False
    print("Welcome agent user!")
    print("which function do you want to select?")
    print("")
    print("1.issue the tickets")
    print("2.find car owner")
    print("3.Exit")
    print("")
    #There are two function, one is issue the tickets and another is find a car owner.
    while trueSelect == False:
        choose = input("Your choose is: ")
        if choose == "1":
            issueTicket()
            trueSelect = True
        elif choose == "2":
            findCar()
            trueSelect = True
        elif choose == "3":
            exit()
        else:
            #Only can input 1 or 2, other will return choose.
            print("Invalid number, please check your input number.")
    return

def issueTicket():
    issueT = False
    correctInput = False
    #When thw tickets will be make, the function will end
    while issueT == False:
        #registration number cannot be empty and only input integer.
        registration_N = input("Please input your registration number: ")
        if registration_N.isdigit():
            registration_N = int(registration_N)
            cursor.execute("""SELECT r.fname||r.lname, v.make,v.model,v.year,v.color FROM registrations r,vehicles v WHERE v.vin = r.vin AND r.regno =:regno""",{"regno":registration_N})
            data = cursor.fetchone()
            if data == None:
                print("wrong registration number.")
            else:
                print(data)
                getT = input("Need Ticket the registration?(press 1 to make ticket and other button to exit):")
                if getT == "1":
                    while True:
                        randint = random.randint(0,100000)
                        cursor.execute("""select * from tickets where tno =:t""",{"t":randint})
                        if (not bool(cursor.fetchone())):
                            tno = randint
                            break
                    #check the input date is correct or wrong.
                    while correctInput == False:
                        #leap year will have 29 days in Second month.
                        None_Leap_Year_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                        Leap_Year_days = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                        viodate = input("please input the violation date(YYYY-MM-DD): ")
                        if len(viodate) == 0:
                            #the date will produce automatically.
                            viodate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                            viotext = input("please input the violation text: ")
                            if len(viotext) == 0:
                                print("Text cannot be empty!")
                                continue
                            fine = input("please input the fine amount: ")
                            if len(fine) == 0:
                                print("Cannot be empty,please input a number!")
                            else:
                                #fine must  be the integer.
                                if fine.isdigit():
                                    cursor.execute("INSERT INTO tickets(tno,regno,fine,violation,vdate) VALUES (?,?,?,?,?)",(tno,registration_N,fine,viotext,viodate))
                                    conn.commit()
                                    print("Success make Ticket!")
                                    issueT = True
                                    correctInput = True
                                else:
                                    print("fine must be integer")
                        else:
                            if len(viodate) != 10:
                                print("please make sure the date is yyyy-mm-dd.")
                            else:
                                year = int(viodate[0:4])
                                month = int(viodate[5:7])
                                day = int(viodate[8:10])
                                if month < 1 or month >12:
                                    print("Month cannot be zero or larger than 12")
                                else:
                                    if (year % 4 ==0 and year % 100 !=0) or (year % 100 ==0 and year %400 ==0):
                                        if day <1 or day > Leap_Year_days[month]:
                                            print("Wrong date")
                                            continue
                                    else:
                                        if day <1 or day>None_Leap_Year_days[month]:
                                            print("Wrong date")
                                            continue

                                    viotext = input("please input the violation text: ")
                                    if len(viotext) == 0:
                                        print("Text cannot be empty!")
                                        continue
                                    fine = input("please input the fine amount: ")
                                    if len(fine) == 0:
                                        print("Cannot be empty,please input a number!")
                                    else:
                                        if fine.isdigit():
                                            cursor.execute("INSERT INTO tickets(tno,regno,fine,violation,vdate) VALUES (?,?,?,?,?)",(tno,registration_N,fine,viotext,viodate))
                                            conn.commit()
                                            print("Success make Ticket!")
                                            issueT = True
                                            correctInput = True
                                        else:
                                            print("fine must be integer")
                else:
                    issueT = True
        else:
            print("Registration number must be integer!")
    officeTurn()

def findCar():
    findCar = False
    while findCar == False:
        #choose one or more information will match the solution.
        make = input("please inter the make: ")
        model = input("please inter the model: ")
        color = input("please inter the color: ")
        year = input("please inter the year: ")
        plate = input("please inter the plate: ")
        if len(year) == 0 and len(model) == 0 and len(make) == 0 and len(plate) == 0 and len(color) == 0:
            print("Please input at least one info !")
        else:
            if len(year) == 0:
                year = "%%"
            if len(model) == 0:
                model = "%%"
            if len(make) == 0:
                make = "%%"
            if len(color) == 0:
                color = "%%"
            if len(plate) == 0:
                plate = "%%"
            #know how much solution we can search.
            cursor.execute("SELECT count(distinct v.vin) FROM registrations r,vehicles v WHERE v.vin = r.vin AND v.make LIKE (?) AND v.model LIKE (?) AND v.year LIKE (?) AND r.plate LIKE (?) AND v.color LIKE (?)",(make,model,year,plate,color))
            num = cursor.fetchone()[0]
            if num ==0:
                sol1 = input("Wrong input information or not have this car! Press any button and enter to exit or press enter to try again: ")
                if len(sol1) == 0:
                    continue
                else:
                    print("")
                    break
            if num >= 4:
                select = False
                cursor.execute("SELECT v.make,v.model,v.year,v.color,r.plate FROM registrations r,vehicles v WHERE v.vin = r.vin AND v.make LIKE (?) AND v.model LIKE (?) AND v.year LIKE (?) AND r.plate LIKE (?) AND v.color LIKE (?)",(make,model,year,plate,color))
                solution = cursor.fetchall()
                print(solution)
                while select == False:
                    selectOne = input("please choose the number that you want to select(start from 1): ")
                    if len(selectOne) != 0:
                        if selectOne.isdigit():
                            selectOne = int(selectOne)
                            if selectOne==0:
                                pass
                            elif selectOne > len(solution) :
                                print("Sorry, your input number is larger than total solution! Please try again!")
                            else:

                                make = solution[selectOne-1][0]
                                model = solution[selectOne-1][1]
                                color = solution[selectOne-1][3]
                                year = solution[selectOne-1][2]
                                plate = solution[selectOne-1][4]
                                cursor.execute("SELECT v.make,v.model,v.year,v.color,r.plate,r.regdate,r.expiry,r.fname||r.lname FROM registrations r,vehicles v WHERE v.vin = r.vin AND v.make LIKE (?) AND v.model LIKE (?) AND v.year LIKE (?) AND r.plate LIKE (?) AND v.color LIKE (?) ORDER BY regdate DESC LIMIT 1",(make,model,year,plate,color))
                                print(cursor.fetchone())
                                TwiceCheck = input("Do you want to find another car?(press 1 to check another car,press other or just press ENTER to break): ")
                                if TwiceCheck == "1":
                                    select = True
                                    pass
                                else:
                                    findCar = True
                                    select = True
                        else:
                            print("Only input number,pleasr try again")
                    else:
                        print("please input the number that you want to check!")


            elif num <4 and num > 0:
                secondTime = 0
                cursor.execute("SELECT v.make,v.model,v.year,v.color,r.plate,r.regdate,r.expiry,r.fname||r.lname FROM registrations r,vehicles v WHERE v.vin = r.vin AND v.make LIKE (?) AND v.model LIKE (?) AND v.year LIKE (?) AND r.plate LIKE (?) AND v.color LIKE (?) GROUP BY r.vin ORDER BY regdate DESC",(make,model,year,plate,color))
                print(cursor.fetchall())
                while secondTime != "yes":
                    secondTime = input("Do you want to find another car?(yes or no): ")
                    if secondTime == "no":
                        findCar = True
                        print("")
                        break
                    elif secondTime == "yes":
                        pass
                    else:
                        print("please inter yes or no!")
    officeTurn()


main()
conn.close()
