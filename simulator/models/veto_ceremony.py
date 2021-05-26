from django.db import models

import random

class VetoCeremony(models.Model):

    hoh = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="veto_meeting_hoh")
    nominees = models.ManyToManyField('Houseguest', related_name="veto_meeting_init_noms")
    veto_holder = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="veto_meeting_pov")
    participants = models.ManyToManyField('Houseguest', related_name="veto_meeting_participants")
    using = models.BooleanField(default=None, null=True, blank=True)

    def serialize(self):

        data = {
            "HOH": self.hoh.serialize(),
            "Used": self.using,
            "Final Nominees": [x.serialize() for x in list(self.nominees.all())]
        }

        return data

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
            self.using = decision_info['Using']

        # If using
        if (self.using):

            # Determine renom
            renom = self.get_renom()

            renom.nominate()
            renom.impact_relationship(self.hoh, 3)

            # Remove old nominee from nominees, add new nominee
            self.nominees.remove(decision_info['On'])
            self.nominees.add(renom)

        return self.nominees

    def get_decision(self):

        # Get the relationship with nominees, keep the max val and player
        max_hg = self.veto_holder.choose_positive_relationships(list(self.nominees.all()))[0]
        max_val = self.veto_holder.relationships.get(player=max_hg).value

        # print(f'{max_hg} ({max_val})')

        # Generate a number 1 through 100, if <= max val, using, else not
        pick_value = random.randint(1, 100)

        if pick_value <= max_val:

            # Positively impact relationship
            max_hg.impact_relationship(self.hoh, 1)

            return {'Using': True, 'On': max_hg}
        else:
            return {'Using': False, 'On': None}


    def get_renom(self):

        # Create the nomination pool (excl. hoh, nominees, and veto holder)
        nom_pool = list(filter(lambda x: x != self.hoh and x not in list(self.nominees.all()) and x != self.veto_holder, list(self.participants.all())))

        # Randomly pick from the nomination pool
        # renom = random.choice(nom_pool)
        renom = self.hoh.choose_negative_relationships(nom_pool)[0]

        # Return picked player
        return renom
