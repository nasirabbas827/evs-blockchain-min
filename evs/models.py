from django.db import models 
from django.contrib.auth.models import User

class Election(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed')])

    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='candidates/', null=True, blank=True)
    description = models.TextField()
    election = models.ForeignKey(Election, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name
    
from django.db import models

class Block(models.Model):
    hash_code = models.CharField(max_length=64 , default='0')  # Hash code of the block
    previous_block = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    data = models.TextField()  # Data associated with the block
    nonce = models.CharField(max_length=64, default='0')
    hash = models.CharField(max_length=64)


    def __str__(self):
        return f"Block {self.id}"



class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True)


    