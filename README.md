# Temple Runner
## Description:
	Agent is trying to escape a trapped temple
	Temple is a maze of tiles and walls.
	Temple has an entrance, and an exit.
	Agent has acquired treasure and must navigate to the exit (Reward)
	Running through the maze is the safest option, but can tire the agent
	A tired agent is forced to take riskier actions
	Agent will have to figure out the best course of actions.
	Agent begins at an entrance, must survive, and proceed to exit.
## Actions
	> Can {Walk|Run|Sneak toward {North|South|East|West

## States
### Environmental States (Tiles):
 	Wall - Basic Barrier					
 	Floor - Regular Safe tile
 	Dart Tile - Shoots darts from the ceiling
 	Trap Door - Opens to a spike pit
### Agent States
 	Ready
 	Tired
 	Exhausted

## Transitions
	Environmental States (Tiles):
		Wall
			Cannot Pass with any action
		Floor
			Walk/Run/Sneak = 1.0 Safe
		Dart Tile
			Sneak = 0.60 Safe | 0.40 Dead
				Higher chance to survive by being careful.
			Walk = 0.10 Safe | 0.90 Dead
				Small chance darts miss
			Run = 1.0 Safe
				Darts completely miss
		Trap Door
			Sneak = 0.50 Safe | 0.50 Dead
				Less likely to fall in
			Walk = 0.20 Safe | 0.80 Dead
				Likely to fall in
			Run = 0.70 Safe | 0.30 Dead 
				Scramble over before it opens.
## Agent Properties
	CTE = 0.05-0.5 = Chance To Exhaust
	ETR = 5-0 = Exhausted Turns Remaining
## Agent States 
	Ready (ETR = 0)
		Run = 1.0 chance to become Tired
	Tired (ETR = 0, CTE = Between {0.05-0.5)
		Run = 1.0 chance to increase CTE by 0.05
		Run = CTE chance to become Exhausted
		Walk | Sneak = 1.0 chance to Reduce CTE by 0.05
	Exhausted (ETR = Between {5-0, CTE = 0.05)
		Run = 1.0 No Movement
		Walk | Sneak = 1.0 Move and Reduce ETR by 1
	P(Tired|_,Running) = 0.05 up to 0.5 chance to become tired
		Increases 0.05 each tile
		Tired = Can only walk or sneak for X number of turns
		Resets CTE to 0.05 after Exhaustion expires
		Decreases by 0.05 each time the Agent Walks/Sneaks 

## Rewards
	Dying = -100, 
	Exit = +100	
