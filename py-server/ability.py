from abc import ABC, abstractmethod

class Ability(ABC):
    def __init__(self, name, ap_cost, cooldown_in_ticks):
        self.name = name
        self.ap_cost = ap_cost  # Action points or other resources required
        self.cooldown_in_ticks = cooldown_in_ticks

    @abstractmethod
    def use(self, player, target_tile, world):
        """
        Executes the ability.
        :param player: The player using the ability.
        :param target: The target of the ability.
        :param world_state: The current state of the world.
        """
        pass

    @abstractmethod
    def is_valid(self, player, target_tile, world):
        pass

    @abstractmethod
    def cooldown(self):
        """
        Returns the cooldown time for the ability.
        """
        pass

    @abstractmethod
    def cost(self):
        """
        Returns the action point cost or other resource cost for using the ability.
        """
        pass


class Attack(Ability):
    def __init__(self, name, ap_cost, cooldown_in_ticks, damage, damage_type="physical"):
        super().__init__(name, ap_cost, cooldown_in_ticks)
        self.damage = damage  # Damage dealt by the attack
        self.damage_type = damage_type

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
                ret.append(f"""(assert
                                ({self.name} 
                                    (source {player.get_id()})
                                    (target {entity_target.get_id()})
                                )
                            )""")
            print(ret)
            return ret
        except Exception as e:
            print(e)

    def add_charge(self, player):
        # Implementation for adding a charge to the ability
        # Example: Increment ability charge count
        player.abilities[self.name].charges += 1

    def is_valid(self, player, target_tile, world):
        # Implementation to check if the attack can be executed
        # Example: Check if an enemy is present at target_tile
        return True
        #return world.is_enemy_at(target_tile)

    def cooldown(self):
        # Returns the cooldown time for the attack ability
        return self.cooldown_in_ticks

    def cost(self):
        # Returns the action point cost for using the attack ability
        return self.ap_cost


class Spell(Ability):
    def __init__(self, name, cost, effect, min_charges, max_charges, cooldown):
        super().__init__(name, cost)
        self.effect = effect
        self.min_charges = min_charges
        self.max_charges = max_charges
        self.cooldown = cooldown  # In ticks
        self.charges = 0
        self.last_cast_time = 0  # Timestamp of the last cast

    def add_charge(self, player):
        if self.is_on_cooldown():
            raise ValueError("Spell is on cooldown")

        current_time = time.time()
        if self.last_cast_time and current_time - self.last_cast_time < player.tick_time:
            raise ValueError("Cannot add charge yet")

        if self.charges < self.max_charges:
            self.charges += 1
            self.last_cast_time = current_time
            player.action_points -= self.cost
        else:
            raise ValueError("Spell has reached maximum charges")

    def is_valid(self):
        # not implemented
        return True

    def use(self, player, target_tile, world, charge):
        if charge:
            self.add_charge(player)
        if self.charges < self.min_charges:
            raise ValueError("Not enough charges to activate spell")
        # Spell activation logic
        pass

    def reset(self):
        self.charges = 0
        self.last_cast_time = time.time()

    def is_on_cooldown(self):
        return time.time() - self.last_cast_time < self.cooldown * player.tick_time()

    def interrupt(self):
        self.reset()
