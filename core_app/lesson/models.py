from django.db import models



class Subject(models.Model):
    name = models.CharField(max_length=32, unique=True)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=16, unique=True)
    teacher = models.ForeignKey('staffs.Teacher', related_name='my_groups', on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField('staffs.Student', related_name='group')

    def __str__(self):
        return f"{self.teacher.subject} fani bo'yicha {self.name} guruhi"



class GroupJournal(models.Model):
    date = models.DateField(auto_now_add=True)
    group = models.ForeignKey(Group, related_name='journal', on_delete=models.CASCADE)
    theme = models.TextField()
    teacher = models.ForeignKey('staffs.Teacher', related_name='group_journals', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.group} {self.date}"


class AttendanceAndGrades(models.Model):
    date = models.DateField(auto_now_add=True)
    group = models.ForeignKey(Group, related_name='att_and_grades', on_delete=models.SET_NULL, null=True, blank=True)
    GRADES = (
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    )
    student = models.ForeignKey('staffs.Student', related_name='attendance_and_grades', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    grade = models.CharField(max_length=1, choices=GRADES, null=True, blank=True)
    teacher = models.ForeignKey('staffs.Teacher', related_name='attendance_and_grades', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.student} {self.status} {self.grade}"
