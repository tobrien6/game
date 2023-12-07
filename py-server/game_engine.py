from event_manager import EventType
import asyncio
import traceback
import time

class GE:
    def __init__(self, world, rules_engine, event_queue):
        self.world = world
        self.rules_engine = rules_engine
        self.event_queue = event_queue

        self.rules_engine.define_functions([
            self.clips_apply_damage,
        ])

        rules_engine.add_rule("""
            (defrule py-apply-damage
                (apply-damage)
                ?d <- (damage (target ?target) (amount ?amount))
                =>
                (clips_apply_damage ?target ?amount)
                (retract ?d)
            )""")
        

    async def send_player_abilities(self, player):
        abilities = list(player.abilities.values())
        print(abilities)
        event = {'type': EventType.PLAYER_ABILITIES,
                 'data': {'action': 'PlayerAbilities', 'player_id': player.player_id, 'abilities': abilities}}
        await self.event_queue.put_event(event)


    async def use_ability(self, ability_name, player, target, world, charge=False):
        try:
            print(f"user {player.player_id} ability: {ability_name}")
            print(player.abilities)

            if ability_name not in player.abilities:
                raise ValueError("Ability not found")
            else:
                ability = player.abilities[ability_name]

            valid = await ability.is_valid(player, target, world)
            if not valid:
                # Generally the client should prevent the player from sending invalid action requests
                raise ValueError("Invalid usage of abilty")

            whiteboard = await ability.use(player, target, world)
            print(f"whiteboard {whiteboard}")

            # Evaluate and apply all effects
            events = self.clips_eval(whiteboard)

        except Exception as e:
            print(e)
            traceback.print_exc()


    def clips_apply_damage(self, target_id, amount):
        asyncio.run_coroutine_threadsafe(self.apply_damage(target_id, amount), asyncio.get_event_loop())

    async def apply_damage(self, target_id, amount):
        amount = float(amount)
        target_id = int(target_id)
        print(f"APPLY DAMAGE {target_id} {amount}")
        self.world.players[target_id].health -= amount
        health = self.world.players[target_id].health
        event = {'type': EventType.PLAYER_HEALTH,
                 'data': {'action': 'PlayerHealth', 'player_id': target_id, 'health': health}}
        await self.event_queue.put_event(event)


    def clips_eval(self, whiteboard):
        ts = time.time()
        print("clips eval starting")
        try:
            # Logic to evaluate and apply effects based on the whiteboard entries
            for fact in whiteboard:
                self.rules_engine.assert_fact(fact)
            self.rules_engine.run()
            ret = self.rules_engine.get_fact_strings()
            self.rules_engine.assert_fact("""(assert (apply-damage))""")
            self.rules_engine.run()
            ret = self.rules_engine.get_fact_strings()
            self.rules_engine.reset()
            print("clips output: " + str(ret))
            print(f"clips eval finished in {time.time() - ts} seconds")
            return ret
        except Exception as e:
            print(e)

    # ... remaining code ...












