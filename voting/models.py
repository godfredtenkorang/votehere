from django.db import models
from django.contrib.auth.models import User

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)  # For ordering categories

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.election.title})"

class Candidate(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='candidates')
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='candidates/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)  # For ordering candidates
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.category.name}"

class Voter(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_key = models.CharField(max_length=50, unique=True)
    has_voted = models.BooleanField(default=False)
    vote_timestamp = models.DateTimeField(null=True, blank=True)
    
    

    def __str__(self):
        return f"{self.user.username} - {self.election.title}"

class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('election', 'category', 'voter')

    def __str__(self):
        return f"{self.voter.user.username} voted for {self.candidate.name} as {self.category.name}"