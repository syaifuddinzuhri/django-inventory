
import datetime
from MySQLdb import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate, logout
from repoakuntansi.models import User
from repoakuntansi.models import TugasAkhir
from repoakuntansi.models import Jurnal
from .forms import UserForm
from .forms import JurnalForm
from .forms import TugasAkhirForm
from repoakuntansi.functions import handle_uploaded_file  # functions.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from django.contrib.auth.hashers import make_password
import xlwt


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
    konteks["user"] = get_object_or_404(User, username=request.user)
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
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password_confirmation = request.POST.get(
                'new_password_confirmation')
            user = get_object_or_404(User, username=request.user)
            user.email = email
            user.username = username
            user.nama = nama
            if old_password:
                if not user.check_password(old_password):
                    messages.error(request, 'Password lama salah')
                    return redirect('/profile')
                if new_password:
                    if not new_password_confirmation:
                        messages.error(
                            request, 'Konfirmasi password baru harus diisi')
                        return redirect('/profile')
                    if new_password != new_password_confirmation:
                        messages.error(
                            request, 'Konfirmasi password baru tidak sama')
                        return redirect('/profile')
                    user.password = make_password(new_password)
            if user.tipe == 'USER':
                user.nim = nim
                user.kode_prodi = kode_prodi
                user.kelas = kelas
            user.save()
            messages.success(request, 'Berhasil menyimpan data')
            return redirect('/login')
        except:
            messages.error(request, 'Internal Server Error')
            return redirect('/profile')
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    context["data"] = get_object_or_404(User, username=request.user)
    return render(request, 'repoakuntansi/profile.html', context)


# PEMBIMBING VIEWS
@login_required(login_url='/login')
def pembimbingList(request):
    users = User.objects.filter(tipe='PEMBIMBING').values()
    context = {}
    context["data"] = users
    context["user"] = get_object_or_404(User, username=request.user)
    return render(request, 'repoakuntansi/pembimbing/index.html', context)


@login_required(login_url='/login')
def pembimbingCreate(request):
    if request.method == 'POST':
        try:
            post = request.POST.copy()
            post['password'] = make_password(request.POST.get('password'))
            post['tipe'] = 'PEMBIMBING'
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
                return redirect('/pembimbing/create')
            return redirect('/pembimbing')
        except:
            messages.error(request, 'Internal Server Error')
            return redirect('/pembimbing/create')
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    return render(request, 'repoakuntansi/pembimbing/create.html', context)


@login_required(login_url='/login')
def pembimbingEdit(request, id):
    if request.method == 'POST':
        try:
            nama = request.POST.get('nama')
            nip = request.POST.get('nip')
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
            user.nip = nip
            user.save()
            messages.success(request, 'Berhasil menyimpan data')
            return redirect('/pembimbing')
        except:
            next = request.POST.get('next')
            messages.error(request, 'Internal Server Error')
            return redirect(request.path)
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    context["data"] = get_object_or_404(User, id=id)
    return render(request, 'repoakuntansi/pembimbing/edit.html', context)


@login_required(login_url='/login')
def pembimbingDelete(request, id):
    try:
        obj = User.objects.get(id=id)
        obj.delete()
        messages.success(request, 'Berhasil menghapus data')
    except:
        messages.error(request, 'Gagal menghapus data')
    return redirect('/pembimbing')

# USER VIEWS


@login_required(login_url='/login')
def userList(request):
    users = User.objects.filter(tipe='USER').values()
    context = {}
    context["data"] = users
    context["user"] = get_object_or_404(User, username=request.user)
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
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    return render(request, 'repoakuntansi/user/create.html', context)


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
            return redirect(request.path)
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
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
    context["user"] = get_object_or_404(User, username=request.user)
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
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    return render(request, 'repoakuntansi/admin/create.html', context)


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
            return redirect(request.path)
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
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
    context["user"] = get_object_or_404(User, username=request.user)
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
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    return render(request, 'repoakuntansi/super-admin/create.html', context)


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
            return redirect(request.path)
    context = {}
    context["data"] = get_object_or_404(User, id=id)
    context["user"] = get_object_or_404(User, username=request.user)
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
def tugasAkhirList(request):
    tugas = TugasAkhir.objects.all()
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    context["data"] = tugas
    return render(request, 'repoakuntansi/tugas-akhir/index.html', context)


