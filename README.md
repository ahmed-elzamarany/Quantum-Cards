# Quantum-Cards
The idea behind this game is to illustrate some aspects of the quantum computing. 
## The Game
This game is similar to the simple memory game ,but differs a litile bit XD

We have 3 levels that you can switch between them via the arrows.
We have a number of boxes in the middle , the number is determined according to the current level. *2^levelNo.*
Every time you finish a level the scores increases by 10.
We have two buttons "Measure", "Entanglement" that will discuiss their purpose later.
In the left you will find a box that illustrate the meaning of the samples
We have 2 modes in this game (dark,light).

### How to play ?
You choose 2 boxes and you can click "Entanglement" to increase your chances at winning for 1 point from your score then you click "Measure", 
If they are matched, they stay revealed. 
If not, you try again and repeat.
you win when all the boxes are matched.

**How is this game different ?**
I will tell you how.

## The Quantum Logic
In this game every box represents a quantum circuit that has a fixed number of qubits that are in the superpoistion.
The number of qubits in every circuit is increased by 1 each level.
When you click "Measure" you excute the circuit and every qubit will be collabsed to either a 0 or 1. *Which are represnted by different icons*
So, everytime you choose a box for measurement ,the hidden icons will change XD
When simulating the circuit we use the Aer simulater that is provided via Qiskit library 
Here is a sample circuit from the first level:
![alt text](https://github.com/ahmed-elzamarany/Quantum-Cards/blob/master/qc.jpg)

### Entanglement
Here where the magic happens!

When you choose "Entanglement" before measurement you increase your chances of winning up to 50% *your chances in winning in 1st level is 50% , 2nd level is 25% ,3rd level is 12.5%* by excuting different circuit that adds CNOT to entangle the qubits and reduce the outcomes of the circuits to 0's and 1's only *eg: "00" ,"11","000","111"* 

This is an example of the different circuit :
![alt text](https://github.com/ahmed-elzamarany/Quantum-Cards/blob/master/qc2.jpg)

