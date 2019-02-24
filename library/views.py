#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
import random

from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone
from django.db.models import Q
from django.db.models import F

from library.models import User, Mission, UserProfile, DoMission, MissionImage, DoMissionImage, MissionLock, MissionBackup, MissionImageBackup, MissionLockBackup, DoMissionBackup, DoMissionImageBackup
from library.forms import LoginForm, RegisterForm, ResetPasswordForm, MissionForm, ProofForm
from wechatvote.settings import APP_VERSION, UPDATE_URL
admin = '13056676836'


def index(request):
    if request.user.is_authenticated():
        new_version = '1.0.0'   #从服务器获取新版本号
        str1 = APP_VERSION.replace('.', '')
        str2 = new_version.replace('.', '')
        if int(str2)-int(str1) > 0:
            return JsonResponse({'update_url': UPDATE_URL})

        missionlock = MissionLock.objects.filter(locker=request.user.username).values('mission_id')
        missions = Mission.objects.filter(~Q(pk__in=missionlock), ~Q(user=request.user.username), amount__gt=0)
        print(missions.count())
        if missions.count() > 0:
            mission = missions[0]
            # missions = random.sample(Mission.objects.filter(user=keyword), 1)
            return render(request, 'library/index.html', {'mission': mission})
        else:
            state = 'filter_zero'
            #return JsonResponse({'state': state})
            return render(request, 'library/index.html', {'state': state})

    else:
        new_version = '1.0.0'   #从服务器获取新版本号
        str1 = APP_VERSION.replace('.', '')
        str2 = new_version.replace('.', '')
        if int(str2)-int(str1) > 0:
            return JsonResponse({'update_url': UPDATE_URL})

        return render(request, 'library/index.html')
        #return JsonResponse({"missions": missions, "current_path": current_path})


