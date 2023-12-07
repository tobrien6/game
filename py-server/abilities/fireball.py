import sys
sys.path.append("..")
from ability import Attack

class Fireball(Attack):
    def __init__(self, name="fireball", ap_cost=10, cooldown_in_ticks=10,
                 ability_range=10, effect_range=1, min_charges=0, max_charges=3,
                 damage_amt=10, damage_type="fire"):
        super().__init__(name, ap_cost, cooldown_in_ticks, 
                        ability_range, effect_range, min_charges, max_charges,
                        damage_amt, damage_type)


    ### NOTE: Need to have a unique ID in the CLIPS def for each damage fact. MISSING HERE
    def CLIPS_effect_fact(self, player, entity_target, world):
        return f"""(assert (damage
                    (source "{player.get_id()}")
                    (target "{entity_target.get_id()}")
                    (amount {float(self.damage_amt)}) 
                    (type "{self.damage_type}")
                ))"""