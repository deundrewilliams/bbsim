from django.db import models

from ..classes import (
    Competition,
    NominationCeremony,
    VetoPlayers,
    VetoCeremony,
    EvictionCeremony,
    Finale,
    Week,
)


class Game(models.Model):

    MIN_PLAYERS = 5
    MAX_PLAYERS = 16

    HOH = 0
    NOM = 1
    POV = 2
    VETO_CEREMONY = 3
    EVICTION = 4
    FINALE = 5
    MEMORYWALL = 6

    GAME_STEP_CHOICES = (
        (HOH, 'HOH Competition'),
        (NOM, 'Nom Ceremony'),
        (POV, 'POV Competition'),
        (VETO_CEREMONY, 'Veto Ceremony'),
        (EVICTION, 'Eviction'),
        (FINALE, 'Finale'),
        (MEMORYWALL, 'Memory Wall'),
    )

    winner = models.ForeignKey(
        "Houseguest",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="game_winner",
    )
    jury = models.ManyToManyField("Houseguest", related_name="game_jury", default=[])
    prejury = models.ManyToManyField(
        "Houseguest", related_name="game_prejury", default=[]
    )
    completed = models.BooleanField(default=False)
    step = models.IntegerField(choices=GAME_STEP_CHOICES, default=MEMORYWALL)
    hoh = models.ForeignKey("Houseguest", on_delete=models.CASCADE, blank=True, null=True, related_name="game_hoh")
    nominees = models.ManyToManyField("Houseguest", related_name="game_nominees", default=[])
    pov = models.ForeignKey("Houseguest", on_delete=models.CASCADE, blank=True, null=True, related_name="game_pov")
    jury_size = models.IntegerField(default=0)

    def serialize(self):

        return {
            "id": self.id,
            "completed": self.completed,
            "current_step": self.GAME_STEP_CHOICES[self.step][1]
        }

    def setup_game(self):

        # Validate number of players
        num_players = len(list(self.players.all()))

        # Determine jury size and prejury size -> determine_jury_size(num_players)
        self.jury_size = self.determine_jury_size(num_players)

        # Get in house array of players
        in_house = [x for x in list(self.players.all())]

        # Initialize all relationships
        for hg in in_house:
            hg.initialize_relationships(in_house)

    def advance_step(self):
        # if completed, return nothing, or msg saying "game is completed"

        # If at memory wall step, return list of serialized players
        if self.step == self.MEMORYWALL:
            self.step = self.HOH
            return [x.serialize() for x in self.players.all()]

        # If at hoh step, run hoh comp and return hoh
        if self.step == self.HOH:
            self.run_hoh_competition(self.hoh)
            self.step = self.NOM
            return self.hoh.serialize()

        # If at noms, run nom ceremony and return noms
        if self.step == self.NOM:
            self.run_nomination_ceremony()
            self.step = self.POV
            return [x.serialize() for x in list(self.nominees.all())]

        # If at pov, get pov players, run pov comp and return pov holder
            # push step to veto ceremony
        if self.step == self.POV:
            pov_players = self.get_veto_players()
            self.run_veto_competition(pov_players)
            self.step = self.VETO_CEREMONY
            return self.pov.serialize()

        # If at veto ceremony, run ceremony, and return info
        if self.step == self.VETO_CEREMONY:
            meeting_info = self.run_veto_ceremony()
            self.step = self.EVICTION
            return meeting_info

        # If at eviction, run eviction and return info
        if self.step == self.EVICTION:

            eviction_info = self.run_eviction()

            if len([x for x in self.players.all() if x.evicted is False]) > 3:

                print([x for x in self.players.all() if x.evicted is False])

                self.step = self.MEMORYWALL
            else:
                self.step = self.FINALE

            return eviction_info

        # If at finale, run finale and return info, set completed to true
        if self.step == self.FINALE:

            finale_info = self.run_finale()

            self.completed = True

            return finale_info

    def determine_jury_size(self, num_players):

        if num_players <= 6:
            return 3
        elif num_players <= 12:
            return 5
        elif num_players <= 14:
            return 7
        else:
            return 9

    def run_hoh_competition(self, outgoing_hoh):
        """
        Runs the hoh competition

        :param outgoing_hoh: The current HOH that can't compete in this competition
        :type outgoing_hoh: 'simulator.models.Houseguest'
        """

        # Create competition using all players except current (outgoing) hoh
        playing = [x for x in self.players.all() if x != outgoing_hoh and x.evicted == False]

        hoh_comp = Competition(comp_type=Competition.HOH, participants=playing)

        # Run competition and get winner
        hoh_comp.run_competition()
        self.hoh = hoh_comp.winner

        # Set new hoh and update winner's comp count
        self.hoh.win_competition()

    def run_nomination_ceremony(self):

        # Create nom ceremony
        nom_ceremony = NominationCeremony(
            hoh=self.hoh, participants=[x for x in self.players.all() if x.evicted == False]
        )
        nom_ceremony.run_ceremony()

        # noms = list(nom_ceremony.nominees.all())

        # Get and set nominees
        self.nominees.set(nom_ceremony.nominees)

        # Update nominees' nomination count
        for nom in nom_ceremony.nominees:
            nom.nominate()

    def get_veto_players(self):

        # Create VetoPlayers
        vp = VetoPlayers(
            hoh=self.hoh,
            nominees=list(self.nominees.all()),
            participants=[x for x in self.players.all() if x.evicted == False],
        )

        # Run picking
        vp.pick_players()

        picked = vp.picked

        # Returned picked players
        return picked

    def run_veto_competition(self, veto_players):

        # Create Competition using veto players
        pov_comp = Competition(comp_type=Competition.POV, participants=veto_players)

        # Run competition and get winner
        pov_comp.run_competition()

        # Set pov holder and update winners' comp count
        self.pov = pov_comp.winner
        self.pov.win_competition()

    def run_veto_ceremony(self):

        # Create VetoCeremony
        vc = VetoCeremony(
            hoh=self.hoh,
            veto_holder=self.pov,
            nominees=list(self.nominees.all()),
            participants=[x for x in self.players.all() if x.evicted == False],
        )
        # Run ceremony
        vc.run_ceremony()

        # Set new nominees to equal ceremony nominees
        self.nominees.set(vc.nominees)

        return vc.serialize()

    def run_eviction(self):

        # Create Eviction Ceremony
        evc = EvictionCeremony(
            hoh=self.hoh,
            nominees=list(self.nominees.all()),
            participants=[x for x in self.players.all() if x.evicted == False],
        )

        # Run eviction
        evc.run_ceremony()

        # Update their evicted status
        evc.evicted.toggle_evicted(True)

        prejury_size = len(self.players.all()) - self.jury_size - 2

        # If before jury, move evictee into prejury
        if len(list(self.prejury.all())) < prejury_size:
            self.prejury.add(evc.evicted)
        else:
            self.jury.add(evc.evicted)

        return evc.serialize()

    def run_finale(self):

        # Create finale
        fn = Finale(finalists=[x for x in self.players.all() if x.evicted == False], jury=list(self.jury.all()))

        # Run finale
        fn.run_finale()

        # Set winner
        self.winner = fn.winner

        return fn.serialize()
