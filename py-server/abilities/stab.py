from ..ability import Attack

class Stab(Attack):
    def __init__(self, name="Stab", ap_cost=10, cooldown_in_ticks=3, damage=5, damage_type="physical"):
        super().__init__(name, ap_cost, cooldown_in_ticks, damage, damage_type)

    def is_valid(self, player, target_tile, world):
        # Implement logic to check if the target is adjacent to the player
        if not super().is_valid(player, target_tile, world):
            return False

        # Logic to determine if the target tile is adjacent to the player
        # This could be something like checking the distance between player and target_tile
        return self.is_adjacent(player, target_tile)

    def is_adjacent(self, player, target_tile):
        # Implement the logic to check if the target_tile is adjacent to the player
        # Example logic here
        return True

    def use(self, player, target_tile, world, entity_target):
        """
        Executes the attack ability.
        :param player: The player using the ability.
        :param target_tile: The target tile of the attack.
        :param world: The current state of the world.
        """
        # Implementation of attack logic
        # Example: Reduce health of an enemy on target_tile, if any
        ret = []
        print(f"target: {entity_target}")
        try:
            if entity_target:
                ret.append(f"""(assert (damage
                                    (source {player.get_id()})
                                    (target {entity_target.get_id()})
                                    (amount {self.damage})
                                    (type {self.damage_type})
                                ))""")
            print(ret)
            return ret
        except Exception as e:
            print(e)