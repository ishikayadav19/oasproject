from django.shortcuts import render, redirect
from . models import Enquiry,AdminLogin, tbl_session , tbl_course, student
import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.cache import cache_control
from . import smssender
# Create your views here.
def index(req):
    return render(req,'index.html')
def about(req):
    return render(req, 'about.html')
def contact(req):
    if req.method=="POST":
        name =req.POST['name']                                       
        gender=req.POST['gender']
        address =req.POST['address']
        contactno =req.POST['contactno']
        emailaddress =req.POST['emailaddress']
        enquirytext =req.POST['enquirytext']
        enquirydate = datetime.datetime.today()
        enq= Enquiry(name=name,gender=gender,address=address,contactno=contactno,emailaddress=emailaddress,enquirytext=enquirytext,enquirydate=enquirydate)
        enq.save()
        smssender.sendsms(contactno)
        msg="Your Enquiry is submitted successfully"
        return render(req,'contact.html', {'msg':msg})
    return render(req,'contact.html')

def login(req):
    return render(req,'login.html')
def enquiry(req):
    return render(req,'enquiry.html')


def logcode(req):
    if req.method=="POST":
        usertype=req.POST['usertype']
        userid=req.POST['userid']
        password=req.POST['password']
        if usertype=="admin":
            try:
                user=AdminLogin.objects.get(userid=userid,password=password)
                if user is not None:
                    req.session['adminid']=userid
                    return redirect('admindash')
            except ObjectDoesNotExist:
                    return render(req,'login.html',{'msg':'Invalid User'})
            
        elif usertype == "student":
            try:
                stu = student.objects.get(emailaddress = userid, password= password)
                if stu is not None:
                    req.session['studentid']=userid
                    return redirect('studentdash')
            except ObjectDoesNotExist:
                return render(req,'login.html',{'msg':'Invalid User'})
    

def organization(req):
    return render(req, 'organization.html')
def biotechpark(req):
    return render(req, 'biotechpark.html')
def locations(req):
    return render(req, 'locations.html')
def certifications(req):
    return render(req, 'certifications.html')
def ourcollab(req):
    return render(req, 'ourcollab.html')
def knowledge(req):
    return render(req, 'knowledge.html')
def outreach(req):
    return render(req, 'outreach.html')
def ceo(req):
    return render(req, 'ceo.html')
def distinguished(req):
    return render(req, 'distinguished.html')
def scientificstaff(req):
    return render(req, 'scientificstaff.html')
def administration(req):
    return render(req, 'administration.html')
def technicalsupport(req):
    return render(req, 'technicalsupport.html')


@cache_control(no_cache=True, must_revalidate= True ,no_store=True )
def adminlayout(req):
    try:
     if req.session['adminid'] != None:
         return render(req,'adminlayout.html')
     else:
         return redirect('login')
    except KeyError:
         return redirect('login')
     
def showenquiry(request):
    sh =Enquiry.objects.all()
    return render(request,"showenquiry.html",{'Show':sh})
def delenq(req,id):
    enq=Enquiry.objects.get(id=id)
    enq.delete()
    return redirect("showenquiry")

def addsession(req):
    return render(req,'addsession.html')
def assave(req):
    session = req.POST['session']
    created_date = timezone.now()
    ads = tbl_session(session=session,created_date=created_date)
    ads.save()
    return redirect('viewsession')
def addcourse(req):
    ch = tbl_session.objects.all()
    if req.method=='POST':
        course_Session = req.POST['course_Session']
        course_name = req.POST['course_name']
        course_duration = req.POST['course_duration']
        course_fees = req.POST['course_fees']
        created_date = timezone.now()
        cor = tbl_course(course_Session=course_Session,course_name=course_name,course_fees=course_fees,created_date=created_date,course_duration=course_duration)
        cor.save()
        return redirect('viewcourse')
    return render(req,'addcourse.html',{'ch':ch})
def viewcourse(req):
    vcor = tbl_course.objects.all()
    return render(req,'viewcourse.html',{'vcor':vcor})
