from django.contrib import admin
from django.contrib.auth.models import User
from django import forms

from comptes.models import Clients, Commercials

admin.site.register(Clients)


class CommercialAdminForm(forms.ModelForm):

    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe",
        required=True,
        help_text="Laisser vide pour ne pas changer le mot de passe (en modification).",
    )

    class Meta:
        model = Commercials
        fields = ['nom', 'prenom', 'email', 'telephone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.user_id:
            self.fields['username'].initial = self.instance.user.username
            self.fields['password'].required = False
        else:
            self.fields['password'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if self.instance and self.instance.pk and self.instance.user_id:
            qs = qs.exclude(pk=self.instance.user_id)
        if qs.exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username


@admin.register(Commercials)
class CommercialAdmin(admin.ModelAdmin):
    form = CommercialAdminForm
    list_display = ('nom', 'prenom', 'user', 'email', 'telephone', 'date_creation')
    search_fields = ('nom', 'prenom', 'email', 'telephone', 'user__username')
    ordering = ('nom',)

    def save_model(self, request, obj, form, change):
        username = form.cleaned_data['username']
        password = form.cleaned_data.get('password')

        if obj.user_id:
            user = obj.user
            user.username = username
            user.email = form.cleaned_data['email']
            if password:
                user.set_password(password)
            user.save()
        else:
            user = User(
                username=username,
                email=form.cleaned_data['email'],
                is_staff=True,
            )
            user.set_password(password)
            user.save()
            obj.user = user

        super().save_model(request, obj, form, change)