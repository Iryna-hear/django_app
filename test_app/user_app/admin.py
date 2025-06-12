from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.utils import timezone
from user_app.models import User, UserPayment, UserAdress


# admin.site.register(User)
# admin.site.register(UserAdress)
admin.site.register(UserPayment)



class DataInput(forms.DateInput):
    input_type = 'date'


class UserAdressInline(admin.StackedInline):
    model = UserAdress
    extra = 1
    fields = ('street', 'city', 'postal_code')

class UserPaymentInline(admin.TabularInline):
    model = UserPayment
    extra = 1
    fields = ('amount', 'payment_date', 'payment_method')
    readonly_fields = ('payment_date',)
    

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'date_of_birth')
        widgets = {
            'date_of_birth': DataInput(),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Password', help_text="Raw passwords are not stored")
    new_password1 = forms.CharField(
        label='New Password', 
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank to keep the same password.")
   
    new_password2 = forms.CharField(
        label='New Password confirmation', 
        widget=forms.PasswordInput, 
        required=False)

    class Meta:
        model = User
        fields = ('__all__')
        widgets = {
            'date_of_birth': DataInput(),
        }

    def clean_password(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 or new_password2:
            if new_password1 and new_password2 and new_password1 != new_password2:
                raise forms.ValidationError("Passwords don't match")
            return new_password2
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get('new_password1')
        if new_password1:
            user.set_password(new_password1)
        if commit:
            user.save()
        return user

@admin.register(UserAdress)
class UserAdressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'postal_code')
    search_fields = ('user__email', 'street', 'city')
    list_filter = ('street', 'city')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserAdressInline, UserPaymentInline]
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'full_name','phone_number','is_active', 'preferred_language')
    list_filter = ('preferred_language', 'is_active')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('email',)
    actions = ['deactivate_user', 'activate_user']



    fieldsets = (
        (None, {'fields': ('email', 'is_active',)}),
        ('Change Password', {'fields': ('new_password1', 'new_password2'), 'classes': ('collapse',)}),
       
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_picture', 'phone_number'), 'classes': ('wide')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'is_active','phone_number', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth')
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


    def payment_total(self, obj):
        total = sum(payment.amount for payment in obj.userpayment_set.all())
        return f'{total} UAH'
    payment_total.short_description = 'Total Payments'

    def deactivate_user(self, request, queryset):
        update = queryset.update(is_active=False)

        self.message_user(request, f"{queryset.count()} users deactivated.")
    deactivate_user.short_description = "Deactivate selected users"

    def activate_user(self, request, queryset):
        update = queryset.update(is_active=True)

        self.message_user(request, f"{queryset.count()} users activated.")
    activate_user.short_description = "Activate selected users"

    class Media:
        js = ('admin/js/admin_user.js',)
