import traceback
import time

class GE:
    def __init__(self, world, rules_engine):
        self.world = world
        self.rules_engine = rules_engine

    async def process_rules_engine_outcomes(self, outcomes):
        pass

    async def use_ability(self, ability_name, player, target, world, charge=False):
        try:
            print(f"user {player.player_id} ability: {ability_name}")
            print(player.abilities)

            if ability_name not in player.abilities:
                raise ValueError("Ability not found")
            else:
                ability = player.abilities[ability_name]

            if not await ability.is_valid(player, target, world):
                # Generally the client should prevent the player from sending invalid action requests
                raise ValueError("Invalid usage of abilty")

            whiteboard = await ability.use(player, target, world)
            print(f"whiteboard {whiteboard}")

            # Evaluate and apply all effects
            self.clips_eval(whiteboard)
        except Exception as e:
            print(e)
            traceback.print_exc()

    def clips_eval(self, whiteboard):
        ts = time.time()
        print("clips eval starting")
        try:
            # Logic to evaluate and apply effects based on the whiteboard entries
            for fact in whiteboard:
                self.rules_engine.assert_fact(fact)
            self.rules_engine.run()
            ret = self.rules_engine.get_fact_strings()
            self.rules_engine.reset()
            print("clips output: " + str(ret))
            print(f"clips eval finished in {time.time() - ts} seconds")
            return ret
        except Exception as e:
            print(e)

    # ... remaining code ...












