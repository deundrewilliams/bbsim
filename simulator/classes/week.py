class Week:
    def __init__(
        self,
        number,
        hoh,
        initial_nominees,
        pov,
        final_nominees,
        evicted,
        vote_count,
        tied=False,
    ):
        self.number = number
        self.hoh = hoh
        self.initial_nominees = initial_nominees
        self.pov = pov
        self.final_nominees = final_nominees
        self.evicted = evicted
        self.vote_count = vote_count
        self.tied = tied

    def serialize(self):
        data = {
            "week_num": self.number,
            "hoh": self.hoh.name,
            "inoms": [x.name for x in self.initial_nominees],
            "pov": self.pov.name,
            "fnoms": [x.name for x in self.final_nominees],
            "evicted": self.evicted.name,
            "vote_count": self.vote_count,
            "tied": self.tied,
        }
        return data
