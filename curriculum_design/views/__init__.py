
import json, re

from django.views import View
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from curriculum_design.models import Student, Teacher


class LoginView(View):

  def get_bool(self, request, key):
    val = request.POST.get(key)
    return val == 'true'

  def get(self, *args, **kwargs):
    return HttpResponse('fuck you')

  def post(self, request):
    identity = self.get_bool(request, 'identity')
    
    if identity:
      user_id = request.POST.get('id')
      password = request.POST.get('password')
      stu = Student.objects.get(user_id=user_id)
      if stu.password == password:
        content = json.dumps({
          # 'status': 200,
          'code': 0,
          'msg': 'login success.'
        })
      else:
        content = json.dumps({
          # 'status': 200,
          'code': 0,
          'msg': 'password is wrong.'
        })
      res = HttpResponse(content=content, content_type='text/json')
      res.set_signed_cookie('session_id', user_id, max_age=60 * 60, salt='fuck')
      return res
    else:
      phone = request.POST.get('phone')
      password = request.POST.get('password')
      teacher = Teacher.objects.get(phone=phone)
      if teacher.password == password:
        content = json.dumps({
          'code': 0,
          'msg': 'login success.'
        })
      else:
        content = json.dumps({
          'code': 0,
          'msg': 'password is wrong.'
        })
      res = HttpResponse(content=content, content_type='text/json')
      res.set_signed_cookie('session_id', phone, max_age=60 * 60, salt='fuck')
      return res



class SignUpView(View):

  def is_student_exist(self, user_id):
    try:
      stu = Student.objects.get(user_id=user_id)
      return True
    except Exception:
      return False
    
  def is_teacher_exist(self, phone):
    try:
      teach = Teacher.objects.get(phone=phone)
      return True
    except Exception:
      return False

  def get_bool(self, request, key):
    val = request.POST.get(key)
    return val == 'true'

  def new_user(self, request):
    identity = self.get_bool(request, 'identity')
    if identity:
      self.new_student(request)
    else:
      self.new_teacher(request)

  def new_student(self, request):
    user_id = request.POST.get('id')

    if (self.is_student_exist(user_id)):
      raise Exception(user_id + ' is already exist')

    password = request.POST.get('password')
    name = request.POST.get('name')
    age = int(request.POST.get('age'))
    sex = self.get_bool(request, 'sex')
    class_number = request.POST.get('classNumber')
    student = Student(
      user_id=user_id,
      password=password,
      name=name,
      age=age,
      sex=sex,
      class_number=class_number
    )
    student.save()
  
  def new_teacher(self, request):
    phone = request.POST.get('phone')

    if (self.is_teacher_exist(phone)):
      raise Exception(phone + ' is already exist')

    name = request.POST.get('name')
    sex = self.get_bool(request, 'sex')
    age = int(request.POST.get('age'))
    password = request.POST.get('password')
    teacher = Teacher(
      phone=phone,
      name=name,
      sex=sex,
      age=age,
      password=password,
    )
    teacher.save()

  def get(self, request):
    return HttpResponse('only post method is supported.')

  def post(self, request):
    print(request.POST)
    try:
      self.new_user(request)
      content = json.dumps({
        'code': 1,
        'msg': 'sign up success.'
      })
      return HttpResponse(content, content_type='text/json')
    except Exception as err:
      return HttpResponse(err, content_type='text/json')


class IsLogin(View):
  def get(self, request):
    try:
      key = request.get_signed_cookie('session_id', salt='fuck')
      content = json.dumps({
        'code': 0,
        'msg': 'login'
      })
    except Exception:
      content = json.dumps({
        'code': 0,
        'msg': 'not login'
      })
    return HttpResponse(content=content)


__all__ = ['LoginView', 'SignUpView', 'IsLogin']
