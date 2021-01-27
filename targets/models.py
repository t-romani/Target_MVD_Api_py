from django.db import models


# Method used to define image name before uploading to S3
# https://stackoverflow.com/questions/3091667/django-call-self-function-inside-a-django-model
def image_name(instance, filename):
    return instance.title


class Topic(models.Model):
    title = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to=image_name)

    def __str__(self):
        return self.title
