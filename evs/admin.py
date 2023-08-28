from django.contrib import admin
from .models import Election, Candidate, Block, Vote

admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Block)
admin.site.register(Vote)