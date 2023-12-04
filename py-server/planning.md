0) Whenever a player action request comes in, an async system first computes all general
	possible actions that player could take based on if they have enough AP and the ability.
	This is just an initial check, not taking into account the target etc.


0) each effect, ability, etc. has pre-defined rules that are loaded into a CLIPS instance.

e.g.:
(defrule ability-ShieldBash
	()
)




1) player activates ability targeting target, shield bash

	-> list of queued effects: player.abilities["ShieldBash"].use(target)
	-> (use-ability ShieldBash player target)

	-> (assert (use-ability ShieldBash player target))

2) all effects are collected from player statements to CLIPS
	-> (damage-buff (type lightning) (multiplier 1.1))
	-> ()

3) 