from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import SignUpForm, AddRecordForm
from .models import Record

from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from .serializers import ItemsSerializer
from .forms import UpdateRecordForm


record_obj = Record()
class Homepage(View):
    def get(self, request):
        records = record_obj.get_records(request.user.id)
        return render(request,template_name='homepage.html',context={'records': records})
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfull")
            return redirect('homepage')
        else:
            messages.success(request, "Error occured, please try again!")
            return redirect('homepage')
    

class Logout_user(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout successfull")
        return redirect('homepage')
    
class Register_User(View):
    def get(self, request):
        form = SignUpForm()
        return render(request,template_name='register.html', context={'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if (form.is_valid()):
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('homepage')
        else:
            messages.success(request, "Error occured, Please try again!")
            return redirect('register')

class AddRecord(APIView):
    
    def get(self, request):
        form = AddRecordForm()
        return render(request, template_name="Addrecord.html", context={"form": form})
    
    def post(self, request):
        if (request.path == '/add/'):
            if request.user.is_authenticated:
                data = request.POST.copy()
                data['added_by'] = request.user.id
                Serializer = ItemsSerializer(data=data)
                if Serializer.is_valid():
                    Serializer.save()
                    messages.success(request, "Record saved successfully!")
                    return redirect("homepage")
                else:
                    messages.success(request, "Data have some issue!")
                    return redirect('addrecord')
            else:
                messages.success(request, "You must be logged In!")
                return redirect("homepage")
        elif (request.path == '/api/add/'):
            data = request.data
            user_name = request.data.get('username', None)
            password = request.data.get('password', None)
            if (not user_name or not password):
                return JsonResponse({"Message": "username and password required!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                authicated = authenticate(username=user_name, password=password)
                if (authicated):
                    data = request.data
                    data['added_by'] = authicated.id
                    Serializer = ItemsSerializer(data=data)
                    if Serializer.is_valid():
                        Serializer.save()
                        return JsonResponse({"Message": "Data saved successfully!"}, status=status.HTTP_200_OK)
                    else:
                        return JsonResponse({"Message": "Error occured! Please make sure all fields are available in the body."}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return JsonResponse({"Message": "Authentication error!"}, status=status.HTTP_401_UNAUTHORIZED)
                    
        
class CustomerRecord(View):
    def get(self, request, pk):
        if (request.user.is_authenticated):
            records = record_obj.get_records(request.user.id,pk)
            return render(request, template_name="customer_record.html", context={'record': records})
        else:
            messages.success(request, "You must be logged in!")
            return redirect('homepage')
        

#####API VIEWS#####
class Api(APIView):
    def get(self, request, pk=None):
        if (request.path == '/api/endpoints/'):
            api_urls = {
                'APIs endpoints':'/api/endpoints/',
                'Add record': '/api/add/',
                'Get record': '/api/id/',
                'Update record': '/api/update/',
                'Delete record': '/api/delete/'
            }
            return JsonResponse(api_urls, status=status.HTTP_200_OK)
        else:
            user_name = request.data.get("username", None)
            password = request.data.get("password", None)
            if (not user_name or not password):
                return JsonResponse({"Message": "Authentication error!"}, status=status.HTTP_401_UNAUTHORIZED)
            authenticated = authenticate(username=user_name, password=password)
            record = record_obj.get_records(authenticated,pk)
            if (record):
                items = ItemsSerializer(record)
                return JsonResponse(items.data, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"Message": "Record dosen't exists!"}, status=status.HTTP_200_OK)
            
class DeleteRecord(APIView):

    def get(self, request, pk):
        if request.user.is_authenticated:
            rec = record_obj.get_records(request.user.id,pk)
            rec.delete()
            messages.success(request, "Record deleted!")
        else:
            messages.success(request, "You must be logged in!")
        return redirect('homepage')
    
    def delete(self, request):
        print ("request_data::",request.data)
        print ("request_path::",request.path)
        #Credential based authentication using username and password.
        user_name = request.data.get('username', None)
        password = request.data.get('password', None)
        if (not user_name or not password):
            return JsonResponse({"Message": "username and password field required!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            authicated = authenticate(username=user_name, password=password)
            if (not authicated):
                return JsonResponse({"Message": "Authentication error!"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                if (request.data.get("pk", None)):
                    rec = record_obj.get_records(authicated,request.data.get("pk"))
                    if (not rec):
                        return JsonResponse({"Message": "No data exists with this ID(pk)."})
                    rec.delete()
                    return JsonResponse({"Message": "Record deleted successfully!"}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"Message": "field record id(pk) is not provided!"}, status=status.HTTP_206_PARTIAL_CONTENT)



class UpdateRecord(APIView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            form = UpdateRecordForm()
            return render(request, template_name='Update.html', context={'id':pk, "form": form})
        else:
            messages.success(request, "You must be logged in!")
        return redirect('homepage')
    
    def post(self, request, pk=None):
        flag = False
        authicate_flag = False

        #If user is sending api request then according to the logic he have to send record id and his credentials in the payload to update the data.
        if (request.path == '/api/update/'):
            #Credential based authentication using username and password.
            user_name = request.data.get('username', None)
            password = request.data.get('password', None)
            if (not user_name or not password):
                return JsonResponse({"Message": "username and password required!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                authicated = authenticate(username=user_name, password=password)
                if (authicated):
                    authicate_flag = True

        #If user is authenticated
        if request.user.is_authenticated or authicate_flag:
            #If pk is not present in the url, that means user is sending an API request.
            if (request.path == '/api/update/'):
                pk = request.data.get("pk", None)
                flag = True
                #If record id is not provided in the data.
                if (not pk):
                    return JsonResponse({"Message": "field record id(pk) is not provided!"}, status=status.HTTP_206_PARTIAL_CONTENT)
            if (authicate_flag):
                get_record = record_obj.get_records(authicated, pk)
            else:
                get_record = record_obj.get_records(request.user.id, pk)
            if (flag and not get_record):
                return JsonResponse({"Message": "No data exists with this ID(pk)"}, status=status.HTTP_200_OK)
            try:
                request.data.pop("username")
                request.data.pop("password")
            except:
                pass


            data = request.data
            Serializer = ItemsSerializer(get_record, data=data, partial=True)
            if (Serializer.is_valid()):
                Serializer.save()
                if (flag):
                    return JsonResponse({"Message": "Data updated successfully!"}, status=status.HTTP_200_OK)
                else:
                    messages.success(request, "Data updated successfully!")
                    return redirect('homepage')
            else:   
                return JsonResponse({"Message": "Inappropriate data."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            if (request.path == '/api/update/'):
                return JsonResponse({"Message": "Authentication error!"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                messages.success(request, "You must be logged in!")
                return redirect('homepage')