def backstage(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/backstage_login')
    elif request.user.is_superuser == 0:
        return HttpResponseRedirect('/backstage_login')
    else:
        start = timezone.now() - datetime.timedelta(days=180)
        print(timezone.now())
        print(start)
        missiontrans = Mission.objects.filter(date_mission__lt=start)
        for misstrans in missiontrans:
            MissionBackup.objects.create(user=misstrans.user, type=misstrans.type, description=misstrans.description, imageshot=misstrans.imageshot, capital=misstrans.capital, cost=misstrans.cost, amount=misstrans.amount, totalcost=misstrans.totalcost, date_mission=misstrans.date_mission)
        missiontrans.delete()

        missionimagetrans = MissionImage.objects.filter(date_missionimage__lt=start)
        for missimagetrans in missionimagetrans:
            MissionImageBackup.objects.create(mission_id=missimagetrans.mission_id, imageshots=missimagetrans.imageshots, date_missionimage=missimagetrans.date_missionimage)
            missionimagetrans.delete()

        missionlock = MissionLock.objects.filter(date_lock__lt=start)
        for misslock in missionlock:
            MissionLockBackup.objects.create(mission_id=misslock.mission_id, locker=misslock.locker, issuer=misslock.issuer, is_pass=misslock.is_pass, type=misslock.type, description=misslock.description, imageshot=misslock.imageshot, cost=misslock.cost, date_lock=misslock.date_lock)
        missionlock.delete()

        domissions = DoMission.objects.filter(date_domission__lt=start)
        for domission in domissions:
            DoMissionBackup.objects.create(mission_id=domission.mission_id, missionlock_id=domission.missionlock_id, executor=domission.executor, issuer=domission.issuer, is_pass=domission.is_pass, type=domission.type, description=domission.description, imageshot=domission.imageshot, proof=domission.proof, cost=domission.cost, date_domission=domission.date_domission)
        domissions.delete()

        domissionimages = DoMissionImage.objects.filter(date_domissionimage__lt=start)
        for domissionimage in domissionimages:
            DoMissionImageBackup.objects.create(domission_id=domissionimage.domission_id, proof=domissionimage.proof, date_domissionimage=domissionimage.date_domissionimage)
            domissionimages.delete()

        userprofile = UserProfile.objects.all()
        paginator = Paginator(userprofile, 10)
        page = request.GET.get('page', 1)

        try:
            userprofile = paginator.page(page)
        except PageNotAnInteger:
            userprofile = paginator.page(1)
        except EmptyPage:
            userprofile = paginator.page(paginator.num_pages)

        context = {
            'userprofile': userprofile,
        }
        return render(request, 'library/backstage.html', context)


def admin_alter(request):
    user_id = request.GET.get('user_id', None)
    userprofile = UserProfile.objects.get(user_id=user_id)
    userx = User.objects.get(pk=user_id)

    state = None
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        integral = request.POST.get('integral', '')

        # User.objects.filter(pk=user_id).update(username=phone, first_name=name, email=email)
        # UserProfile.objects.filter(pk=user_id).update(name=name, phone=phone, email=email, integral=integral)

        userx.username = phone
        userx.first_name = name
        userx.email = email
        userx.save()

        userprofile.name = name
        userprofile.phone = phone
        userprofile.email = email
        userprofile.integral = integral
        userprofile.save()

        state = 'success'
        context = {
            'state': state,
            'userx': userx,
            'userprofile': userprofile,
        }
        return render(request, 'library/admin_alter.html', context)

    context = {
        'state': state,
        'userx': userx,
        'userprofile': userprofile,
    }
    return render(request, 'library/admin_alter.html', context)


def myissue(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    else:
        missions = Mission.objects.filter(user=request.user.username).order_by('-id')

        paginator = Paginator(missions, 10)
        page = request.GET.get('page', 1)

        try:
            missions = paginator.page(page)
        except PageNotAnInteger:
            missions = paginator.page(1)
        except EmptyPage:
            missions = paginator.page(paginator.num_pages)

        context = {
            'missions': missions,
        }

        #return JsonResponse(serializers.serialize('json', missions), safe=False)
        return render(request, 'library/myissue.html', context)


def mymission(request):
    if not request.user.is_authenticated():
        return JsonResponse({'msg': 'login'})
        #return HttpResponseRedirect('/login')

    else:
        missionlock = MissionLock.objects.filter(locker=request.user.username, is_pass=3).order_by('-id')
        mymissions = DoMission.objects.filter(executor=request.user.username).order_by('-id')

        for lock in missionlock:
            print(lock.date_lock)
            print((timezone.now()-lock.date_lock).seconds)
            if (timezone.now()-lock.date_lock).seconds > 600:
                lock.is_pass = 4
                lock.save()
                Mission.objects.filter(pk=lock.mission_id).update(amount=F('amount')+1)

        paginator = Paginator(mymissions, 10)
        page = request.GET.get('page', 1)

        try:
            mymissions = paginator.page(page)
        except PageNotAnInteger:
            mymissions = paginator.page(1)
        except EmptyPage:
            mymissions = paginator.page(paginator.num_pages)

        context = {
            'mymissions': mymissions,
            'missionslock': missionlock,
        }
        return render(request, 'library/mymission.html', context)


def myaudit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    elif request.user.username == admin:
        domissions = DoMission.objects.filter(is_pass=2).order_by('-id')

        paginator = Paginator(domissions, 10)
        page = request.GET.get('page', 1)

        try:
            domissions = paginator.page(page)
        except PageNotAnInteger:
            domissions = paginator.page(1)
        except EmptyPage:
            domissions = paginator.page(paginator.num_pages)

        context = {
            'domissions': domissions,
        }
        return render(request, 'library/myaudit.html', context)

    else:
        domissions = DoMission.objects.filter(issuer=request.user.username).order_by('-id')

        paginator = Paginator(domissions, 10)
        page = request.GET.get('page', 1)

        try:
            domissions = paginator.page(page)
        except PageNotAnInteger:
            domissions = paginator.page(1)
        except EmptyPage:
            domissions = paginator.page(paginator.num_pages)

        context = {
            'domissions': domissions,
        }
        return render(request, 'library/myaudit.html', context)


def backstage_login(request):
    if request.user.is_authenticated() and request.user.is_superuser == 1:
        return HttpResponseRedirect('/backstage')

    else:
        state = None
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            #request.session['username'] = username

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active and user.is_superuser == 1:
                    auth.login(request, user)
                    return HttpResponseRedirect('/backstage')
                else:
                    state = 'permission_denied'
            else:
                state = 'not_exist_or_password_error'

        context = {
            'loginForm': LoginForm(),
            'state': state,
        }
        return render(request, 'library/backstage_login.html', context)


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        state = None
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            #request.session['username'] = username

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse(u'Your account is disabled.')
            else:
                state = 'not_exist_or_password_error'

        context = {
            'loginForm': LoginForm(),
            'state': state,
        }
        return render(request, 'library/login.html', context)


def user_register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    registerForm = RegisterForm()
    state = None
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST, request.FILES)
        password = request.POST.get('password', '')
        re_password = request.POST.get('re_password', '')
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        photo = request.FILES['photo']

        if password == '' or re_password == '':
            state = 'empty'
        elif password != re_password:
            state = 'repeat_error'
        elif User.objects.filter(email=email):
            state = 'email_exist'
        else:
            username = request.POST.get('username', '')
            #request.session['username'] = username

            if User.objects.filter(username=username):
                state = 'user_exist'

            else:
                new_user = User.objects.create_user(username=username, password=password, first_name=name, email=email)
                UserProfile.objects.create(user=new_user, name=name, phone=username, email=email, photo=photo)

                state = 'success'
                auth.login(request, new_user)
                context = {
                    'state': state,
                    'registerForm': registerForm,
                }
                return render(request, 'library/register.html', context)

    context = {
        'state': state,
        'registerForm': registerForm,
    }
    return render(request, 'library/register.html', context)


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')

        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'

    context = {
        'state': state,
        'resetPasswordForm': ResetPasswordForm(),
    }
    return render(request, 'library/set_password.html', context)


@login_required
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        try:
            userprofile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            return HttpResponse('no this id user')

        context = {
            'state': request.GET.get('state', None),
            'userprofile': userprofile,
        }
        return render(request, 'library/profile.html', context)


def check(request):
    mission_id = request.GET.get('mission_id', None)
    domission_id = request.GET.get('domission_id', None)
    print(mission_id)

    if not mission_id:
        return HttpResponse('there is no such an mission_id')
    try:
        mission = Mission.objects.get(pk=mission_id)
        domission = DoMission.objects.get(pk=domission_id)
        domissionimage = DoMissionImage.objects.filter(domission_id=domission_id)
    except Mission.DoesNotExist:
        return HttpResponse('there is no such an mission_id')
    except DoMission.DoesNotExist:
        return HttpResponse('there is no such an mission_id')

    action = request.GET.get('action', None)
    state = None

    if action == 'pass':
        if not request.user.is_authenticated():
            state = 'no_user'
        else:
            if domission.is_pass == 0 or domission.is_pass == 2:
                DoMission.objects.filter(pk=domission_id).update(is_pass=1)
                UserProfile.objects.filter(phone=domission.executor).update(integral=F('integral')+mission.cost)
                state = 'pass_success'
            else:
                state = 'pass_error'

    elif action == 'notpass':
        if not request.user.is_authenticated():
            state = 'no_user'
        else:
            if request.user.username == admin:
                if domission.is_pass == 2:
                    DoMission.objects.filter(pk=domission_id).update(is_pass=-1)
                    Mission.objects.filter(pk=mission_id).update(amount=F('amount')+1)
                    state = 'notpass_admin'
                else:
                    state = 'notpass_error'
            else:
                if domission.is_pass == 0:
                    DoMission.objects.filter(pk=domission_id).update(is_pass=2)
                    state = 'notpass_success'
                else:
                    state = 'notpass_error'

    context = {
        'state': state,
        'mission': mission,
        'domission': domission,
        'domissionimage': domissionimage,
    }
    return render(request, 'library/check.html', context)


def mission(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        missionForm = MissionForm()
        state = None

        if request.method == 'POST':
            missionForm = MissionForm(request.POST, request.FILES)
            _type = request.POST.get('type', '微信投票')
            description = request.POST.get('description', '')
            cost = request.POST.get('cost', '')
            amount = request.POST.get('amount', '')
            capital = 59
            totalcost = (int(capital)+int(cost))*int(amount)
            imageshot = request.FILES.getlist('imageshot')
            username = request.user.username

            userprofile = UserProfile.objects.get(phone=username)
            if userprofile.integral - totalcost < 0:
                state = 'integral_error'
            else:
                mission = Mission.objects.create(user=username, type=_type, description=description, imageshot=imageshot[0], cost=cost, amount=amount, capital=capital, totalcost=totalcost, date_mission=timezone.now())
                MissionImage.objects.create(mission=mission, imageshots=mission.imageshot, date_missionimage=timezone.now())
                del imageshot[0]
                for shot in imageshot:
                    MissionImage.objects.create(mission=mission, imageshots=shot, date_missionimage=timezone.now())

                UserProfile.objects.filter(id=userprofile.id).update(integral=F('integral')-totalcost)

                # userprofile.integral -= totalcost
                # userprofile.save()
                # if UserProfile.objects.filter(id=userprofile.id, integral__gte=totalcost).update(integral=F("integral")-totalcost):
                #     #成功
                #     pass
                # else:
                #     #失败 积分不足
                #     pass

                state = 'success'
                context = {
                    'state': state,
                    'mission': mission,
                    'missionForm': missionForm,
                }
                return render(request, 'library/mission.html', context)

        context = {
            'state': state,
            'missionForm': missionForm,
        }
        return render(request, 'library/mission.html', context)


def mission_detail(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        mission_id = request.GET.get('mission_id', None)
        print(mission_id)
        if not mission_id:
            return HttpResponse('there is no such an mission_id')
        try:
            mission = Mission.objects.get(pk=mission_id)
            missionimage = MissionImage.objects.filter(mission_id=mission_id)
            missionlock = MissionLock.objects.filter(locker=request.user.username, mission_id=mission_id)
        except Mission.DoesNotExist:
            return HttpResponse('there is no such an mission_id')

        state = None
        action = request.GET.get('action', None)

        if action == 'mission_drop':
            MissionLock.objects.filter(locker=request.user.username, mission_id=mission_id).update(is_pass=4)
            Mission.objects.filter(pk=mission_id).update(amount=F('amount')+1)
            state = 'mission_dropped'
            return HttpResponseRedirect('/')

        if action == 'mission_accept':
            if request.user.username == mission.user:
                state = 'mission_error'
            elif MissionLock.objects.filter(locker=request.user.username, mission_id=mission_id):
                state = 'lock_exist'
            elif mission.amount <= 0:
                state = 'mission_empty'
            elif mission.amount > 0:
                MissionLock.objects.create(mission=mission, locker=request.user.username, issuer=mission.user, type=mission.type, description=mission.description, imageshot=mission.imageshot, cost=mission.cost, is_pass=3, date_lock=timezone.now())
                Mission.objects.filter(pk=mission_id).update(amount=F('amount')-1)
                state = 'mission_lock'
            else:
                state = 'unknown_error'

        context = {
            'state': state,
            'mission': mission,
            'missionimage': missionimage,
            'missionlock': missionlock,
        }
        return render(request, 'library/mission_detail.html', context)


def proof(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        mission_id = request.GET.get('mission_id', None)
        print(mission_id)
        if not mission_id:
            return HttpResponse('there is no mission_id')
        try:
            mission = Mission.objects.get(pk=mission_id)
            missionlock = MissionLock.objects.get(locker=request.user.username, mission_id=mission_id, is_pass=3)
        except Mission.DoesNotExist:
            return HttpResponse('there is no such an mission_id')

        state = None
        if request.method == 'POST':

            if DoMission.objects.filter(executor=request.user.username, mission_id=mission_id):
                state = 'domission_exist'

            else:
                proofForm = ProofForm(request.POST, request.FILES)
                proof = request.FILES.getlist('proof')
                domission = DoMission.objects.create(mission=mission, missionlock=missionlock, executor=request.user.username, issuer=mission.user, type=mission.type, description=mission.description, imageshot=mission.imageshot, proof=proof[0], cost=mission.cost, date_domission=timezone.now())
                MissionLock.objects.filter(id=missionlock.id).update(is_pass=domission.is_pass)

                DoMissionImage.objects.create(domission=domission, proof=domission.proof, date_domissionimage=timezone.now())
                del proof[0]
                for prf in proof:
                    DoMissionImage.objects.create(domission=domission, proof=prf, date_domissionimage=timezone.now())

                state = 'success'

            context = {
                'state': state,
                'mission': mission,
                'proofForm': ProofForm,
            }
            return render(request, 'library/proof.html', context)

        context = {
            'state': state,
            'mission': mission,
            'proofForm': ProofForm,
        }
        return render(request, 'library/proof.html', context)


def share(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        return render(request, 'library/share.html', {})
