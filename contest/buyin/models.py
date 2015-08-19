from ..models import Action

class Buyin(Action):

    def __str__(self):
        return "Buyin Contest_Name:"+self.contest.name+" user_name:"+self.entry.lineup.user.username

