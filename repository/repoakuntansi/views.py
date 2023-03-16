
from MySQLdb import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate, logout
from repoakuntansi.models import User
from repoakuntansi.models import Jurnal
from .forms import UserForm
from .forms import JurnalForm
from repoakuntansi.functions import handle_uploaded_file  # functions.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from django.contrib.auth.hashers import make_password


@login_required(login_url='/login')
def index(request):
    return redirect('/dashboard')


@login_required(login_url='/login')
def dashboard(request):

    user = User.objects.all()
    data = {}
    data['object_list'] = user

    # if request.method == 'POST' and request.FILES['myfile']:
    if request.method == 'POST':
        form = JurnalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('COAK')
        print('KOO')
        # form.save()
        # form = UserForm(request.POST or None)
        # print(form)
        # myfile = request.FILES['myfile']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        # return render(request, 'repoakuntansi/dashboard.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })

    form = JurnalForm()
    books = Jurnal.objects.all()
    konteks = {
        'form': form,
        'books': books,
    }
    return render(request, 'repoakuntansi/dashboard.html', konteks)


# AUTH VIEWS

def loginPage(request):
    if request.user.is_anonymous == False:
        redirect('dashboard')
    return render(request, 'repoakuntansi/login.html')


def submitLogin(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not username or not password:
                messages.error(request, 'Username dan password harus diisi')
            user = authenticate(request, username=username,
                                password=password)
            if user is None:
                messages.error(request, 'Username atau password salah')
            else:
                login(request, user)
                messages.success(request, 'Login Berhasil')
            return redirect('dashboard')
        except:
            messages.error(request, 'Internal Server Error')
    return redirect('login')


def logoutPage(request):
    logout(request)
    messages.success(request, 'Logout Berhasil')
    return redirect('login')


def profile(request):
    if request.method == 'POST':
        try:
            nama = request.POST.get('nama')
            nim = request.POST.get('nim')
            kelas = request.POST.get('kelas')
            kode_prodi = request.POST.get('kode_prodi')
            email = request.POST.get('email')
            username = request.POST.get('username')
            user = get_object_or_404(User, username=request.user)
            user.email = email
            user.username = username
            user.nama = nama
            if user.tipe == 'USER':
                user.nim = nim
                user.kode_prodi = kode_prodi
                user.kelas = kelas
            user.save()
            messages.success(request, 'Berhasil menyimpan data')
            return redirect('profile')
        except:
            messages.error(request, 'Internal Server Error')
            return redirect('profile')
    context = {}
    context["data"] = get_object_or_404(User, username=request.user)
    return render(request, 'repoakuntansi/profile.html', context)


# USER VIEWS
@login_required(login_url='/login')
def userList(request):
    users = User.objects.filter(tipe='USER').values()
    context = {}
    context["data"] = users
    return render(request, 'repoakuntansi/user/index.html', context)


@login_required(login_url='/login')
def userCreate(request):
    if request.method == 'POST':
        try:
            post = request.POST.copy()
            post['password'] = make_password(request.POST.get('password'))
            post['tipe'] = 'USER'
            form = UserForm(post or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Berhasil menyimpan data')
            else:
                msg = []
                for field in form:
                    for error in field.errors:
                        msg.append(error)
                messages.error(request, msg)
                return redirect('/user/create')
            return redirect('/user')
        except:
            messages.error(request, 'Internal Server Error')
            return redirect('/user/create')
    return render(request, 'repoakuntansi/user/create.html')


@login_required(login_url='/login')
def userEdit(request, id):
    if request.method == 'POST':
        try:
            nama = request.POST.get('nama')
            nim = request.POST.get('nim')
            kelas = request.POST.get('kelas')
            kode_prodi = request.POST.get('kode_prodi')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = get_object_or_404(User, id=id)
            if len(password) > 0:
                password = make_password(request.POST.get('password'))
                user.password = password
            user.email = email
            user.username = username
            user.nama = nama
            user.nim = nim
            user.kode_prodi = kode_prodi
            user.kelas = kelas
            user.save()
            messages.success(request, 'Berhasil menyimpan data')
            return redirect('/user')
        except:
            next = request.POST.get('next')
            messages.error(request, 'Internal Server Error')
            return HttpResponseRedirect(next)
    context = {}
    context["data"] = get_object_or_404(User, id=id)
    return render(request, 'repoakuntansi/user/edit.html', context)


@login_required(login_url='/login')
def userDelete(request, id):
    try:
        obj = User.objects.get(id=id)
        obj.delete()
        messages.success(request, 'Berhasil menghapus data')
    except:
        messages.error(request, 'Gagal menghapus data')
    return redirect('/user')

# ADMIN VIEWS


@login_required(login_url='/login')
def adminList(request):
    users = User.objects.filter(tipe='ADMIN').values()
    context = {}
    context["data"] = users
    return render(request, 'repoakuntansi/admin/index.html', context)


@login_required(login_url='/login')
def adminCreate(request):
    if request.method == 'POST':
        try:
            post = request.POST.copy()
            post['password'] = make_password(request.POST.get('password'))
            post['tipe'] = 'ADMIN'
            form = UserForm(post or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Berhasil menyimpan data')
            else:
                msg = []
                for field in form:
                    for error in field.errors:
                        msg.append(error)
                messages.error(request, msg)
                return redirect('/admins/create')
            return redirect('/admins')
        except:
            messages.error(request, 'Internal Server Error')
            return redirect('/admins/create')
    return render(request, 'repoakuntansi/admin/create.html')


@login_required(login_url='/login')
def adminEdit(request, id):
    if request.method == 'POST':
        try:
            nama = request.POST.get('nama')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = get_object_or_404(User, id=id)
            if len(password) > 0:
                password = make_password(request.POST.get('password'))
                user.password = password
            user.email = email
            user.username = username
            user.nama = nama
            user.save()
            messages.success(request, 'Berhasil menyimpan data')
            return redirect('/admins')
        except:
            next = request.POST.get('next')
            messages.error(request, 'Internal Server Error')
            return HttpResponseRedirect(next)
    context = {}
    context["data"] = get_object_or_404(User, id=id)
    return render(request, 'repoakuntansi/admin/edit.html', context)


@login_required(login_url='/login')
def adminDelete(request, id):
    try:
        obj = User.objects.get(id=id)
        obj.delete()
        messages.success(request, 'Berhasil menghapus data')
    except:
        messages.error(request, 'Gagal menghapus data')
    return redirect('/admins')

# SUPER ADMIN VIEWS


@login_required(login_url='/login')
def superAdminList(request):
    users = User.objects.filter(tipe='SUPER_ADMIN').values()
    context = {}
    context["data"] = users
    return render(request, 'repoakuntansi/super-admin/index.html', context)


@login_required(login_url='/login')
def superAdminCreate(request):
    if request.method == 'POST':
        try:
            post = request.POST.copy()
            post['password'] = make_password(request.POST.get('password'))
            post['tipe'] = 'SUPER_ADMIN'
            form = UserForm(post or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Berhasil menyimpan data')
            else:
                msg = []
                for field in form:
                    for error in field.errors:
                        msg.append(error)
                messages.error(request, msg)
                return redirect('/super-admin/create')
            return redirect('/super-admin')
        except:
            messages.error(request, 'Internal Server Error')
            return redirect('/super-admin/create')
    return render(request, 'repoakuntansi/super-admin/create.html')


@login_required(login_url='/login')
def superAdminEdit(request, id):
    if request.method == 'POST':
        try:
            nama = request.POST.get('nama')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = get_object_or_404(User, id=id)
            if len(password) > 0:
                password = make_password(request.POST.get('password'))
                user.password = password
            user.email = email
            user.username = username
            user.nama = nama
            user.save()
            messages.success(request, 'Berhasil menyimpan data')
            return redirect('/super-admin')
        except:
            next = request.POST.get('next')
            messages.error(request, 'Internal Server Error')
            return HttpResponseRedirect(next)
    context = {}
    context["data"] = get_object_or_404(User, id=id)
    return render(request, 'repoakuntansi/super-admin/edit.html', context)


@login_required(login_url='/login')
def superAdminDelete(request, id):
    try:
        obj = User.objects.get(id=id)
        obj.delete()
        messages.success(request, 'Berhasil menghapus data')
    except:
        messages.error(request, 'Gagal menghapus data')
    return redirect('/super-admin')

# TUGAS VIEWS


@login_required(login_url='/login')
def tugas(request):
    return render(request, 'repoakuntansi/tugas.html')

# JURNAL VIEWS


@login_required(login_url='/login')
def jurnal(request):
    return render(request, 'repoakuntansi/jurnal.html')

# PEMBIMBING VIEWS


@login_required(login_url='/login')
def pembimbing(request):
    return render(request, 'repoakuntansi/pembimbing.html')