def viewsession(req):
    vsess = tbl_session.objects.all()
    return render (req,'viewsession.html',{'vsess':vsess})
def delcourse(req,id):
    vcor=tbl_course.objects.get(id=id)
    vcor.delete()
    return redirect("viewcourse")
def delsession(req,id):
    shsess=tbl_session.objects.get(id=id)
    shsess.delete()
    return redirect("viewsession")

def editsession(req,id):
    ab= tbl_session.objects.get(id=id)
    return render(req,"editsession.html",{'ab':ab})

def updatesession(req):
    if req.method=="POST":
        id=req.POST['id']
        session = req.POST['session']
        created_date = timezone.now()
        tbl_session.objects.filter(id=id).update(session=session,created_date=created_date)
        return redirect('viewsession')
def editcourse(req,id):
    ba = tbl_course.objects.get(id=id)
    c = tbl_session.objects.all()
    return render (req,"editcourse.html",{'ba':ba,'c':c})
def updatecourse(req):
    if req.method=="POST":
         id=req.POST['id']
         course_Session = req.POST['course_Session']
         course_name =req.POST['course_name']
         course_duration = req.POST['course_duration']
         course_fees = req.POST['course_fees']
         created_date = timezone.now()
         tbl_course.objects.filter(id=id).update(course_Session=course_Session,course_name=course_name,course_fees=course_fees,created_date=created_date,course_duration=course_duration)
         return redirect('viewcourse')
    
def addstudent(req):
    if req.method=="POST":
        name = req.POST['name']
        emailaddress= req.POST['emailaddress']
        contactno = req.POST['contactno']
        gender = req.POST['gender']
        stu = student(name=name, emailaddress=emailaddress, contactno=contactno, gender=gender, password = "12345",fees=0)
        stu.save()
        subject = 'Welcome to Biotech Park Lucknow  Your Online Admission Details'
        message = f'''
        Dear {name},
        Welcome to Biotech Park Lucknow!
        We are thrilled to have you join our community. Below are your login details to access the Nou Egyan portal for your online admission process:
        Portal Link: biotechpark.org.in
        Username:{emailaddress}
        Password:{12345}

        Important Instructions:

        1.Log In: Use the provided credentials to log into Biotech park.
        2.Complete Admission Form: Fill out the online admission form with accurate details.
        3.Submit Required Documents: Upload all necessary documents as specified on the portal.
        4.Check Status: Regularly check your portal for updates on your admission status.
        5.Should you encounter any issues or have any questions, please do not hesitate to reach out to our support team at [Insert Contact Information].

        We look forward to your successful admission and to welcoming you to Biotech Park Lucknow!

        Best regards,

        [Rohit Kumar]
        [CTO Softpro India]
        Biotech Park Lucknow
        [7080102008]
        [softproindia.in]


        

        Please keep this information secure and do not share it with anyone.
        '''
        from_email = 'ishikayadav19125@gmail.com'
        recipient_list = [emailaddress]

        # Send email
        send_mail(subject, message, from_email, recipient_list)
        # Add success message and redirect
        messages.success(req, 'Registration successful! Please check your email for confirmation.')
        return redirect('addstudent')
    return render(req,'addstudent.html')


def editstudent(req,sid):
    std = student.objects.get(sid=sid)
    return render (req,"editstudent.html",{'std':std,})


def updatestudent(req):
    if req.method=="POST":
         sid=req.POST['sid']
         name = req.POST['name']
         emailaddress =req.POST['emailaddress']
         contactno = req.POST['contactno']
         gender = req.POST['gender']
         student.objects.filter(sid=sid).update(name=name,emailaddress=emailaddress,contactno=contactno,gender=gender)
         return redirect('viewstudent')
    
def delstudent(req,sid):
    dstd =student.objects.get(sid=sid)
    dstd.delete()
    return redirect("viewstudent")

         
def viewstudent(req):
    vstd = student.objects.all()
    return render(req,'viewstudent.html',{'vstd':vstd})
