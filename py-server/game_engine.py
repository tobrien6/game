import traceback

class GE:
    def __init__(self, world, rules_engine):
        self.world = world
        self.rules_engine = rules_engine

    async def use_ability(self, ability_name, player, target_tile, world, charge=False, aoe=False):
        print(f"user {player.player_id} ability: {ability_name}")

        whiteboard = []

        try:
            print(player.abilities)

            if ability_name not in player.abilities:
                raise ValueError("Ability not found")

            try:
                ability = player.abilities[ability_name]
            except Exception as e:
                print(e)

            if player.action_points < ability.cost():
                raise ValueError("Not enough action points")
        except Exception as e:
            print(e)
            traceback.print_exc()

        if not ability.is_valid(player, target_tile, world):
            # Generally the client should prevent the player from sending invalid action requests
            # not implemented
            if False:
                raise ValueError("Invalid usage of abilty")

        if not aoe:
            # Check and apply ability effect on the target tile
            # returns a string with one or more assert statements for CLIPS
            # Note that a tile is targeted, but this will check if there is a player on it and return proper effects
            # ****currently assuming there is a player there
            entity_on_tile = await world.get_entity_at(target_tile)
            tentative_ability_outcomes = ability.use(player, target_tile, world, entity_on_tile)
            whiteboard.extend(tentative_ability_outcomes)

            if entity_on_tile:
                whiteboard.extend(entity_on_tile.effects)

        # Check for effects on nearby tiles if the ability has area effect
        if aoe:
            # ability aoe effect has a method to get aoe tiles, which might include target_tile
            aoe_tiles = ability.get_aoe_tiles(target_tile, world)
            for tile in aoe_tiles:
                # Apply effects to nearby tiles
                outcome = ability.apply_area_effect(player, tile, world)
                whiteboard.append(outcome)

        # Deduct action points after successful ability use
        player.action_points -= ability.cost()

        print(f"whiteboard {whiteboard}")

        # Evaluate and apply all effects
        clips_eval(whiteboard)


    def clips_eval(self, whiteboard):
        try:
            # Logic to evaluate and apply effects based on the whiteboard entries
            print(f"facts: rules_engine.facts()")
            for fact in tentative_ability_outcomes:
                rules_engine.assert_fact(fact)
            print(f"facts: rules_engine.facts()")
            rules_engine.run()
            ret = rules_engine.get_fact_strings()
            rules_engine.reset()
            print(ret)
            return ret
        except Exception as e:
            print(e)

    # ... remaining code ...












