from django.contrib.auth.models import User, Group

from departments.models import department
from main_requests.models import MainRequest
from places.models import Places
from work_profiles.models import Profile


def createGroups():
    group1 = Group.objects.create(name='Администрато')
    group1.save()
    group2 = Group.objects.create(name='Исполнитель')
    group2.save()
    group3 = Group.objects.create(name='Пользователи')
    group3.save()


def createDepartments():
    dep1 = department.objects.create(name='Department1', description='Description1')
    dep1.save()
    dep2 = department.objects.create(name='Department2', description='Description2')
    dep2.save()


def createUsers():
    user1 = User.objects.create_user(username='user1', password='11223344')
    user1.save()
    p1 = user1.profileEptm
    dep1 = department.objects.get(name='Department1')

    p1.deparment = dep1
    p1.user_position = 'position1'
    p1.save()

    user2 = User.objects.create_user(username='user2', password='11223344')
    user2.save()

    p2 = user2.profileEptm
    p2.deparment = department.objects.all()[0]
    p2.user_position = 'position2'
    p2.save()


def createBase():
    pl1 = Places.objects.create(name="place1")
    pl1.save()
    pl2 = Places.objects.create(name="place2")
    pl2.save()
    m1 = MainRequest.objects.create(number=1,
                                    request_user=Profile.objects.all()[0],
                                    about='About',
                                    input_user=Profile.objects.all()[0],
                                    place=pl1)
    m1.save()
    print('pk =', m1.pk)


def createDepatment():
    dep1 = department.objects.create(name='Department1', description='Description1')
    dep1.save()
    dep2 = department.objects.create(name='Department2', description='Description2')
    dep2.save()


def updateProfile():
    u1 = User.objects.get(username='user1')
    p1 = Profile.objects.filter(user=u1)
    p1.deparment = department.objects.get(pk=1)
    p1.user_position = 'position1'

    u2 = User.objects.get(username='user2')
    p2 = Profile.objects.filter(user=u2)
    p2.deparment = department.objects.get(pk=2)
    p2.user_position = 'position2'


def createPlace():
    p1 = Places.objects.create(name="place1")
    p1.save()
    p2 = Places.objects.create(name="place2")
    p2.save()


def createRequests():
    m1 = MainRequest.objects.create(numbrer=1,
                                    reauest_user=Profile.objects.get(pk=1),
                                    about='About',
                                    input_user=Profile.objects.get(pk=1),
                                    place=Places.objects.get(pk=1))
    m1.save()
