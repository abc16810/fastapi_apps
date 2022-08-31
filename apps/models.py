from tortoise import Model, fields
from tortoise.validators import RegexValidator, Validator
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import ValidationError
from pydantic.errors import EmailError
from pydantic.networks import validate_email
from tortoise.validators import MaxLengthValidator
import datetime
import re


class UsernameValidator(Validator):
    """
    A validator to validate whether the given value is an even number or not.
    """
    def __call__(self, value: str):
        if value is None:
            raise ValidationError("Value must not be None")
        if len(value) < 3 or len(value) > 30:
            raise ValidationError(f"'{value}' length must be > 3")
        if not re.match('^[a-zA-Z]', value):
            raise ValidationError(f"'{value}' must start with a letter")
        value = value.strip()
        if re.match('\w+', value).group() != value:
            raise ValidationError("Invalid '{value}'")


class EmailValidator(Validator):
    """email validator"""
    def __call__(self, value: str):
        if value:
            try:
                validate_email(value)
            except EmailError:
                raise ValidationError("value is not a valid email address")


class AbstractUser(Model):
    username = fields.CharField(max_length=50, unique=True, index=True,
                                description="用户名名称",
                                validators=[UsernameValidator()])
    password = fields.CharField(max_length=200)  # 创建的列名为passwd
    email = fields.CharField(max_length=200, default=None, unique=True, validators=[EmailValidator()])

    class Meta:
        abstract = True


class Users(AbstractUser):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    last_login = fields.DatetimeField(description="Last Login", default=datetime.datetime.now)
    avatar = fields.CharField(max_length=200, default="")
    intro = fields.TextField(default="")
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        db_table = "user_test"


    def full_name(self) -> str:
        """
        Returns the best name
        """
        if self.name:
            return f"{self.name}".strip()
        return self.username

    def token(self) -> str:
        return self.username

    class PydanticMeta:
        # computed = ["token"]
        exclude = ("password", )

    def __str__(self):
        return f"{self.pk}#{self.username}"


User_Pydantic = pydantic_model_creator(Users, name="User")
# UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True, exclude=("last_login", ))
UserTokenResponse = pydantic_model_creator(Users,
                                             name="UserCreate",
                                             include=("username", "email", "avatar"),
                                             computed=("token", )
                                             )

UserName = pydantic_model_creator(Users, name="UserTest", include=("username","email"))
