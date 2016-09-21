"""
   Program to simulate a Binary Symmetric Channel (BSC) with two states. 
   The channel can be in one of two states, "good" (pg) or "bad" (pb). 
   Regardless of the state, the channel acts like a BSC, but the state changes 
   the error bit rate of which the BSC operates. The channel switches its state 
   in a random fashion.
   
   Authors:
        Andrew Dallow
        James Priddy
"""

from math import factorial
from numpy import random
state = 0

def prompt_user():
    """Prompt the user for user data (u), the number of redundant bits (n-k) 
    and the error probability (p) and return these values."""
    
    user_data = int(input("Enter the amount of User Data (u): "))
    while (user_data <= 0):
        print("Please Enter an amount greater than 0.")
        user_data = int(input("Enter the amount of User Data (u): "))
    
    redun_bits = int(input("Enter the number of redundant bits (n - k): "))
    while (redun_bits < 0):
        print("Redundant bits must be greater than or equal to 0.")
        redun_bits = int(input("Enter the number of redundant bits (n - k): "))
        
    pg = float(input("Enter the 'Good' state bit error rate (pg): "))
    while (pg < 0 and pg > 1):
        print("Probability must be between 0 and 1.")
        pg = float(input("Enter the 'Good' state bit error rate (pg): "))
        
    pb = float(input("Enter the 'Bad' state bit error rate (pb): "))
    while (pb < 0 and pb > 1):
        print("Probability must be between 0 and 1.")
        pg = float(input("Enter the 'Bad' state bit error rate (pb): "))    
    
    return user_data, redun_bits, pg, pb    
    

def get_Coefficient(num_bits, i):
    """Return the Binomial Coefficient given num_bits and i"""
    
    return factorial(num_bits) / (factorial(i) * factorial(num_bits - i))    


def get_max_t(tot_data, num_redun_bits):
    """Return the error correction capability (t*), the maximum of wrong bits 
    that can be corrected using the Hamming Bound"""
    
    ham_sum = 0
    num_errors = 0
    packet_size = num_redun_bits + tot_data
    ham_bound = 2**(num_redun_bits)
    
    # The Hamming Bound is achieved provided the relationship is fulfilled    
    while (ham_sum <= ham_bound):
        ham_sum += get_Coefficient(packet_size, num_errors)
        num_errors += 1 
    
    return num_errors - 2


def get_num_errors(packet_size, pg, pb, pgg, pbb):
    """Return a random number of errors from a binomial probability distrubution 
    based on the current state and last state of the channel which determine
    whether to use pg in a "Good" state or pb in a "Bad" state"""   
    
    global state
    q = random.uniform()
    if state == 0: #If channel state is "Good"
        prob = pg
        if q >= pgg:
            state = 1
    elif state == 1: #If channel state is "Bad"
        prob = pb
        if q >= pbb:
            state = 0       
    return random.binomial(packet_size, prob, 1)


def getEfficiency(user_data, packet_size, tStar, prob):
    """Calculate a random number of errors in a given packet via a binomial 
    probability distrubultion and repeat until the number of errors is below
    the given threshold, then return the transmission efficiency"""
    
    num_transmissions = 1      
    
    pg = prob[0]
    pb = prob[1]
    pgg = 0.9
    pbb = 0.9
    
    num_errors = get_num_errors(packet_size, pg, pb, pgg, pbb)
    while (num_errors > tStar):
        num_errors = get_num_errors(packet_size, pg, pb, pgg, pbb)
        num_transmissions += 1       
    
    efficiency = user_data / (num_transmissions * packet_size)
          
    return efficiency


def run_sim(user_data, tStar, packet_size, prob):
    """Run a simulation with 1 million packets and return the average 
    efficiency"""
    
    transmit_eff = []
    num_trials = 1000000
    
    # Calculate the average efficiency over 1 million packets.
    for i in range(num_trials):
        transmit_eff.append(getEfficiency(user_data, packet_size, tStar, prob))      
        
    avg_efficiency = sum(transmit_eff) / num_trials
    
    return avg_efficiency

    
def main():
    """Run the Program"""
    
    overhead = 100
    # Prompt the User
    user_data, redun_bits, pg, pb = prompt_user()
    
    print("Running simulation for:")
    print("  User Data (u):", user_data)
    print("  Redundant Bits (n-k):", redun_bits)
    print("  Probabilities: pg = {}, pb = {}".format(pg, pb))    
    
    packet_size = overhead + user_data + redun_bits
    tot_data = overhead + user_data   
    
    # Calculate t*, the error correction capability
    tStar = get_max_t(tot_data, redun_bits)
    print("  Error Correction Capability: ", tStar)    
    
    # Calculate the average efficiency
    avg_eff = run_sim(user_data, tStar, packet_size, [pg, pb])
    
    print("Simulation Complete.")
    print("  The average effeciency of all packets is: {0:.4}".format(avg_eff)) 

main()