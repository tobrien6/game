import clips

DEFTEMPLATE_1 = """
(deftemplate damage
  (slot id (type INTEGER))
  (slot source (type STRING))
  (slot target (type STRING))
  (slot amount (type FLOAT))
  (slot type (type STRING)))
"""

DEFTEMPLATE_2 = """
(deftemplate resist
  (slot type (type STRING))
  (slot factor (type FLOAT))
  (slot player_id (type STRING))
  (multislot applied_to)) ; Add a multislot to track to which damage facts this resist has been applied
"""

DEFRULE_1 = """
(defrule damage-resistance
   ?d <- (damage (source ?source) (target ?target) (amount ?amount) (type ?type) (id ?id))
   ?r <- (resist (type ?type) (factor ?factor) (player_id ?target) (applied_to $?applied))
   (test (not (member$ ?id ?applied)))
   =>
   (bind ?reduced-amount (* ?amount ?factor))
   (modify ?r (applied_to $?applied ?id)) ; Mark this resist as applied to this damage source
   (modify ?d (amount ?reduced-amount))
)
"""

##
## Problem with this is that the resist fact is removed, but it might be relevant if there are multiple damage facts...
##


FACTS = ["""
(assert (damage (source "1") (target "2") (amount 10.0) (type "physical") (id 0)))
""", """
(assert (damage (source "1") (target "2") (amount 5.0) (type "physical") (id 1)))
""", """
(assert (resist (type "physical") (factor 0.9) (player_id "2")))
"""]

environment = clips.Environment()

# define templates
environment.build(DEFTEMPLATE_1)
environment.build(DEFTEMPLATE_2)

# define rules
environment.build(DEFRULE_1)

# eval facts
for f in FACTS:
	environment.eval(f)

# execute the activations in the agenda
environment.run()

final_facts = []
for f in environment.facts():
  final_facts.append(str(f))

print(final_facts)







