"""
   Program to simulate a Binary Symmetric Channel (BSC) and calculate the average 
   effficiency given the user_data size (u > 0), the number of redundant bits 
   (n-k > = 0) and the probability (0 < p < 1) for N = 1000000 packets sent by a 
   transmitter. 

   Authors:
        Andrew Dallow
        James Priddy   
"""

from math import factorial
from numpy import random

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
        
    error_prob = float(input("Enter the bit error rate (p): "))
    while (error_prob < 0 or error_prob > 1):
        print("Probability must be between 0 and 1.")
        error_prob = float(input("Enter the bit error rate (p): "))
    
    return user_data, redun_bits, error_prob

    
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


def getEfficiency(user_data, packet_size, tStar, prob):
    """Calculate a random number of errors in a given packet via a binomial 
    probability distrubultion and repeat until the number of errors is below
    the given threshold, then return the transmission efficiency"""
    num_transmissions = 1
    
    num_errors = random.binomial(packet_size, prob)
    while (num_errors > tStar):
        num_errors = random.binomial(packet_size, prob)
        num_transmissions += 1        
    
    efficiency = user_data / (num_transmissions * packet_size)
          
    return efficiency


def run_sim(user_data, tStar, packet_size, prob):
    """Run a simulation with 1 mil trials and return the mean efficiency, 
    given user_data (u), tStar (t*), packet_size (n), and bit error rate (prob)
    """
    
    transmit_eff = []
    num_trials = 1000000
    
    # Calculate the average efficiency over 1 million packets.
    for i in range(num_trials):
        efficiency = getEfficiency(user_data, packet_size, tStar, prob)
        transmit_eff.append(efficiency) 
        
    mean_eff = sum(transmit_eff) / num_trials    
    return mean_eff    
    
           
def main():
    """Run the Program"""
    overhead = 100
    # Prompt the User
    user_data, num_redun_bits, error_prob = prompt_user()
    
    print("Running simulation for:")
    print("  User Data (u):", user_data)
    print("  Redundant Bits (n-k):", num_redun_bits)
    print("  Probability (p):", error_prob)
    # Calculate t*, the error correction capability
    packet_size = overhead + user_data + num_redun_bits
    tot_data = overhead + user_data    
    error_threshold = get_max_t(tot_data, num_redun_bits)
    
    print("  Error Correction Capability: ", error_threshold)    
       
    avg_eff = run_sim(user_data, error_threshold, packet_size, error_prob)
    print("Simulation Complete.")
    print("  The average effeciency of all packets is: {0:.4}".format(avg_eff))    

main()