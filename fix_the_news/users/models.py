from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from fix_the_news.core.models import DateCreatedUpdatedMixin
from fix_the_news.users.validators import EmailValidator


class UserManager(auth_models.BaseUserManager):

    def _create_user(
            self, email, password, is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        user = self.model(
            email=email.lower(),
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(
            email,
            password,
            is_staff=False,
            is_superuser=False,
            **extra_fields,
        )

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True,
            **extra_fields,
        )


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):

    email_validator = EmailValidator()

    email = models.CharField(
        _('email'),
        max_length=254,
        unique=True,
        validators=[email_validator],
        error_messages={
            'unique': _("User with that email address already exists."),
        },
    )
    name = models.CharField(_('name'), max_length=254)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    avatar_thumbnail_small = \
        models.ImageField(upload_to="avatars", blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    has_viewed_registration_communication = models.BooleanField(default=False)
    has_viewed_daily_communication = models.BooleanField(default=False)
    no_upload_limit = models.BooleanField(
        default=False,
        help_text='If true this user ignores upload'
                  ' limits for topics and articles',
    )

    # settings
    subscribe_to_emails = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    ANONYMOUS_EMAIL = "@example.com"

    @classmethod
    def get_or_create_anonymous_user(cls, ipaddress):
        """
        So people can leave comments + like and add news items we create
        anonymous users based upon their ip address. This is so we can
        still enforce restrictions.

        For example limit a user to one like per news item.
        """
        email = f"{str(ipaddress).replace('.', '__')}{cls.ANONYMOUS_EMAIL}"
        user_query = cls.objects.filter(email=email)
        if user_query.exists():
            return user_query.first()
        return cls.objects.create(email=email, name="anonymous")


class Message(DateCreatedUpdatedMixin):

    email_validator = EmailValidator()

    email = models.CharField(max_length=254, validators=[email_validator])
    text = models.TextField()
    title = models.CharField(max_length=254)
    CONTACT_US = 'contact_us'
    HELP = 'help'
    TYPE_CHOICES = [
        (CONTACT_US, 'contact_us'),
        (HELP, 'help'),
    ]
    type = models.CharField(
        choices=TYPE_CHOICES,
        max_length=50,
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.email}, {self.type}'
