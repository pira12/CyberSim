NeDeS
==========================

NeDeS is a modern cybersecurity simulator made in Python. It
was designed from the ground up to provide the users with new features.
Some of the features that NeDeS has are:

-   Fast simulation
-   Easy acces to results
-   Customizable scenarios

Getting Started with NeDeS
===============================

NeDeS is very easy to use, and you do not need a lot to get
started!

Installation
------------

First of all, make sure you have the minimum requirements installed.

For example, on Ubuntu:

``` {.bash}
pip3 install -r requirements.txt
```

After running this command all the requirements are installed and you can
immediately use the NeDeS simulator.

Quickstart
----------

To start the simulator, you can use the
following command:

``` {.bash}
python3 simulator.py
```

Explaining the simulator
===============================


Settings sidebar
-----------------

**Start button:** This button will start the simulation when all the required fields are filled in correctly.

**Results button:** This button will show the results window when a simulation has finished running.

**Appearance mode selector:**
This dropdown menu has three options:
**Light:** This option will show the GUI in light mode.
**Dark:** This option will show the GUI in dark mode.
**System:** This option will show the GUI in the mode your computer system is set on.


**UI scaling selector:** This dropdown menu has multiple options for scaling the simulator. These are 80%, 90%, 100%, 110%, and 120%.

Systems tab:
-------------

**Network selector:** This dropdown menu will show the available networks to run the simulation on. When selecting a network the network preview will change with it.
		
**The number of simulations entry field:** This entry field will decide how many times the simulation will be run. Must be an integer.

**Simulation run time entry field:** This entry field will decide how long the simulated time will be. Must be an integer.

**Output folder name entry field:** This entry field will decide the name of the output folder will be named, which contains all the results.

Attacker tab
-------------

On the attacker tab, we create the number of attackers we want for a simulation and then decide which strategy and which actions they should use. 

To create attackers, fill in an integer in the attacker entry field and follow that by pressing the create attackers button. The graphical user interface will now generate that amount of attackers in the scrollable frame. 

Each attacker has its own id. Each attacker can also be set with an attacker strategy by selecting it in the dropdown menu.
The options are Random Strategy, Zero-day exploit, and Advanced Persistent Threats.

You will notice that each strategy has actions which are blocked, these can not be unselected and will remain selected, the other actions however can be selected or unselected.


Defender tab
-------------

There is only one defender in the simulator therefore all the options for the defender are shown in this tab.

First, the defender can choose its strategy by selecting one from the dropdown menu.
These are the options for the defenders’ strategy: 
random, last layer, minimum, reactive and random, highest degree neighbour.

The defender has split his actions into two parts. One part will affect the host and the other part will affect the edges between the hosts. The defender requires at least one defending action to be selected. 


Log tab
--------

The log tab displays the log for the latest simulation which has been finished running.


Results window
--------------

The results window will show a quick summary of the results of the simulation.

In the top left, we have the network topography after the simulation is finished. This topography will show which hosts have been compromised and which have not.

Underneath that, we have the plot of the scores of the attacker(s) and defender over time.

On the right side, there is a summary with all the valuable results from the simulation, which is divided into three parts: network, defender, and attacker.

When the simulation is run multiple times, then the results will be shown in an average over all the simulations. 




