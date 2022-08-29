from apps.models import Users
from tortoise import signals
from utils import hash_password


async def pre_save_users(_, instance: Users, using_db, update_fields):
    if instance.pk:
        db_obj = await instance.get(pk=instance.pk)
        if db_obj.password != instance.password:
            instance.password = hash_password(instance.password)
    else:
        instance.password = hash_password(instance.password)

signals.pre_save(Users)(pre_save_users)
