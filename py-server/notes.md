""
###ABILITIES###

# BASIC ABILITIES

ATTACK -> passive grants a chance to counterattack when ambushed (eg when resting in dangerous area)
	   -> active single target attacks a target
	   -> active AOE performs an AOE attack depending on weapon type (eg barehanded it would be a haymaker)


SPEED BUFF -> passive grants everyone in group lower AP cost for moving
		   -> active single-target grants one player a bigger buff for x turns
		   -> active AOE grants a buff in-between single target and passive for y turns
requires min song (tongue?)

if a mob aggros on a player, another player can cast a speed buff and they can run away


PROGNOSTICATION -> passive grants chance to be warned of hidden things
				-> active single-target on monster grants information about their next attack
				-> active AOE grants 50-100% (scaling) chance to detect hidden things in the area
requires min perception (eyes?)
requires min spirit (heart?)
scales with perception and spirit


ILLUMINATION -> passive grants light in a radius around the caster
			 -> single target can light a tile on fire
			 -> ??? aoe warms an area, melting ice etc
requires min spirit (heart?)


ANALYZE -> passive grants general information on entities and objects in world which character has knowledge about (eg edible plants, mob basics)
		-> active single targer grants information on a specific mob, such as its buffs, its weaknesses, etc.
		-> active AOE forages for harder-to-find edibles, plus a lower chance to detect hidden things
requires min perception
affected by knowledge


###SKILLS###

REST -> if there are no mobs around, converts hunger into health and stamina

LITERACY<LANGUAGE> -> Grants ability to read books in language. Books may be found in world from ancient times, read, and brought to a library.
				   -> Partial literacy gives certain words. Full literacy can give 

COOK -> Can combine ingredients over a fire into food, potentially giving buffs

EAT -> Consumes food, but depending on food might take a fair amount of action points, so cannot do in fight.
	-> Gives slow regen of hunger stat

###TRADES###

HISTORIAN -> grants ability to learn about monster abilities, weaknesses, patterns when at library
				(in gameplay you can see the monster ability list and any status effects (like weakness to holy))
		  -> grants ability to write in new books passing along information

requires min intellect
requires literacy
requires access to a library





###PLAYER STATS###

Primary External:
Strength
	- affects how much you can carry (important for food etc on lower levels), i.e. stamina cost is lower per unit carried
	- certain abilities scale based on it
Dexterity
	- affects speed and stamina cost moving on difficult terrain
	- certain abilities based on it
Constitution

Primary Internal:
Heart
Intellect
Spirit

Secondary:
Stamina
	- goes down very slowly when moving, faster when fighting or moving on rough terrain. Affected by Constitution.

Hunger
	- affects stamina regeneration rate
	- increases over time, faster depending on circumstances (fighting, rough terrain)
	- when hunger is above a certain level, it grants very slow regeneration of health (so if you rest and time passes, you can regen)
	- may decrease stats when very low, eventually slowly decreasing max health until death
		- not an issue on surface or early levels, where there are fruit trees etc.

Spirit


### PROGRESSION ###

- You spawn into game as a person from an NPC camp/village/city (you can choose from a selection).
- There is minimal progression with that specific character.
- You can jump into game right away, no grinding. Your character is already equipped based on their job/position in the world.
	- eg peasant, wretch, guard, fisherman, explorer, ranger, hunter, historian, etc.
- Progression comes from developing the camp/town/city, which increases population, diversity, and productive capacity
	- eg a forge and barracks means that you will often get the option to play as a well-equipped soldier.

- What is gameplay loop?
	- On the surface, you can farm, fish, forage, mine, etc. to help build city.
	- You can adventure into caves, dark forests, or down into the abyss.
	- Just as city-building is a collective activity, so too is abyss exploration. Requiring players build infrastructure along the way.
	- When you spawn as a character, you choose a short-term life goal, like farm x, explore x caves, etc.
		- When you complete this, it is recorded, it helps the settlement, and that character can select a new step on their life path.e
		- Character life paths are like Slay the Spire maps, where you can choose to travel along them.
		- Like Slay the Spire, there are three acts: early age, middle age, and old age.
		- Your life path maps are set up depending on the character you selected. If you selected a farmer, most of their life path
			will be 

