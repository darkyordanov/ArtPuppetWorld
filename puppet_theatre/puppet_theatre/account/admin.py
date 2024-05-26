from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin

from puppet_theatre.account.forms import \
    AccountRegisterForm, AccountEditForm
    
from puppet_theatre.account.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(auth_admin.UserAdmin):
    list_display = ("email", "is_superuser", "is_staff")
    search_fields = ("email",)
    ordering = ("email",)
    
    form = AccountEditForm
    add_form = AccountRegisterForm
    
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name")}),
        ("Personal info", {"fields": ()}),
        ("Permissions", {"fields": ("is_active", "is_staff", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_email', 'grade',)
    list_filter = ('grade', )
    readonly_fields = ('user', )
    search_fields = ('user__email', 'user__created_at',)
    ordering = ('user__created_at',)

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = 'User Email'