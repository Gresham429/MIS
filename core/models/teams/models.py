from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name="团队名称")
    description = models.CharField(blank=True, null=True, max_length=1000, verbose_name="团队简介")
    logo = models.ImageField(upload_to="teams_logo/", blank=True, null=True, verbose_name="团队logo")

    def delete(self, *args, **kwargs):
        #先解除队员的绑定
        related_team_members = TeamMember.objects.filter(teams=self)
        for team_member in related_team_members:
            team_member.teams.remove(self)
        super().delete(*args, **kwargs)

class Group(models.Model):
    group_name = models.CharField(max_length=50, verbose_name="组别")
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="所属团队")

    def __str__(self):
        return self.group_name

class TeamMember(models.Model):
    teams = models.ManyToManyField(Team)
    MIB_ID = models.CharField(max_length=20)
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.student_id} - {self.name}"
    
    def delete(self, *args, **kwargs):
        # 在删除成员之前，从关联的所有团队中删除该成员
        for team in self.teams.all():
            team.teammember_set.remove(self)
        super().delete(*args, **kwargs)