
from django.db import models
from users.models import Profile
import uuid
# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    def __str__(self):
        return str(self.title)
#
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    def __str__(self):
        return str(self.title)

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    details = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    total_target = models.FloatField()
    total_upvotes = models.IntegerField(default=0, null=True, blank=True)  # FIXME AA
    total_votes = models.IntegerField(default=0, null=True, blank=True)  # FIXME AA
    collected_donations = models.IntegerField(default=0, null=True, blank=True)  # FIXME AA
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    main_photo = models.ImageField(upload_to='projects/')
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-total_votes','-total_upvotes']



#
# #####################################################
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Project',on_delete=models.CASCADE,blank=True)
    image = models.ImageField(upload_to='projects/slider/')



#
#
# #################################################
class ProjectRate(models.Model):
    id = models.AutoField(primary_key=True)
    # TODO link to Profile instead of User
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    is_upvote = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

#
class Comment(models.Model):
    project = models.ForeignKey('Project',on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)

    class Meta:
        ordering = ['-created']

class Report(models.Model):
    REPORT_TYPE = (
        ('bully', 'Bully'),
        ('disrespectful behavior ', 'Disrespectful Behavior'),
        ('fraud', 'Fraud'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    value = models.CharField(max_length=200, choices=REPORT_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value
