# Create your views here.
import re
from symbol import return_stmt
from traceback import print_tb
from uuid import RESERVED_FUTURE
from app.serializers import BoxSerializer,BoxSerializer2
from .models import Box,Account
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login,logout
import datetime






@api_view(('GET',))
def logout_page(request):
    logout(request)
    return Response({'message':"Logged out"})

@api_view(('GET','POST'))
def login_page(request):
    if request.method == "POST":
        username = request.data['username']
        password=request.data['password']
        print(request.user)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return Response({"message":"Login done"})
        else:
            return Response({"message":"Invalid Credentials"})
    return Response({"username":"","password":""})



















@api_view(('GET','POST','DELETE'))
def my(request):
    try:
        account=Account.objects.get(user=request.user)
        box=Box.objects.get(Creator=account)
        try:
            srlzr=BoxSerializer(box,many=True)
            return Response(srlzr.data)
        except Box.DoesNotExist:
            return Response({"msg":"You Not Have Any box In Store"})
    except Account.DoesNotExist:
        return Response({"msg":"Login First"})


@api_view(('GET','POST','DELETE'))
def my_filter(request):
    account=Account.objects.get(user=request.user)
    if request.method=='POST':
        try:
            minl=int(request.data['Min_Length'])
            maxl=int(request.data['Max_Length'])
            minw=int(request.data['Min_Width'])
            maxw=int(request.data['Max_Width'])
            minh=int(request.data['Min_Height'])
            maxh=int(request.data['Max_Height'])
            mina=int(request.data['Min_Area'])
            maxa=int(request.data['Max_Area'])
            minv=int(request.data['Min_Volume'])
            maxv=int(request.data['Max_Volume'])
            box=Box.objects.filter(Creator=account,Length__gte=minl,Length__lte=maxl,Height__lte=maxh,Height__gte=minh,Width__lte=maxw,Width__gte=minw,Area__lte=maxa,Area__gte=mina,Volume__gte=minv,Volume__lte=maxv)
            try:
                srlzr=BoxSerializer(box,many=True)
                return Response(srlzr.data)
            except Box.DoesNotExist:
                return Response({"msg":"You Not Have Any box In Store"})
        except Account.DoesNotExist:
            return Response({"msg":"Login First"})
    else:
        dict={
            'Min_Length':"0",
            'Max_Length':"9999",
            'Min_Width':"0",
            'Max_Width':"9999",
            'Min_Height':"0",
            'Max_Height':"9999",
            'Min_Area':"0",
            'Max_Area':"9999",
            'Min_Volume':"9999",
            'Max_Volume':"9999",
        }
        return Response(dict)





@api_view(('GET','POST','DELETE'))
def filter(request):
    if request.method=='POST':
        try:
            minl=int(request.data['Min_Length'])
            maxl=int(request.data['Max_Length'])
            minw=int(request.data['Min_Width'])
            maxw=int(request.data['Max_Width'])
            minh=int(request.data['Min_Height'])
            maxh=int(request.data['Max_Height'])
            mina=int(request.data['Min_Area'])
            maxa=int(request.data['Max_Area'])
            minv=int(request.data['Min_Volume'])
            maxv=int(request.data['Max_Volume'])

            box=Box.objects.filter(Length__gte=minl,Length__lte=maxl,Height__lte=maxh,Height__gte=minh,Width__lte=maxw,Width__gte=minw,Area__lte=maxa,Area__gte=mina,Volume__gte=minv,Volume__lte=maxv)

            try:
                srlzr=BoxSerializer(box,many=True)
                return Response(srlzr.data)
            except Box.DoesNotExist:
                return Response({"msg":"You Not Have Any box In Store"})
        except Account.DoesNotExist:
            return Response({"msg":"Login First"})
    else:
        dict={
            'Min_Length':"0",
            'Max_Length':"9999",
            'Min_Width':"0",
            'Max_Width':"9999",
            'Min_Height':"0",
            'Max_Height':"9999",
            'Min_Area':"0",
            'Max_Area':"9999",
            'Min_Volume':"9999",
            'Max_Volume':"9999",
        }
        return Response(dict)





