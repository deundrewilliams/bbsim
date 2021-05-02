from django.db import models

import random

class VetoCeremony(models.Model):

    hoh = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="veto_meeting_hoh")
    nominees = models.ManyToManyField('Houseguest', related_name="veto_meeting_init_noms")
    veto_holder = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="veto_meeting_pov")
    participants = models.ManyToManyField('Houseguest', related_name="veto_meeting_participants")
    using = models.BooleanField(default=None, null=True, blank=True)

    def run_ceremony(self):

        decision_info = {}

        # If veto holder is nominee, use on theirself
        if (self.veto_holder in list(self.nominees.all())):
            self.using = True
            decision_info['Using'] = True
            decision_info['On'] = self.veto_holder

        # If length of participants is 4 and holder is not hoh, don't use
        elif (self.veto_holder != self.hoh and len(list(self.participants.all())) == 4):
            self.using = False
            decision_info['Using'] = False
            decision_info['On'] = None

        # Else generate veto decision
        else:
            decision_info = self.get_decision()

        # If using
        if (self.using):

            # Determine renom
            renom = self.get_renom()

            # Remove old nominee from nominees, add new nominee
            self.nominees.remove(decision_info['On'])
            self.nominees.add(renom)

        return self.nominees

    def get_decision(self):

        if (self.using == None):
            self.using = random.choice([True, False])
        else:
            using = self.using


        # If True, pick one of the nominees to use it on
        if self.using:
            saved = random.choice(list(self.nominees.all()))
            return {'Using': True, 'On': saved}
        else:
            return {'Using': False, 'On': None}

    def get_renom(self):

        # Create the nomination pool (excl. hoh, nominees, and veto holder)
        nom_pool = list(filter(lambda x: x != self.hoh and x not in list(self.nominees.all()) and x != self.veto_holder, list(self.participants.all())))

        # Randomly pick from the nomination pool
        renom = random.choice(nom_pool)

        # Return picked player
        return renom
