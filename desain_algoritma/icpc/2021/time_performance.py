import spider_walk # ganti ini 
import time
import random
import matplotlib.pyplot as plt
import pandas as pd

def time_performance():
    number_of_inputs = [10, 100, 1000, 10000, 100000, 200000, 500000, 1000000]

    time_records = []

    for case in range(len(number_of_inputs)):
        N = number_of_inputs[case]
        M = number_of_inputs[case]
        S = random.randint(1, N)

        bridges = []

        for _ in range(1, M + 1):
            D = random.randint(1, N)
            T = random.randint(1, N)
            bridges.append((D, T))


        start_time = time.perf_counter()
        spider_walk.solve_case(N, M, S, bridges)
        end_time = time.perf_counter()

        elapsed_time_ms = (end_time - start_time) * 1000

        time_records.append((N, M, elapsed_time_ms))

    
    # Plotting the performance graph
    Ns = [record[0] for record in time_records]
    Ms = [record[1] for record in time_records]
    times = [record[2] for record in time_records]
    plt.figure(figsize=(10, 6))
    plt.plot(Ns, times, marker='o')
    plt.title('Time Performance of Spider Walk Algorithm')
    plt.xlabel('Number of Strands (N)')
    plt.ylabel('Time (milliseconds)')
    plt.savefig('time_performance_spider_walk.png')
    plt.show()


    df = pd.DataFrame(time_records, columns=['Number of Strands (N)', 'Number of Bridges (M)', 'Time (milliseconds)'])
    df.to_csv('time_performance_spider_walk.csv', index=False)




if __name__ == "__main__":
    time_performance()

