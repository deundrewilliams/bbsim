from django.db import models

from ..models import Competition, NominationCeremony, VetoPlayers, VetoCeremony, EvictionCeremony, Week, Finale

class Game(models.Model):

    MIN_PLAYERS = 5
    MAX_PLAYERS = 16

    winner = models.ForeignKey('Houseguest', on_delete=models.CASCADE, blank=True, null=True, related_name="game_winner")
    jury = models.ManyToManyField('Houseguest', related_name="game_jury", default=[])
    prejury = models.ManyToManyField('Houseguest', related_name="game_prejury", default=[])
    completed = models.BooleanField(default=False)

    def serialize(self):
        data = {
            "id": self.id,
            "players": [x.serialize() for x in list(self.players.all())],
            "weeks": self.weeks if self.completed else [],
            "winner": self.winner.serialize() if self.completed else None,
            "jury": [x.serialize() for x in list(self.jury.all())],
            "prejury": [x.serialize() for x in list(self.prejury.all())],
            "finale": self.finale if self.completed else None
        }
        return data

    def run_game(self):

        # Validate number of players
        num_players = len(list(self.players.all()))

        # if (num_players < self.MIN_PLAYERS or num_players > self.MAX_PLAYERS):
        #     raise Exception("Too few/many players")

        # Determine jury size and prejury size -> determine_jury_size(num_players)
        self.jury_size = self.determine_jury_size(num_players)

        # Create in house array of players not evicted
        self.in_house = [x for x in list(self.players.all())]

        # Initialize an 'in jury' var and set it to false
        self.jury_began = False

        # Initialize current hoh to None
        self.current_hoh = None

        current_week = 1

        self.weeks = []

        # While in house array is > 3
        while (len(self.in_house) > 3):

            # Run each week
            week_data = self.run_week(current_week)

            # Add week to weeks array
            self.weeks.append(week_data)

            current_week += 1

        # Run finale
        self.run_finale()

        # Set completed to true
        self.completed = True

    def determine_jury_size(self, num_players):

        # 5 -> 3
        # 6 -> 3
        # 7 -> 5
        # 8 -> 5
        # 9 -> 5
        # 11 -> 5
        # 12 -> 5
        # 13 -> 7
        # 14 -> 7
        # 15 -> 9
        # 16 -> 9

        if (num_players <= 6):
            return 3
        elif (num_players <= 12):
            return 5
        elif (num_players <= 14):
            return 7
        else:
            return 9

    def run_week(self, week_number):

        # Check if in jury should be turned on
        if (self.jury_began == False and len(self.in_house) <= self.jury_size + 2):
            self.jury_began = True

        # Run HOH competition

        # Pass in current hoh
        self.run_hoh_competition(self.current_hoh)

        # Store current hoh in 'hoh'
        hoh = self.current_hoh

        # Run Nomination ceremony
        self.run_nomination_ceremony()

        # Store current noms in 'initial' noms
        initial_noms = self.current_nominees.copy()

        # Run Veto Players
        players = self.get_veto_players()

        # Run POV Competition
        self.run_veto_competition(players)

        # Store POV winner in 'pov'
        pov = self.pov_holder

        # Run Veto cerermony
        self.run_veto_ceremony()

        # Store current noms in 'final noms'
        final_noms = self.current_nominees

        # Run Eviction
        self.run_eviction()

        # Move evictee to correct spot
        self.in_house.remove(self.evicted)

        if (self.jury_began):
            self.jury.add(self.evicted)
        else:
            self.prejury.add(self.evicted)

        wk = Week(number=week_number, hoh=self.current_hoh, pov=self.pov_holder, evicted=self.evicted)
        wk.save()
        wk.initial_nominees.set(initial_noms)
        wk.final_nominees.set(final_noms)

        week_data = wk.serialize()

        wk.delete()

        return week_data

    def run_hoh_competition(self, outgoing_hoh):
        """
        Runs the hoh competition

        :param outgoing_hoh: The current HOH that can't compete in this competition
        :type outgoing_hoh: 'simulator.models.Houseguest'
        """

        # Create competition using all players except current (outgoing) hoh
        playing = [x for x in self.in_house if x != outgoing_hoh]

        hoh_comp = Competition(comp_type=Competition.HOH)
        hoh_comp.save()
        hoh_comp.participants.set(playing)

        # Run competition and get winner
        hoh_comp.run_competition()
        self.current_hoh = hoh_comp.winner

        # Set new hoh and update winner's comp count
        self.current_hoh.win_competition()

        hoh_comp.delete()

    def run_nomination_ceremony(self):

        # Create nom ceremony
        nom_ceremony = NominationCeremony(hoh=self.current_hoh)
        nom_ceremony.save()
        nom_ceremony.participants.set(self.in_house)
        nom_ceremony.run_ceremony()

        noms = list(nom_ceremony.nominees.all())

        # Get and set nominees
        self.current_nominees = list(nom_ceremony.nominees.all())

        # Update nominees' nomination count
        for nom in self.current_nominees:
            nom.nominate()

        nom_ceremony.delete()

    def get_veto_players(self):

        # Create VetoPlayers
        vp = VetoPlayers(hoh=self.current_hoh)
        vp.save()
        vp.nominees.set(self.current_nominees)
        vp.participants.set(self.in_house)

        # Run picking
        vp.pick_players()

        picked = list(vp.picked.all()).copy()

        vp.delete()

        # Returned picked players
        return picked

    def run_veto_competition(self, veto_players):

        # Create Competition using veto players
        pov_comp = Competition(comp_type=Competition.POV)
        pov_comp.save()
        pov_comp.participants.set(veto_players)

        # Run competition and get winner
        pov_comp.run_competition()

        # Set pov holder and update winners' comp count
        self.pov_holder = pov_comp.winner
        self.pov_holder.win_competition()

        pov_comp.delete()


    def run_veto_ceremony(self):

        # Create VetoCeremony
        vc = VetoCeremony(hoh=self.current_hoh, veto_holder=self.pov_holder)
        vc.save()
        vc.nominees.set(self.current_nominees)
        vc.participants.set(self.in_house)

        # Run ceremony
        vc.run_ceremony()

        # Set new nominees to equal ceremony nominees
        self.current_nominees = list(vc.nominees.all())

        vc.delete()

    def run_eviction(self):

        # Create Eviction Ceremony
        evc = EvictionCeremony(hoh=self.current_hoh)
        evc.save()
        evc.nominees.set(self.current_nominees)
        evc.participants.set(self.in_house)

        # Run eviction
        evc.run_ceremony()

        # Set evicted and update their evicted status
        self.evicted = evc.evicted
        self.evicted.toggle_evicted(True)

        evc.delete()

    def run_finale(self):

        # Create finale
        fn = Finale()
        fn.save()
        fn.finalists.set(self.in_house)
        fn.jury.set(list(self.jury.all()))

        # Run finale
        fn.run_finale()

        # Set winner and final juror
        self.winner = fn.winner
        self.final_juror = fn.final_juror

        self.finale = fn.serialize()

        fn.delete()

