from ..models import Action

class Refund(Action):
    def __str__(self):
        return "Refund Contest_Name:"+self.contest.name+" user_name:"+self.entry.lineup.user.username

