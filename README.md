# Preamble
Hello! Please note that the following was a very manual way of finding a local (possibly global?) minimum. My general approach was to determine at which times the most people were at stations and create a rough schedule to give more service at those times. I then used a brute force approach by slightly modifying (increase or decrease by up to 5) two departure times. I then greedily selected the one that provided the minimum average wait time. I repeated this process until I found a minimum.

I tried increasing 1-2 values by a larger amount (up to 10) to try to escape any local minima and increase my chances of finding a global one.

Note: I assumed that trains would not idle in stations for longer than they needed to. This is an arbitrary assumption that made the model easier to work with. There may be small gains that are possible with short delays, but it would also annoy the passengers, which should be taken into consideration.

# Hackathon Notes

Average wait time: **3:39**.
Results: `result.csv`

I have another submission to McHacks so this is NOT an official submission. I just worked on it for fun and figured it would be nice to see how it stacked up against other people's solutions, in terms of best wait time found. For this reason, I did not make a visualization. 

# Running the Program
`python train_scheduling.py`