@login_required(login_url='/login')
def tugasAkhirCreate(request):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, username=request.user)
            post = request.POST.copy()
            post['user'] = user.id
            post['status'] = 'Menunggu'
            post['komentar'] = None
            form = TugasAkhirForm(post or None, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Berhasil menyimpan data')
            else:
                msg = []
                for field in form:
                    for error in field.errors:
                        msg.append(error)
                messages.error(request, msg)
                return redirect('/tugas-akhir/create')
            return redirect('/tugas-akhir')
        except:
            messages.error(request, 'Internal Server Error')
            return redirect('/tugas-akhir/create')
    pembimbing = User.objects.filter(tipe='PEMBIMBING').values()
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    context["pembimbing"] = pembimbing
    return render(request, 'repoakuntansi/tugas-akhir/create.html', context)


@login_required(login_url='/login')
def tugasAkhirEdit(request, id):
    if request.method == 'POST':
        try:
            tugasAkhir = TugasAkhir.objects.get(id=id)
            post = request.POST.copy()
            post['user'] = tugasAkhir.user_id
            # post['status'] = tugasAkhir.status
            form = TugasAkhirForm(post,
                                  request.FILES, instance=tugasAkhir)
            if form.is_valid():
                form.save()
                messages.success(request, 'Berhasil menyimpan data')
            else:
                msg = []
                for field in form:
                    for error in field.errors:
                        msg.append(error)
                messages.error(request, msg)
                return redirect(request.path)
            messages.success(request, 'Berhasil menyimpan data')
            return redirect('/tugas-akhir')
        except:
            next = request.POST.get('next')
            messages.error(request, 'Internal Server Error')
            return redirect(request.path)
    context = {}
    pembimbing = User.objects.filter(tipe='PEMBIMBING').values()
    context["user"] = get_object_or_404(User, username=request.user)
    context["data"] = get_object_or_404(TugasAkhir, id=id)
    context["pembimbing"] = pembimbing
    return render(request, 'repoakuntansi/tugas-akhir/edit.html', context)


@login_required(login_url='/login')
def tugasAkhirDelete(request, id):
    try:
        obj = TugasAkhir.objects.get(id=id)
        obj.delete()
        messages.success(request, 'Berhasil menghapus data')
    except:
        messages.error(request, 'Gagal menghapus data')
    return redirect('/tugas-akhir')

# JURNAL VIEWS


@login_required(login_url='/login')
def jurnalList(request):
    tugas = Jurnal.objects.all()
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    context["data"] = tugas
    return render(request, 'repoakuntansi/jurnal/index.html', context)


@login_required(login_url='/login')
def jurnalCreate(request):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, username=request.user)
            post = request.POST.copy()
            post['user'] = user.id
            post['status'] = 'Menunggu Konfirmasi'
            form = JurnalForm(post or None, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Berhasil menyimpan data')
            else:
                msg = []
                for field in form:
                    for error in field.errors:
                        msg.append(error)
                messages.error(request, msg)
                return redirect('/jurnal/create')
            return redirect('/jurnal')
        except:
            messages.error(request, 'Internal Server Error')
            return redirect('/jurnal/create')
    pembimbing = User.objects.filter(tipe='PEMBIMBING').values()
    context = {}
    context["user"] = get_object_or_404(User, username=request.user)
    context["data"] = pembimbing
    return render(request, 'repoakuntansi/jurnal/create.html', context)


@login_required(login_url='/login')
def jurnalEdit(request, id):
    if request.method == 'POST':
        try:
            jurnal = Jurnal.objects.get(id=id)
            post = request.POST.copy()
            post['user'] = jurnal.user_id
            post['status'] = jurnal.status
            form = JurnalForm(post,
                              request.FILES, instance=jurnal)
            if form.is_valid():
                form.save()
                messages.success(request, 'Berhasil menyimpan data')
            else:
                msg = []
                for field in form:
                    for error in field.errors:
                        msg.append(error)
                messages.error(request, msg)
                return redirect(request.path)
            messages.success(request, 'Berhasil menyimpan data')
            return redirect('/jurnal')
        except:
            next = request.POST.get('next')
            messages.error(request, 'Internal Server Error')
            return redirect(request.path)
    context = {}
    pembimbing = User.objects.filter(tipe='PEMBIMBING').values()
    context["user"] = get_object_or_404(User, username=request.user)
    context["data"] = get_object_or_404(Jurnal, id=id)
    context["pembimbing"] = pembimbing
    return render(request, 'repoakuntansi/jurnal/edit.html', context)


@login_required(login_url='/login')
def jurnalDelete(request, id):
    try:
        obj = Jurnal.objects.get(id=id)
        obj.delete()
        messages.success(request, 'Berhasil menghapus data')
    except:
        messages.error(request, 'Gagal menghapus data')
    return redirect('/jurnal')


@login_required(login_url='/login')
def exportJurnal(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Jurnal' + \
        str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Jurnal')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font_bold = True
    columns = ['Judul', 'Deskripsi', 'File']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Jurnal.objects.all().values_list('title', 'deskripsi', 'file')

    for row in rows:
        row_num += 1
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response
