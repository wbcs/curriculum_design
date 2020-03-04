from django.db import models

class Student(models.Model):

  class Meta:
    db_table = 'table_student'
    ordering = ('-create_time',)

  user_id = models.CharField(max_length=8, primary_key=True, verbose_name=u"学号")
  password = models.CharField(max_length=100, null=False, verbose_name=u"密码")
  name = models.CharField(max_length=50, verbose_name=u"姓名")
  sex = models.BooleanField(default=True, verbose_name=u"性别")
  age = models.IntegerField(default=0, verbose_name=u"年龄")
  class_number = models.CharField(max_length=20, verbose_name=u"班级")

  create_time = models.DateTimeField(
    auto_now_add=True,
    verbose_name='创建时间'
  )
  modify_time = models.DateTimeField(
    auto_now=True,
    verbose_name='最后修改时间'
  )


class Teacher(models.Model):

  class Meta:
    db_table = 'table_teacher'
    ordering = ('-create_time',)

  phone = models.CharField(max_length=11, primary_key=True, verbose_name=u"电话")
  name = models.CharField(max_length=50, verbose_name=u"姓名")
  sex = models.BooleanField(default=True, verbose_name=u"性别")
  age = models.IntegerField(null=False, verbose_name=u"年龄")
  password = models.CharField(max_length=100, null=False, verbose_name=u"密码")

  create_time = models.DateTimeField(
    auto_now_add=True,
    verbose_name='创建时间'
  )
  modify_time = models.DateTimeField(
    auto_now=True,
    verbose_name='最后修改时间'
  )


class ClassInfo(models.Model):

  class Meta:
    db_table = 'table_class'
    ordering = ('-create_time',)

  class_number = models.IntegerField(primary_key=True, verbose_name=u"班级")
  teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u"老师")
  class_name = models.CharField(max_length=50, verbose_name=u"课程名")
  location = models.CharField(max_length=300, verbose_name=u"资源标识")

  create_time = models.DateTimeField(
    auto_now_add=True,
    verbose_name='创建时间'
  )
  modify_time = models.DateTimeField(
    auto_now=True,
    verbose_name='最后修改时间'
  )

