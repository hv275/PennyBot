Penny Points System

A player has the following attributes:
	No. of Pennys 		(Start at 10)
	Kills 			(Start at 0)
	Deaths 			(Start at 0)
	ATTACK			(Start at 0)
	DEFENCE			(Start at 0)
	Blocking		(Start at FALSE)
	Level			(Start at 0 or 1) (I vote 0)

And the following abilities/  methods:
	Penny (Player2)		Attempt to penny another player. At least one penny is required
	Hold_glass		Hold your glass for 30 seconds, 2 min cooldown
	Snipe (Player2)		Attempt to throw your penny into someone's glass. Will bypass hold
					and DEFENCE stats, but has significantly lower success rate
	Give(Player2, number)	Give another player some of your pennys. At least one penny is required
	Check (Player2)		Check the status of another player, such as their Level, ATTACK and DEFENCE,
					and then dependant on the difference in the player's levels (?),
					whether they're blocking, and what the chance of success is

The Points system itself:
	Upon an attempt:	The success probability is calculated using the attacker's ATTACK and the
					defender's DEFENCE points (exactly how can be figured later). If successful,
					the attacker's ATTACK will go up by [1-prob], where prob is the success
					probaility, and the defender's DEFENCE will go up by [prob/3], as well as
					the attacker's "Kills" incrementing, and the target's "Deaths". Upon an
					unsuccessful attempt, the target's DEFENCE will go up by [prob], with no
					gain for the attacker. Either way, a penny will be transferred from the
					attacker to the target. This goes for both "Penny" and "Snipe", with the
					only difference being the system to calculate [prob].

	Levels:			Levels will be calculated by taking the logarithm of the sum of ATTACK and DEFENCE.
					the base of the logarithm can be decided later. Higher levels will grant
					players extra abilities, such as "Snipe" and being able to see another
					player's "Blocking" status when they use "Check". I suggest a possible
					level cap, but advise against caps for ATTACK and DEFENCE stats, as these
					are effectively a player's overall points.

	Seating arrangements?	Due to the usual nature of pennying, you can only really target those nearby, unless
					you walk around. A way i think we could potentially mimick this is to restrict
					people to pennying only those who are "seated" adjacent and diagonal to
					themselves. An ability such as check_neighbours could allow for a player
					to see who they are able to penny, and another "Walk" ability could allow a
					player to penny anyone, except that everyone is notified that you are walking,
					giving people the chance to block. 