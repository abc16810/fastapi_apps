from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
import datetime


class AbstractUser(Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)
    email = fields.CharField(max_length=200, default="", unique=True)

    class Meta:
        abstract = True


class Users(AbstractUser):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    last_login = fields.DatetimeField(description="Last Login", default=datetime.datetime.now)
    avatar = fields.CharField(max_length=200, default="")
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

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
