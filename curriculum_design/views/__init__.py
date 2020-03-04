
import json, re

from django.views import View
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.hashers import make_password

from curriculum_design.models import Student, Teacher
# from curriculum_design.utils.validate import ValidateSignUpParams

class LoginView(View):

  def get(self, *args, **kwargs):
    return HttpResponse('fuck you')

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


__all__ = ['LoginView', 'SignUpView']
