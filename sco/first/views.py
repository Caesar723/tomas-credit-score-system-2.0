from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import mysql.connector
import re
import csv
import codecs
import datetime
# Create your views here.
pw='20040723caesar'
conect = mysql.connector.connect(user='root', password=pw, host='localhost', database='python1',auth_plugin='mysql_native_password')
home='<a href=http://127.0.0.1:8000/ >返回登陆</a>'

def createUserTable():

    con = conect.cursor()
    con.execute('CREATE TABLE identification(ID int AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(255),Password VARCHAR(255),Class VARCHAR(255))')

def changeScore(Nam,num,reason,conect):

    con = conect.cursor()
    con.execute('UPDATE studentScore SET Score=Score+%s WHERE Name="%s"'%(num,Nam))

    conect.commit()
    con.execute('SELECT Class ,Name,Score  FROM studentScore WHERE Name="%s"'%(Nam))
    get=con.fetchone()
    
    addLog(get[0],Nam,reason,num,conect)
    return get[0]+' '+get[1]+' '+str(get[2])
#def addUser(user,password,conect):
    
def addLog(Class,name,reason,Sc,conect):

    con = conect.cursor()
    con.execute('INSERT INTO ScoreLog(Class,Name,Log,ScoreChange) VALUES ("%s","%s","%s",%s)'%(str(Class),str(name),str(reason),Sc))
    conect.commit()
def getlog(name,conect):
    con = conect.cursor()
    con.execute('SELECT Log,ScoreChange,ID FROM ScoreLog WHERE Name="%s"' %(name))
    get = con.fetchall()
    text=''
    arr=[]
    for i in get:
        arr.append([str(i[0])+'__'+str(i[1]),i[2]])
    
    return arr
def addUser(name,password,clas,conect):
    con = conect.cursor()
    con.execute('INSERT INTO identification(Class,Name,Password) VALUES ("%s","%s","%s")'%(str(clas),str(name),str(password)))
    conect.commit()
def getstu(clas,conect):
    arr=[]
    con = conect.cursor()
    con.execute('SELECT Class ,Name,Score  FROM studentScore WHERE Class="%s"' % (clas))
    get = con.fetchall()
    
    for i in get :
        arr.append(i[0]+'--'+i[1]+'--'+str(i[2]))
        
    
    return arr
def getAllClass(conect):
    con = conect.cursor()
    con.execute('SELECT Class FROM studentScore ')
    get = set(con.fetchall())
    return list(get)
def getalluser(conect):
    con = conect.cursor()
    con.execute('SELECT Name FROM identification ')
    get = list(set(con.fetchall()))
    arr=[]
    for i in get:
        arr.append(i[0])
    return list(arr)
def deletelog(Id,conect):
    con = conect.cursor()
    for iii in Id:
        con.execute('Delete FROM ScoreLog WHERE id=%s' % (iii))
        conect.commit()
    print('delete!')
def checkTeacher(name):
    teacher=['']
def checkStudent(cla,conect):
    
    con = conect.cursor()
    con.execute('SELECT Name,Class,Score FROM studentScore WHERE Class="%s"' %(str(cla)))
    students=con.fetchall()
    print(students)
    for i in range(len(students)):
        con.execute('SELECT Log,ScoreChange FROM ScoreLog WHERE Name="%s"'%(students[i][0]))
        get=con.fetchall()
        print(get)
        students[i]=list(students[i])
        for rea in get:
            
            students[i].append((str(rea[0])+'__'+str(rea[1])))
    print(students)
    return students
def load(request):
    conect = mysql.connector.connect(user='root', password=pw, host='localhost', database='python1',auth_plugin='mysql_native_password')
    
    lo="<td><font size=8><center>上海托马斯信誉积分系统</center></td></font>" 
    tit="<td><font size=6><center>输入账号密码</center></td>"
    fail="<td><font size=6><center>输入账号密码(fail)</center></td>"
    body="<td><form name='input' action='' method='post'><center>账号：<input name='name' size=30 ></center></td>" \
       "<td><center>密码：<input type='password' name='secret' size=30 ></center></td>" \
       "<td><center><input type='submit' value='提交' name='create' style='width:200px; height:50px;background-color:#FFFFFF'></form><form name='in' action='' method='post'><input type='submit' value='注册' name='create' style='width:200px; height:50px;background-color:#FFFFFF'></form></center></font></td>"
    
    if request.method=='GET':

        return HttpResponse(lo+tit+body)
    if request.method=='POST':
        print(request.POST)
        try:
            if request.POST['cla']!='':
                print(request.POST)
                return primary(request,request.POST['cla'],"pass")
        except :
            pass
        if request.POST['create']=='注册':
            return HttpResponseRedirect('register/')
        if request.POST['create']=='提交':
            con = conect.cursor()
            con.execute('SELECT Class FROM identification WHERE Name="%s" AND Password="%s"' %(str(request.POST['name']),str(request.POST['secret'])))
            get=con.fetchone()
            print(get)
            if get!=None:
                request.method='GET'
                return primary(request,get[0],"pass")
                #return  redirect(primary,Pass="pass",data=get[0])
            else:
                return HttpResponse(lo+fail+body)

