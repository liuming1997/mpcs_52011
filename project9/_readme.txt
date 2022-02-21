To run:

Open the ScorchedWaters folder in VMEmulator.

What works:

This is a very basic artillery game with semi-realistic physics simulating the fall of shot, depicting an artillery duel between the player's warship and a coastal defense fort. The AI in charge of the fort will attempt to adjust its aim as it goes; the first shot is always going to overshoot the player's ship.

Uses a random number generator from https://gist.github.com/ybakos/7ca67fcfd07477a9550b

What doesn't work:
Hitbox detection is very wonky due to the difficulty of making an array of pixels that the player's ship and the fort contain. It's no Python, that's for sure. What the game does is it calculates the final impact point of the shell, and compares it to a hitbox of the ship or the fort. But often times the last point of impact you see on the screen is NOT the true point of impact.
The RNG loads, but doesn't seem to actually do anything, or it does it so minutely that it's impossible to tell. But it does generate numbers.
A lot of things like having the AI adjust fire automatically were left on the cutting room floor because of time constraints, and so this game would be more feature-complete with them.
The lookup table for calculating the trajectory is very inefficient, but that's what happens when you don't have access to floats. It's literally a sine/cosine table hardcoded into Jack.
Just figuring out physics took me so long that I should've just made a Snake game instead. But I decided to go with this, because I thought it would be more interesting.
Azimuth is actually supposed to be elevation, but originally the player's ship and the fort could be in any direction to each other, and so the name stuck.

Jack is a very difficult language to program in; maybe Python has spoiled me.