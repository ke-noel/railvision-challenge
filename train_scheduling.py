'''
Hello! Please note that the following was a very manual way of finding a local 
(possibly global?) minimum. My general approach was to determine at which times 
the most people were at stations and create a rough schedule to give more service 
at those times. I then used a brute force approach by slightly modifying (increase 
or decrease by up to 5) two departure times. I then greedily selected the one that 
provided the minimum average wait time. I repeated this process until I found a minimum.

I tried increasing 1-2 values by a larger amount (up to 10) to try to escape any local
minima and increase my chances of finding a global one.

Note: I assumed that trains would not idle in stations for longer than they needed
to. This is an arbitrary assumption that made the model easier to work with. There may 
be small gains that are possible with short delays, but it would also annoy the
passengers, which should be taken into consideration.
'''
import copy

# The passengers at a station
passengers = {
    'A': [25,50,75,100,125,150,125,100,75,50,45,40,35,30,25,20,15,10,5],
    'B': [50,75,100,125,150,175,150,125,100,100,75,75,50,45,35,25,20,15,10],
    'C': [50,100,150,200,250,200,175,150,150,125,100,75,50,50,45,40,35,30,25],
}

# The times passengers arrive, converted to integers
times = [700,710,720,730,740,750,800,810,820,830,840,850,900,910,920,930,940,950,1000]

# Useful constants
dwell_time = 3
AB_time = 8
BC_time = 9
CU_time = 11
l4_cap = 200
l8_cap = 400
info_header = 'TrainNum,TrainType,A_ArrivalTime,A_AvailCap,A_Boarding,B_ArrivalTime,B_AvailCap,B_Boarding,C_ArrivalTime,C_AvailCap,C_Boarding,U_Arrival,U_AvailCap,U_Offloading\n'

# --- HELPER FUNCTIONS ---
def get_timeslot(time):
    # Return the most recent passenger arrival time
    # This means that the passengers at a station are the sum up until 
    # this timeslot.
    if time >= 1000:
        return 1000
    return time if time % 10 == 0 else int(str(time)[:2] + '0')

def fix_time(time):
    # Fix the time if it has gone over 60 minutes (960 becomes 1000)
    if time < 1000 and time > 959:
        return 1000 + (time - 960)
    elif time >= 1000:
        return time
    return time if int(str(time)[1]) < 6 else int(str(int(str(time)[0]) + 1) + '00')

def convert_time(time):
    # Convert to string
    if time >= 1000:
        return f'{str(time)[:2]}:{str(time)[2:]}'
    else:
        return f'{str(time)[0]}:{str(time)[1:]}'

# --- MAIN FUNCTIONS ---

def arrive_at_station(capacity, time, station, passengers):
    if capacity == 0:
        return 0, 0

    ti = times.index(get_timeslot(time))
    wait = 0

    # Move all passengers from previous timeslots to current
    if ti > 0 and passengers[station][ti-1] != 0:
        passengers[station][ti] += sum(passengers[station][:ti])
        for i in range(ti):
            if passengers[station][i] != 0:
                wait += passengers[station][i] * ((ti-i)*10)
                passengers[station][i] = 0

    # Pick up as many passengers as possible
    if passengers[station][ti] <= capacity:
        boarded = passengers[station][ti]
        wait += passengers[station][ti] * (time - get_timeslot(time))
        passengers[station][ti] = 0
    else:
        passengers[station][ti] -= capacity
        boarded = capacity
        wait += (time - get_timeslot(time)) * capacity

    return boarded, wait

def send_train(num, type, time, passengers):
    max_capacity = 200 if type == 'L4' else 400
    info = f'{num},{type},'
    capacity = max_capacity
    wait = 0
    
    # Visit station A
    new_boarded, new_wait = arrive_at_station(capacity, time, 'A', passengers)
    info += f'{convert_time(time)},{capacity},{new_boarded},'
    wait += new_wait
    capacity -= new_boarded

    # Travel to station B
    time = fix_time(time + dwell_time + AB_time)

    # Visit station B
    new_boarded, new_wait = arrive_at_station(capacity, time, 'B', passengers)
    info += f'{convert_time(time)},{capacity},{new_boarded},'
    wait += new_wait
    capacity -= new_boarded

    # Travel to station C
    time = fix_time(time + dwell_time + BC_time)

    # Visit station C
    new_boarded, new_wait = arrive_at_station(capacity, time, 'C', passengers)
    info += f'{convert_time(time)},{capacity},{new_boarded},'
    wait += new_wait
    capacity -= new_boarded

    # Travel to Union Station
    time = fix_time(time + dwell_time + CU_time)

    # Update the info
    info += f'{convert_time(time)},{capacity},{max_capacity-capacity}\n'

    return info, wait

def send_trains(start_times, types):
    wait = 0
    infos = info_header
    num_passengers = sum([sum([n for n in passengers[p]]) for p in passengers])
    for n,s,t in zip(range(1,17), start_times, types):
        info, new_wait = send_train(n, t, s, passengers)
        infos += info
        wait += new_wait
    return wait / num_passengers, infos

# --- Code used for finding the minimum ---
def find_min(passengers):
    good_times = [700,710,720,729,737,740,750,800,807,810,820,840,900,910,930,1000]
    good_types = ['L8','L8','L8','L8','L8','L8','L8','L8','L8','L8','L8','L8','L4','L4','L4','L4']
    ps = copy.deepcopy(passengers)

    best = good_times
    min_delay = 500
    for i1 in range(10):
        for i2 in range(10):
            for t1 in range(len(good_times)):
                for t2 in range(len(good_times)):
                    passengers = copy.deepcopy(ps)
                    ts = copy.deepcopy(good_times)
                    ts[t1] = fix_time(ts[t1] + i1 - 5)
                    ts[t2] = fix_time(ts[t2] + i2 - 5)
                    if len(set(ts)) == len(ts):
                        delay, _ = send_trains(ts, good_types)
                        if delay < min_delay:
                            min_delay = delay
                            best = ts
    print(min_delay)
    print(best)

# --- FINAL DEPARTURE TIMES AND TRAIN TYPES ---
if __name__ == '__main__':
    ideal_times = [700,710,720,729,737,740,750,800,807,810,820,840,900,910,930,1000]
    ideal_types = ['L8','L8','L8','L8','L8','L8','L8','L8','L4','L8','L8','L8','L4','L8','L4','L4']
    avg_wait, info = send_trains(ideal_times, ideal_types)

    print('The average delay per passenger with the following schedule is %.2fs, or 3:39.' %avg_wait)
    print(info)

    with open('result.csv', 'w') as f:
        f.write(info)