- Normal monsters drop mostly crafting supplies which are brought back to the town or cooked into food. They drop basic equipment in some
	cases, but rarely upgrades. So gearing up is not part of progression. However, like Slay the Spire, there are some larger events along
	the life path that can upgrade the character, by giving them new abilities, items, stats, etc. So the progression of one life is somewhat
	determined by the character origin (e.g. wretch, peasant, soldier, etc) but the player can choose which paths to go down to progress.
	For a farmer, there might be paths that are entirely peaceful (what would the "boss" encounters at the end of each act be?), while a wretch
	might have one of their boss encounters be to, say, seek out and kill a rat king in the sewer. This might give them an ability to transform
	into a rat, or a the ability to turn a normal dagger into a poison dagger, or ability to charm rats, etc. If the player completes the life
	path of that character, that ability can be part of a boon bestowed on a future life (they may start with ability to charm rats). There can
	be meta-unlocks like "incarnate as a minor rat god" which involves first collecting multiple rat-related boons over several lives, then
	stacking them on a new character (what determines how you can stack boons? how is it balanced?).

- Most of the setup for the nodes in the life path are text-based narratives describing e.g. your interactions with people, setup for your
	goal, etc. The game then potentially spawns NPCs, events, structures, resources, etc. to ensure that you can complete the node, and
	guides you to where you need to be.

- Perhaps when you play a class a second, third, etc. time after beating it, the stats and difficulty of quests are auto-adjusted
	based on player statistics, such that a certain failure rate is maintained. Automatic rebalancing seems important.

- An individual life should be fun and interesting on its own, not even counting potential abyss exploration after you complete it.
- Fun and interesting meaning that there is a sense of meaningful progression, customization, 

- Player of games, a gambler who plays a bunch of games like go, poker, etc. You can then use these potentially against certain intelligent beings
	in the abyss.



### STORY ###

- You are a minor god who is subservient to one of the nine elder gods. This world is like a chess board for the elder gods.
- Over several character lives, you as a minor god get favor with your elder god, allowing you to perform certain miracles, or even posess a hero.
- You must complete a full life path of a peasant in order to be able to posess more powerful characters. There are player-specific and settlement-specific
	pre-requisites for incarnating as more advanced "classes"/backgrounds (no explicit classes).
- If you successfully finish the three-act life path of a character, that character is added to a pool of characters who may journey into the abyss.
- By finishing the life path, you also unlock certain boons or advantages for future lives, settlement upgrades/benefits, etc.



### USER GENERATED CONTENT ###

- One path a player may go down is mutating monsters to create new monsters which mix and match abilities, etc.
- Camps/town/villages are instances that players can build inside. 


### MISC ###

Ability details:

abilities are always unlocked with the passive first, then the player can obtain items which
allow it to be turned into a single target (focus lens) or AOE (dispersive lens). Depending
on the item, the AOE can be shaped different, e.g. centered around caster, remote, cone, etc.

information about mobs should be specific enough that the internet or a wiki wont help. the
mob may or may not be wearing leather armor, may or may not have a current weakness, etc.


Adventure stories:

we took three mules down loaded with supplies. On level 2, after an ambush while resting, 
one of our party was injured and needed to be carried on a mule. That mule was consuming
too much food, and we needed some for ourselves, so it eventually collapsed and died. We
ate that mule and camped for days, giving the player time to heal enough to continue...





### CHATGPT NOTES ###

Good. Let's focus on use case studies now. Let's use a peasant as an example. Let's categorize different nodes for a peasant into three categories: basic, cumulative 1, cumulative 2, and capstone. Basic nodes have no pre-requisites: gathering seeds, foraging, maintaining crops, etc. Cumulative nodes have a set of pre-requisites: planting seeds, harvesting crops, etc. Cumulative 1 have 1 pre-requisite. Cumulative 2 have 2 pre-requisites. There are 3 capstone nodes, one at the end of each act. Help me brainstorm some nodes of each category. They should be FUN, have variety, and not be as boring as the examples I have listed. They should allow for strategy and replayability.
ChatGPT
Certainly! When designing nodes for a peasant character in an MMORPG, it's important to create engaging activities that go beyond mundane tasks, while still fitting within the theme of a peasant's life. Here are some brainstormed nodes for each category:

Basic Nodes
These nodes are immediately accessible and introduce players to the game mechanics and the peasant lifestyle.

Mysterious Crop Circles: Investigate strange patterns in the fields that could lead to a mini-game involving puzzle-solving.
The Great Chicken Escape: Chase and recapture escaped chickens from the coop, possibly requiring strategy to corner and capture them.
Market Day Bargaining: Engage in a timed mini-game where you haggle with buyers to get the best prices for your goods.
Secret Fishing Spot: Discover a hidden fishing spot where you can catch rare fish, which might require learning specific patterns or timings.
Potion Brewing with Homegrown Herbs: Create unique potions using a combination of herbs grown in your garden, with effects that can aid in various tasks.
Cumulative 1 Nodes
These nodes require the completion of one prerequisite and expand on the basic activities, leading to more complex gameplay.