@cache_control(no_cache=True, must_revalidate= True ,no_store=True )
def studentdash(req):
    if 'studentid' in req.session :
        studentid = req.session['studentid']
        stu = student.objects.get(emailaddress=studentid)
        asign=""
        if stu.status=="A":
            asign="yes"
        return render(req,'studentdash.html',{'asign': asign,'stu':stu})
    else:
        return redirect('login')

def stdapplication(req):
    try:
        if req.session['studentid']!=None:
            stuid = req.session['studentid']
            stu=student.objects.get(emailaddress = stuid)
            ses = tbl_session.objects.all()
            course = tbl_course.objects.all()
            return render(req,'stdapplication.html',{'stu':stu,'ses':ses,'course':course})
    except KeyError:
        return redirect('login')
    
def saveinfo(req):
    if req.method=="POST":
        name=req.POST['name']
        fname=req.POST['fname']
        mname=req.POST['mname']
        gender=req.POST['gender']
        contactno = req.POST['contactno']
        dob = req.POST['dob']
        emailaddress =req.POST['emailaddress']
        aadharno = req.POST['aadharno']
        address = req.POST['address']
        session=req.POST['session']
        course = req.POST['course']
        hs_percent = req.POST['hs_percent']
        inter_percent = req.POST['inter_percent']
        c= tbl_course.objects.get(course_name = course)
        fees = c.course_fees
        course_duration = c.course_duration
        student.objects.filter(emailaddress=emailaddress).update(name=name,fname=fname,mname=mname,gender=gender,contactno=contactno,dob=dob,aadharno=aadharno,session=session,address=address, course=course,fees=fees,hs_percent=hs_percent,inter_percent=inter_percent,course_duration=course_duration)
        return redirect('stdapplication')

def uploaddoc(req):
    if req.method== "POST":
         stuid = req.session['studentid']
         stu = student.objects.get(emailaddress=stuid)
         pic = req.FILES['pic'] 
         aadharpic = req.FILES['aadharpic']
         hs_marksheet = req.FILES['hs_marksheet']        
         inter_marskheet = req.FILES['inter_marksheet']
         sign = req.FILES['sign']
         fs = FileSystemStorage()
         picfile = fs.save(pic.name,pic)
         aadharfile = fs.save(aadharpic.name,aadharpic)
         hsfile = fs.save(hs_marksheet.name, hs_marksheet)
         interfile = fs.save(inter_marskheet.name,inter_marskheet)
         signfile = fs.save(sign.name,sign)
         stu.pic=picfile
         stu.aadharpic =aadharfile
         stu.hs_marksheet = hsfile
         stu.inter_marksheet = interfile
         stu.sign = signfile
         stu.application_status="C"
         stu.save()
         return redirect('studentdash')


def verifydoc(req):
    students=student.objects.filter(application_status="C")
    return render(req,"verifydoc.html",{'students':students})

def verifystu(req,sid):
     student.objects.filter(sid=sid).update(application_status="V")
     return redirect('verifydoc')

def payfees(req):
    studentid = req.session['studentid']
    stu = student.objects.get(emailaddress = studentid)
    vs=""
    if stu.application_status=="V":
        vs="yes"
    return render(req,'payfees.html',{'stu':stu,'vs':vs})

