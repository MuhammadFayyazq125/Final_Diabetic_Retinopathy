# importing required packages

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from diab_retina_app import process
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from fpdf import FPDF
# from .decorators import authorized_access , admin_only , unauthenticated_user,allowed_user
from django.contrib.auth.models import User

@login_required(login_url='login')
@csrf_exempt
def display(request):
    if request.method == 'GET':
        return render(request, 'index.html')

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        img = request.POST.get('image')
        pname = request.POST.get('name')
        rightEye = request.POST.get('right')
        leftEye = request.POST.get('left')
        print( "right eye ============== ",rightEye," ================ leftEye", leftEye)
        response = process.process_img(img)  
        pdfFile(pname,rightEye,leftEye,response)              
        return HttpResponse(response, status=200)
def result(request):
    return render(request, 'result.html')

def pdfFile(pname,rightEye,leftEye,response):
    Dr_name = User.objects.all().last()
    Patient_name = pname
    rightEye = rightEye
    leftEye = leftEye
    diabetic_level = response[0]
    diabetic_accuracy = response[2]
    sales = [
        {"item": "Dr Name", "amount": str(Dr_name)},
        {"item": "Patient Name", "amount": str(pname)},
        {"item": "Eye", "amount": str(rightEye)},
        {"item": "Diabetic Level", "amount": str(diabetic_level)},
        {"item": "Diabetic Accuracy", "amount": str(int(diabetic_accuracy))},
    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Diabetic Retinopathy Report:',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Item'.ljust(30)} {'Amount'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    return pdf.output(f'{Patient_name}.pdf', 'F')
def registerPage(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("registration of user is", user)
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='admin')
            user.groups.add(group)
            print("checking user group", group)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    print("checking the all values of form", form)
    context = {'form':form} 
    return render(request, 'register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('display')
		else:
			messages.info(request, 'Username OR password is incorrect')
	context = {}
	return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')