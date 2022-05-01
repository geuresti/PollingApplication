from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Models are here to define data tables
# For this project I'm using a Poll model and an Answer model
#
# Answer objects are connected to Poll objects so by having a poll ID, I'm
# able to grab all the answers related to that Poll and display/manipulate them.
#
# My Poll model also has a creator field and a voter field. I'm using these to
# keep track of who made a Poll, as well as who voted on a Poll. This will
# help prevent users from editting each other's polls or from voting for the
# same poll twice.

class Poll(models.Model):
    title = models.CharField(max_length = 50)
    question = models.CharField(max_length = 100)
    post_date = models.DateField()

    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    voter = models.ManyToManyField(
        User,
        related_name='voters'
    )

    def __str__(self):
        return self.title

# answer is associated to a question, has text, has votes
class Answer(models.Model):
    votes = models.IntegerField(default = 0)
    text = models.CharField(max_length = 150)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
