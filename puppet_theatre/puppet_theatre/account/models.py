from django.db import models
from django.contrib.auth import models as auth_models

from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from puppet_theatre.common.model_mixins import TimeStampedModel
from puppet_theatre.account.managers import AccountUserManager


class AccountUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin, TimeStampedModel):
    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
        
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True
    )
    
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True
    )
              
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    
    USERNAME_FIELD = "email"
    
    objects = AccountUserManager()
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
        
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

class Profile(models.Model):
    class Subjects(models.IntegerChoices):
        GRADE_1 = 1, '1-ви клас'
        GRADE_2 = 2, '2-ви клас'
        GRADE_3 = 3, '3-ти клас'
        GRADE_4 = 4, '4-ти клас'
        GRADE_5 = 5, '5-ти клас'
        GRADE_6 = 6, '6-ти клас'
        GRADE_7 = 7, '7-ми клас'
        GRADE_8 = 8, '8-ми клас'
        GRADE_9 = 9, '9-ти клас'
        GRADE_10 = 10, '10-ти клас'
        GRADE_11 = 11, '11-ти клас'
        GRADE_12 = 12, '12-ти клас'
        
    grade = models.PositiveSmallIntegerField(
        choices=Subjects.choices,
        # only if is needed a new God user
        # null=True,
        # blank=True,
        )
    
    user = models.OneToOneField(
        AccountUser,
        unique=True,
        editable=False,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    
    def __str__(self):
        return str(self.user.email)
    

class Bookmarks(models.Model):
    image_url = models.URLField()
    
    user = models.ForeignKey(
        AccountUser,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.user.email