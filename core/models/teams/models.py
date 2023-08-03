from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name="团队名称")
    description = models.CharField(blank=True, null=True, max_length=1000, verbose_name="团队简介")
    logo = models.ImageField(upload_to="teams_logo/", blank=True, null=True, verbose_name="团队logo")

    def delete(self, *args, **kwargs):
        #先解除队员的绑定
        self.TeamMember_set.clear()
        super().delete(*args, **kwargs)

class TeamMember(models.Model):
    teams = models.ManyToManyField(Team)
    MIB_ID = models.CharField(max_length=20)
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    email = models.EmailField()