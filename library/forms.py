#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label=u'用户名：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        }),
    )
    password = forms.CharField(
        label=u'密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'password',
            'id': 'id_password',
        }),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label=u'用户名/手机号码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        }),
    )
    name = forms.CharField(
        label=u'名字：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'name',
            'id': 'id_name',
        }),
    )
    password = forms.CharField(
        label=u'密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'password',
            'id': 'id_password',
        }),
    )
    re_password = forms.CharField(
        label=u'重复密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 're_password',
            'id': 'id_re_password',
        }),
    )
    email = forms.CharField(
        label=u'电子邮件：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'email',
            'id': 'id_email',
        }),
    )

    photo = forms.FileField(
        label=u'头像：',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'name': 'photo',
            'id': 'id_photo',
        }),
    )


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(
        label=u'原始密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'old_password',
            'id': 'id_old',
        }),
    )
    new_password = forms.CharField(
        label=u'新密码：',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'new_password',
            'id': 'id_new',
        }),
    )
    repeat_password = forms.CharField(
        label=u'重复密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'repeat_password',
            'id': 'id_repeat',
        }),
    )


class MissionForm(forms.Form):
    TYPE_CHOICES = [
        (u'微信投票', u'微信投票'),
        (u'微博投票', u'微博投票'),
    ]

    type = forms.ChoiceField(
        label='任务类型：',
        choices=TYPE_CHOICES,
        widget=forms.Select(),
        initial=u'微信投票',
    )

    description = forms.CharField(
        label='任务描述：',
        max_length=100,
        widget=forms.Textarea(attrs={
            'class': 'form-control input-lg',
            'placeholder': u'请输入任务描述',
            'name': 'description',
        })
    )

    imageshot = forms.FileField(
        label=u'任务截图：',
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
            'class': 'form-control',
            'name': 'imageshot',
            'id': 'id_imageshot',
        }),
    )

    cost = forms.CharField(
        label=u'任务加价：',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'name': 'cost',
            'id': 'id_cost',
        }),
    )

    amount = forms.CharField(
        label=u'任务数量：',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'name': 'amount',
            'id': 'id_amount',
        }),
    )


class ProofForm(forms.Form):
    proof = forms.FileField(
        label=u'任务凭证：',
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
            'class': 'form-control',
            'name': 'proof',
            'id': 'id_proof',
        }),
    )