Moonlit Harvest: A night-time event where crops harvested under the moon have special properties, requiring strategic planning of the harvest schedule.
Livestock Fair: Prepare and show your best livestock in competitions, which would require prior tasks like feeding and grooming animals.
The Old Mill's Secret: Repair and operate an ancient grain mill that produces more flour, involving a rhythm-based mini-game.
Beekeeping Bonanza: Manage a beehive to produce honey, involving a mini-game where you calm bees and extract honey without getting stung.
Cumulative 2 Nodes
These require the completion of two prerequisites, offering more challenging and rewarding gameplay.

The Enchanted Scarecrow: Build and enchant a scarecrow that protects your crops and can come to life to help with various farm tasks through a mini-quest series.
Festival Preparation: Organize a village festival by gathering resources, decorating, and planning events, resulting in a boost to morale and resources.
Storm Chaser: Brace your farm against seasonal storms, requiring strategic reinforcement of buildings and protection of crops and animals.
Brewmaster's Request: Assist the local brewmaster in creating a special batch of ale using your crops, involving a sequence of timed mini-games.
Capstone Nodes
These are significant events at the end of each act, requiring the completion of multiple prior nodes and significantly affecting the game world.

The Harvest Moon Gala: Host a grand gala celebrating the harvest, involving mini-games related to dancing, feasting, and storytelling, impacting your social standing and future interactions.
The Great Drought: Overcome a severe drought by managing water resources, leading to a dramatic mission to discover an ancient water source.
Defend the Harvest: Protect your village and its harvest from raiders or wildlife, involving strategy and possibly combat or diplomacy, which could affect the entire region's economy and safety.
By providing variety in gameplay through mini-games, puzzles, and strategic decision-making, these nodes aim to make the life of a peasant both fun and engaging, while also ensuring that players have the opportunity to employ different strategies and experience a high replay value.

User
I don't think I want separate minigames, but I like some of these ideas. I like the idea of a crop circle showing up in a field the player has planted, and what that might lead to. I consider crop circles a cumulative 1 node since it depends on the player having a field first (unless they started with one). This might place the player on a deterministic path to a specific capstone which the crop circle leads to.

Certain nodes like potion brewing can serve as a tutorial and also unlock a potential boon for future incarnations involving the recipes that player has learned. Thus, it might be valuable to bring along someone who has incarnated as farmer many times in the past, since they will be good at using monster body parts for recipes, using herbs to make salves, etc. Likewise, a path with beekeeping might teach the player about how some insects are repelled by smoke. 

Successfully completing a farmer path might unlock the ability to incarnate as more specialized people like chef, herbalist, etc. However, that also requires that the home settlement of the player is advanced enough, which is contributed to by every player's life paths.

A lot of brainstorming is required still. Keep in mind that the game is a 2d tile-based game. Let's now brainstorm some nodes for a soldier.
ChatGPT
For a soldier character in a 2D tile-based MMORPG, the nodes can incorporate elements of combat, strategy, and camaraderie. Nodes should also reflect the soldier's progression from a raw recruit to a seasoned veteran, with increasing complexity and impact on the game world.

Basic Nodes
No prerequisites, introducing the player to the soldier's life and basic combat.

Drill and Discipline: Execute a series of drills to improve stamina and learn basic formations, increasing your defense stats.
Weapon Mastery: Select a weapon to specialize in, leading to a series of quests to hone your skill with that weapon.
Patrolling the Borders: Patrol the edges of your territory, with chances to encounter minor skirmishes or find items.
Camp Maintenance: Keep the garrison in good shape by organizing supplies, which affects the readiness of troops for future encounters.
Messenger Duty: Deliver messages between commanders, uncovering hints of a larger narrative or potential threats.
Cumulative 1 Nodes
Require the completion of one prerequisite, bringing more engaging soldierly duties.

Scouting Mission: Venture into enemy territory to gather intelligence, requiring stealth and affecting the outcome of future battles.
Siege Training: Learn and practice siege tactics, which can be used to unlock siege-related events or battles.
Blacksmith Apprentice: Assist the blacksmith to learn about weapon and armor crafting, leading to improved gear.
Tournament of Arms: Participate in a friendly competition to win honor and rewards, potentially unlocking unique equipment or abilities.
Battlefield Medicine: Gain basic field medic skills, which can save comrades in future skirmishes.
Cumulative 2 Nodes
Require the completion of two prerequisites, involving strategic and significant combat roles.

Wartime Diplomacy: Engage with neutral factions to sway them to your side or ensure their neutrality, affecting resource flow and alliances.
Ambush Tactics: Set up an ambush for an enemy convoy, requiring careful planning and execution.
Fortification Construction: Oversee the building of a new fort, which becomes a strategic point on the map.
Veteran's Mentorship: Train new recruits, potentially affecting the quality of troops available in later engagements.
Guerrilla Warfare: Lead a series of hit-and-run missions on enemy camps, with each success increasing your stealth and attack stats.
Capstone Nodes
Significant events that require the completion of multiple nodes and have a profound impact on the character and the game world.