def finalsubmit(req):
    studentid = req.session['studentid']
    stu = student.objects.get(emailaddress = studentid)
    if req.method=="POST":
        fees_ss=req.FILES['fees_ss']
        fs = FileSystemStorage()
        feesfile=fs.save(fees_ss.name,fees_ss)
        stu.fees_ss=feesfile
        stu.fees_status = "P"
        stu.save()
        subject = '📢📢 Congratulations! Your Admission is Confirmed 📢📢'
        message = f'''
         Dear [{stu.name}],
         Here are the details of your admission
         Name: [{stu.name}]
         Course Enrolled: [{stu.course}]
         Session: [{stu.session}]
         We look forward to welcoming you to our campus and are excited to have you join our academic community. Please make sure to keep an eye on your email for any further instructions and important updates regarding the start of your course and orientation activities.

         If you have any questions or need further assistance, feel free to contact our support team at [Support Email] or [Support Phone Number].

         Once again, congratulations and best wishes for your upcoming academic journey!

         Warm regards,

        [Rohit Kumar]
        [CTO Softro india]
        [Softpro India Computer Technology Lucknow]
        [7080102008]
     
        '''
        from_email = 'ishikayadav19125@gmail.com'
        recipient_list = [stu.emailaddress]
   
        # Send email
        send_mail(subject, message, from_email, recipient_list)

        # Add success message and redirect
        messages.success(req, 'Registration successful! Please check your email for confirmation.')
        return redirect('studentdash')
    return render(req,'finalsubmit.html',{'stu':stu})

def finalverification(req):
    students = student.objects.filter(fees_status="P",status="")
    return render(req,'finalverification.html',{'students':students})

def assign(req,id):
    stu = student.objects.filter(sid=id).update(status="A")
    return redirect('finalstudents')

def finalstudents(req):
    students = student.objects.filter(status="A")
    return render(req,'finalstudents.html',{'students': students})

def logout(req):
    req.session.flush()
    return redirect('login')
@cache_control(no_cache=True, must_revalidate= True ,no_store=True )
def changepass(req):
    userid = req.session.get('studentid')
    user = student.objects.filter(emailaddress = userid )
    if req.method=="POST":
        password = req.POST['password']
        confpass = req.POST['confpass']
        if user:
            if password==confpass  :
             user.password=password
             user.save()
             return redirect('login')
    return render(req,'changepass.html')
@cache_control(no_cache=True, must_revalidate= True ,no_store=True )
def changesave(req):
    if 'studentid' in req.session:
        userid = req.session.get('studentid')
        user = student.objects.filter(emailaddress = userid ).first()
        oldpass = req.POST['changepass']
        newpass = req.POST['password']
        confpass = req.POST['confpass']
        if user:
            if user.password == oldpass:
                if newpass==confpass:
                     user.password= newpass
                     user.save()
                else:
                     return render(req,'changepass.html',{'msg':'New Password and Confirm Password did not Match! Try Again'})    
            else:
                     return render(req,'changepass.html',{'msg':' Your Old Password did not Match! Try Again'})         

        return redirect('login')
    else:
        return redirect('login')

def changepassadmin(req):
    userid = req.session.get('adminid')
    user = AdminLogin.objects.filter(userid = userid )
    if req.method=="POST":
        password = req.POST['password']
        confpass = req.POST['confpass']
        if user:
            if password==confpass:
             user.password=password
             user.save()
             return redirect('login')
    return render(req,'changepassadmin.html')
def changesaveadmin(req):
    if 'adminid' in req.session:
        userid = req.session.get('adminid')
        user = AdminLogin.objects.filter(userid = userid ).first()
        oldpass = req.POST['changepass']
        newpass = req.POST['password']
        confpass = req.POST['confpass']
        if user:
            if user.password == oldpass:
                 if newpass==confpass:
                     user.password= newpass
                     user.save()
                 else:
                     return render(req,'changepassadmin.html',{'msg':'New Password and Confirm Password did not Match! Try Again'}) 
            else:
                     return render(req,'changepass.html',{'msg':' Your Old Password did not Match! Try Again'})         
        
        return redirect('login')
    else:
        return redirect('login')

def admindash(req):
    sc = student.objects.all().count()
    cc = tbl_course.objects.all().count()
    ec = Enquiry.objects.all().count()
    dp = student.objects.filter(application_status="C" ,fees_status="",status="").count()
    fc = student.objects.filter(application_status="V", fees_status ="P", status="").count()
    apc = student.objects.filter(application_status="V", fees_status = "P",status = "A").count()
    return render(req,"admindash.html",{'sc':sc,'cc':cc,'ec':ec,'dp':dp , 'fc':fc,'apc':apc})



   