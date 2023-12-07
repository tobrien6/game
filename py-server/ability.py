from abc import ABC, abstractmethod
from tile_utils import cheb_dist
import time

class Ability(ABC):
    def __init__(self, name, ap_cost, cooldown_in_ticks):
        self.name = name
        self.ap_cost = ap_cost  # Action points or other resources required
        self.cooldown_in_ticks = cooldown_in_ticks
        self.last_used_ts = 0
        
    def __repr__(self):
        return str(self.to_dict())


    @abstractmethod
    def use(self, player, target, world):
        """
        Executes the ability.
        :param player: The player using the ability.
        :param target: The target of the ability.
        :param world_state: The current state of the world.
        """
        pass

    @abstractmethod
    def is_valid(self, player, target, world):
        pass

    def in_cooldown(self, player, world):
        return self.cooldown_in_ticks > (time.time() - self.last_used_ts)*1000 / player.get_tick_time()

    def cost(self, player, world):
        # TODO: this might be modified by effects on the player or world
        return self.ap_cost
    
    # how the ability will be sent with json
    def to_dict(self):
        return {
            'name': self.name,
            'ap_cost': self.ap_cost,
            'cooldown_in_ticks': self.cooldown_in_ticks,
            'last_used_ts': self.last_used_ts
        }


class Attack(Ability):
    def __init__(self, name, ap_cost, cooldown_in_ticks,
                 ability_range, effect_range, min_charges, max_charges,
                 damage_amt, damage_type):
        super().__init__(name, ap_cost, cooldown_in_ticks)
        self.ability_range = ability_range
        self.effect_range = effect_range
        self.min_charges = min_charges
        self.max_charges = max_charges
        self.charges = 0
        self.damage_amt = damage_amt
        self.damage_type = damage_type


    @abstractmethod
    async def CLIPS_effect_fact(self, player, entity_target, world):
        pass

    async def get_target_entities(self, target, world):
        entities = await world.get_entities_in_range(target, self.effect_range)
        return entities

    async def use(self, player, target, world):
        # Implementation of attack logic
        # Example: Reduce health of an enemy on target_tile, if any
        ts = time.time()
        whiteboard = []
        # first apply any effect on the player
        whiteboard.extend(player.effects)
        for entity in await self.get_target_entities(target, world):
            # First apply the effect of the attack on the target entity
            whiteboard.append(self.CLIPS_effect_fact(player, entity, world))
            # Then apply any effects on the target entity
            whiteboard.extend(entity.effects)
        await player.update_action_points(-self.cost(player, world))
        self.last_used_ts = ts
        self.charges = 0
        return whiteboard

    async def add_charge(self, player, world):
        # Implementation for adding a charge to the ability
        self.last_used_ts = time.time()
        player.abilities[self.name].charges += 1
        await player.update_action_points(-self.cost(player, world))

    async def target_valid(self, player, target, world):
        player_pos = (player.x, player.y)
        return cheb_dist(player_pos, target) <= self.ability_range

    async def is_valid(self, player, target, world):
        cooldown_ok = not self.in_cooldown(player, world)
        target_ok = await self.target_valid(player, target, world)
        ap_ok = player.action_points >= self.cost(player, world)
        print(cooldown_ok, target_ok, ap_ok)
        return cooldown_ok and target_ok and ap_ok

    async def interrupt(self):
        self.charges = 0