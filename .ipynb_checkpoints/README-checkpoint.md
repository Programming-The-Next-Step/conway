# conway
![](https://upload.wikimedia.org/wikipedia/commons/e/e5/Gospers_glider_gun.gif)

## Game of Life 
Game of Life is a cellular automaton created by the mathematician John Horton Conway in 1970. A cellular automaton is a grid / lattice of cells. Each cell neighbors  the adjacent cells in the horizontal, vertical and diagonal (i.e., north, south, east, west, and diagonal) directions. In principle, the cells can be in one of many states at a given time. In the Game of Life, they can be in one of two states: on or off. The cells update their states over time as a function of the states of the neighboring cells. They follow a rule to do so that is called the _cell update rule_. For example: _"If the majority of the cells in my neighborhood is on, then turn on. Otherwise, turn off_. Consequently, the state of each cell at the next time point depends on the state of its neighboring cell at the current time point and the cell udpate rule. The collective behavior the cellular automaton depends on the cell update rule and the initial configuration of the cells. Althought the rules are constant, the initial pattern can be manipulated. Different initial patterns lead to different collective behavior. For example, the pattern shown in the GIF is called the _Gosper glider gun_.

### The Rules 
Conway set the rules in terms of life processesm which is why it is called the Game of Life. 
A cell is considered _alive_ if it is on, and _dead_ if it is off. The rules are: 
1. _Birth_: a dead cell with exactly three live neighbors becomes alive at the next time step. 
2. _Survival_: a live cell with exactly two or three live neighbors 
3. _Loneliness_: a live cell with fewer than two live neighbors dies and a dead cell with fewer than three live neighbors stays dead. 
4. _Overcrowding_: a live or dead cell with more than three live neighbors dies or stays dead. 

### How to use the software