def check_Area(incr_ar,cnt,Max_Area=10000):
    boxs=Box.objects.all()
    area=0
    for box in boxs:
        area=area+box.Area
    area=area+int(incr_ar)
    area_limit=Max_Area
    if (area/cnt)>area_limit:
        return False
    return True


def check_Volume(incr_vol,cnt,Max_Volume=100000):
    boxs=Box.objects.all()
    volume=0
    for box in boxs:
        volume=volume+box.Volume
    volume=volume+incr_vol
    vol_limit=Max_Volume
    if (volume/cnt)>vol_limit:
        return False
    return True

def check_Date(account=None,limit1=None,limit2=None):
    current_date=datetime.date.today()
    one_week_ago_date=current_date- datetime.timedelta(days=7)
    current_boxes=Box.objects.filter(created_at__lte=current_date).count()
    previous_week_boxes=Box.objects.filter(created_at__lte=one_week_ago_date).count()
    print(current_boxes)
    print(previous_week_boxes)
    box_change_total=int(current_boxes)-int(previous_week_boxes)
    box_change_Staff=Box.objects.filter(created_at__lte=current_date,Creator=account).count()-Box.objects.filter(created_at__lte=one_week_ago_date,Creator=account).count()
    if box_change_total>limit1 or box_change_Staff>limit2:
        return False
    return True







class boxActionIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        Boxs=Box.objects.all()
        if request.user.is_staff:
            srlzr=BoxSerializer(Boxs,many=True)
        else:
            srlzr=BoxSerializer2(Boxs,many=True)
        return Response(srlzr.data)

    def post(self,request,name=None):
        try:
            account=Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            return Response({"msg":"You Are not an User"})
        if account.user.is_staff == False:
            return Response({"Message":"You are not a Store member"})
        length = request.data['Length']
        width = request.data['Width']
        height = request.data['Height']
        count= Box.objects.all().count()

        if check_Area(2*(length*height+height*width+width*length),count+1) ==False:
            return Response("You can't add it as it Area result in more Than Limit")
        if check_Volume(length*height*width,count+1)==False:
            return Response("You can't add it as it Volume result in more Than Limit")
        if check_Date(account,100,50)==False:
            return Response("You can't add it as it Volume result in more Than Limit")
        box = Box.objects.create(Length=length,Height=height,Width=width,Creator=account)
        return Response({"msg":"The Box created sucessfully"})

   
    
    
    
@api_view(('PUT','GET'))    
def put(request):
    if request.method=="PUT":
        if request.user.is_staff == False:
            return Response({"Message":"You are not a Staff member"})
        try:
            pk=int(request.data['pk'])
            box=Box.objects.get(id=pk)
            length = int(request.data['Length'])
            width = int(request.data['Width'])
            height = int(request.data['Height'])
            new_area=2*(length*height+height*width+width*length)
            new_vol=length*height*width
            count= Box.objects.all().count()           
            if check_Area(new_area-box.Area,count)==False:
                return Response("You can't update it as it Area result in more Than Limit")
            if check_Volume(new_vol-box.Volume,count)==False:
                return Response("You can't update it as it Volume result in more Than Limit")
            box.Length=request.data['Length']
            box.Height=request.data['Height']
            box.Width=request.data['Width']
            box.save()
            return Response({"msg":"The Box updated sucessfully"})
        except Box.DoesNotExist:
            return Response({"msg":"Box Not found"})
    else:
        return Response({"pk":'',"Length":'',"Height":'',"Width":''})
  





@api_view(('DELETE','GET'))
def delete(request,pk=None):
    if request.method=='DELETE':
        try:
            account=Account.objects.get(user=request.user)
        except Account.DoesNotExist:
                return Response({"msg":"You Are not an user"})
        count= Box.objects.all().count()
        box = Box.objects.get(pk=pk)
        if check_Area(-box.Area,count-1)==False:
            return Response("You can't Delte it as it Area result in more Than Limit")
        if check_Volume(-box.Volume,count-1)==False:
            return Response("You can't Delete it as it Volume result in more Than Limit")
        creator=box.Creator
        if account!=creator:
            return Response({"Message":"You are not creator fo this box so you can't delete it"})
        box.delete()
        return Response({"msg":"The Box deleted sucessfully"})
    else:
        return Response({"msg":"On Delete Page"})

