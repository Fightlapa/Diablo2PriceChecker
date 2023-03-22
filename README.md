# Diablo 2 price checker
### What it does
It prints estimation of value of Diablo2 rare items (currently amulets, rings and circlets)

### How to use it
It requires Python 3.7+

It doesn't require additional python packages to be installed.

It should work properly on MacOS, Windows, Linux

## Calculations
To calculate points for single modifier, it uses (almost) pure square function after mapping modifier values to be in range [0,1].


![alt text](https://i.stack.imgur.com/wa4iF.png)

So as an example. Assuming modifier can have values [10, 30] and item has value 28. Out of range of 20 values (21 exactly as it's inclusive, but it doesn't matter much in an example), it's 18.
Value is calculated as 18/20 which is 0.9.
Then the square function is applied, so 0.9^2, which gives 0.81 points. For perfect value(30) it will be 1. 


Using square function reflects d2jsp price changes when modifiers are perfect, for sure it's not ideal but it's all about estimation.
Same goes for low values for modifiers, it doesn't matter if attack rating in range [10,150] is 15 or 35, score will be very low for both: 0.01 and 0.05.
