from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):


    def create_user(self, email, username, description='', password=None):
        if not email:
            raise ValueError("email is a required field")
        if not username:
            raise ValueError("username is a required field")         
        
        
        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
            description = description,
        )


        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, username, password, description=''):
        user = self.create_user(
            email         = self.normalize_email(email),
            username      = username,
            password      = password,
            description   = description,
        )
        user.is_admin     = True
        user.is_active    = True
        user.is_staff     = True
        user.is_superuser = True
        user.save(using=self._db)
        return user