The Siege of the Ancient Fortress: Command the siege of a critical enemy stronghold, determining control over a region and unlocking new resources.
The Last Stand: Defend a strategic location against overwhelming odds, with success leading to a heroic reputation and special honors.
The King's Campaign: Lead a major offensive that involves multiple battles and decisions, ultimately affecting the political landscape of the game world.
These nodes for a soldier are designed to be deeply integrated into the world-building and lore of the MMORPG, providing a sense of progression and impact. They offer opportunities for strategy, resource management, and engagement with the game's military and political systems, ensuring that each player's journey as a soldier is unique and significant.

User
I like that several of the nodes give settlement benefits, like increasing the skill of the guards, expanding the city with new buildings, etc. Perhaps certain nodes are only assigned to incarnations when enough of certain resources have been provided, e.g. enough wood has been gathered by woodsmen to upgrade the forge, or something. I am not sure if we will have explicit classes like soldier and farmer. More likely, each incarnation will have some basic backstory that makes certain nodes more likely than others. But for now, we can classify them in this way. Let's brainstorm for a rogue/thief style class, which might involve things like stealth, subterfuge, pickpocketing, poisoning, assassination, traps, spying, etc. Some of these may put the player in the lands of an opposing faction (though through disguises they may be able to blend in unless other characters have high perception or use certain skills). This goes back to the "five factions" who are separated by far distances in the ring around the abyss. If a rogue quest involves something behind enemy lines, then pvp comes into the picture, which is a whole other can of worms. Perhaps each side has its own "outlands" which are pvp zones -- high risk, high reward. Some rogue quests would allow the rogue to go on a caravan to travel the far distance to the enemy outlands (whereas normally it would take a long time to travel there by foot or mount). Let's now brainstorm nodes for a rogue, but mark them pve or pvp depending on the type. 
ChatGPT
For a rogue/thief class, nodes can be designed to take advantage of their stealthy and cunning nature, with PvE nodes focusing on story and skill development, while PvP nodes engage them in riskier activities against other players.

Basic Nodes (PvE)
No prerequisites, introducing the player to stealth and subterfuge mechanics.

Shadow's Embrace: Learn to move unseen and unheard, improving your stealth abilities.
Sleight of Hand: Perfect your pickpocketing skills with a series of thefts, increasing dexterity.
Locks and Secrets: Become adept at lockpicking, opening new areas and treasure opportunities.
Poison Crafting: Mix basic poisons for your weapons or to sabotage enemies, leading to crafting proficiency.
Underworld Connections: Establish contacts within the thieves' guild, granting access to specialized gear and information.
Cumulative 1 Nodes (PvE)
Require one prerequisite, expanding the rogue's repertoire.

The Heist: Plan and execute a burglary on a wealthy estate, requiring prior knowledge from "Underworld Connections".
Forgery and Disguise: Create false documents or identities, which can be used to infiltrate enemy factions.
Trap Mastery: Design and deploy traps for unsuspecting targets, useful in both PvE and PvP scenarios.
Information Brokerage: Gather and sell information, influencing NPC relationships and faction standings.
Shadowmark: Leave secret signs for fellow rogues, providing benefits and warnings, depending on the mark.
Cumulative 2 Nodes (PvP)
Require two prerequisites, often leading to PvP interactions.

Enemy Espionage: Infiltrate an opposing faction's outpost to gather critical intelligence (requires "Forgery and Disguise" and "Information Brokerage").
Caravan Ambush: Set up an ambush for resource caravans in the PvP zones, yielding high rewards (requires "Trap Mastery" and "Shadowmark").
Assassin's Contract: Take out a high-profile target in enemy lands, affecting the PvP power balance (requires "Poison Crafting" and "Shadow's Embrace").
Capstone Nodes
Significant events with both PvE and PvP elements, shaping the rogue's legacy and the game's political landscape.

The Kingpin's Fall (PvE): Dismantle the operations of a corrupt official, leading to changes in faction control and law enforcement within your territory.
The Great Escape (PvE): Conduct a daring rescue of prisoners from an enemy dungeon, potentially unlocking them as allies or revealing key plot points.
Silent War (PvP): Engage in a covert war against the enemy faction's rogues, with each victory weakening their intelligence and resource networks.
By carefully balancing PvE and PvP nodes, rogues can enjoy a variety of gameplay experiences that cater to their skills and playstyles. The nodes encourage strategic thinking and can significantly impact the broader game world and faction dynamics.