def reg(request):
    conect = mysql.connector.connect(user='root', password=pw, host='localhost', database='python1',auth_plugin='mysql_native_password')
    
    tit="<td><font size=6><center>注册</center></td>"
    fail="<td><font size=6><center>注册失败</center></td>"
    success="<td><font size=6><center>注册(Success)</center></td>"
    lo = "<td><form name='input' action='' method='post'><center>账号：<input name='name' size=30 ></center></td>" \
         "<td><center>密码：<input type='password' name='secret' size=30 ></center></td>" \
         "<td><center>密码确认：<input type='password' name='Dsecret' size=30 ></center></td>" \
         
    send="<center><input type='submit' value='提交' name='create' style='width:200px; height:50px;background-color:#FFFFFF'></form></center></font></td>"
    lo+="<center><select size='4' name='choose'>"
    for i in getAllClass(conect):
        lo+="<option value="+i[0]+">"+i[0]+"</option>"
    lo+="</select></center>"+send
    if request.method == 'GET':
        return HttpResponse(home+tit+lo)
    if request.method == 'POST':
        print(request.POST)
        alluser=getalluser(conect)
        if request.POST['secret']!='' and request.POST['secret']==request.POST['Dsecret'] and request.POST['choose']!='' and not(request.POST['name'] in alluser):
            
            try:
                addUser(request.POST['name'],request.POST['secret'],request.POST['choose'],conect)
                return HttpResponse(home+success+lo)
            except:
                
        #if request.POST[]
                return HttpResponse(home+fail+lo)
        else:
            return HttpResponse(home+fail+lo)
def primary(req,data=None,Pass="NO"):
    conect = mysql.connector.connect(user='root', password=pw, host='localhost', database='python1',auth_plugin='mysql_native_password')
    #name=req.POST['people']
    print(Pass)
    log=''
    allC=getAllClass(conect)
    print(allC)
    level='command'
    if data=='super':
        level='super'
        data=allC[0][0]
    if req.method == 'POST' and req.POST['lev']=="super":
        level='super'
        
    try:
        if req.POST['send']=='Delete':
            #print(req.POST.getlist('numid'),'hhhlh')
            deletelog(req.POST.getlist('numid'),conect)
        if req.POST['send']=='Get all student csv':
            now=datetime.datetime.now()
            alls=HttpResponse(content_type="text/text")
            alls.write(codecs.BOM_UTF8)
            alls['Content-Disposition']='attachment;filename="'+req.POST['cla']+str(now.year)+'/'+str(now.month)+'/'+str(now.day)+'AllStudent.csv"'
            w=csv.writer(alls)
            print('okkkk')
            allstudent=checkStudent(req.POST['cla'],conect)
            
            print(allstudent,'okkkk')
            title=['name','class','score','log']
            w.writerow(title)
            for inp in allstudent:
                arr=[]
                for en in inp:
                    arr.append(str(en))
                w.writerow(arr)
            return alls
    except:
        pass
    try:
        people=req.POST['people']
        c=re.compile('-\S+-')
        nameLog=(c.findall(req.POST['people'])[0]).replace('-','')
        
        log=getlog(nameLog,conect)
       
    except:
        pass
    
    try:
        sco=req.POST['score']
        c=re.compile('-\S+-')
        sc=re.compile('-\d+')
        name=(c.findall(req.POST['people'])[0]).replace('-','')
        changeScore(name,sco,req.POST['reason'],conect)
        insco=(sc.findall(req.POST['people'])[0]).replace('-','')
        #print(insco)
        newsco=str(int(insco)+int(sco))
        #print(newsco)
        people=people.replace(str(insco),newsco)
        #print(insco,newsco,'ok')
    except:
        pass
    
    #a=['ss','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv','sibibisibisbibs','suvhusvuhsvuhv']
    #title="<td><font size=10><center>阿爸吧</center></font></td>"
    stu=getstu(req.POST['cla'] if req.method == 'POST' else data,conect)
    #print(stu)

    if req.method == 'POST':
        print(req.POST)
    return render(req,'homeP.html',{'data':stu,'class':req.POST['cla'] if req.method == 'POST' else data,'get':people if req.method == 'POST' else '','log':log,'allClass':allC,'level':level})
    #return HttpResponse(title+""+con+''+test+'')













'''
   con="<form name='inp' action='' method='post'>"
    test="<div><form name='input' action='' method='post'><input name='name' style='background-position: right  7px center;'>" \
         "<input type='password' name='secret' style='background-position: right  7px center;'></form></div>"
    for i in range(len(a)):
        #print(i)

        con+="<input type='submit' value="+a[i]+" name='people' style='width:400px; height:28px;background-color:"+("#A0A0A0'" if req.method == 'POST' and req.POST['people']==a[i] else "#FFFFFF'")+">"
        if i==0 and req.method == 'POST':
            for ii in a:
                if ii==req.POST['people']:

                    con+=''+''
                    break
            con+='<br>'
        else:
            con+='<br>'
    con+='</form>'
    
'''