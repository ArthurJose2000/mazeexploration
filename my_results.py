import matplotlib.pyplot as plt
import csv

rows = []
with open("tarry_1to80agents_250iterations_20x20.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

tarry_steps_row = rows[1]
tarry_pionner_steps_row = rows[2]
tarry_fraction_row = rows[3]
tarry_stdev_row = rows[4]
tarry_steps_from_first_to_last_row = rows[5]

""" rows = []
with open("my_1to80agents_250iterations_20x20.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

my_steps_row = rows[1]
my_pionner_steps_row = rows[2]
my_fraction_row = rows[3]
my_stdev_row = rows[4]
my_fraction_pionner = rows[5] """

""" header = rows[0]

rows = []
with open("my_1to40agents_250iterations_30x30_v2.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

my_v2_steps_row = rows[1]
my_v2_pionner_steps_row = rows[2]
my_v2_fraction_row = rows[3]
my_v2_stdev_row = rows[4]
my_v2_fraction_pionner = rows[5] """

rows = []
with open("my_1to40agents_250iterations_40x40_strangepeaks.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

my_strange_peaks_steps_row = rows[1]
my_strange_peaks_pionner_steps_row = rows[2]
my_strange_peaks_fraction_row = rows[3]
my_strange_peaks_stdev_row = rows[4]
my_strange_peaks_fraction_pionner = rows[5]

my_strange_peaks_steps_pioneer_after_interval1_row = rows[6]
my_strange_peaks_steps_pioneer_after_interval2_row = rows[7]
my_strange_peaks_fraction_pioneer_after_interval1_row = rows[8]
my_strange_peaks_fraction_pioneer_after_interval1_row = [i*100 for i in my_strange_peaks_fraction_pioneer_after_interval1_row]
my_strange_peaks_fraction_pioneer_after_interval2_row = rows[9]
my_strange_peaks_fraction_pioneer_after_interval2_row = [i*100 for i in my_strange_peaks_fraction_pioneer_after_interval2_row]
my_strange_peaks_fraction_pioneer_in_interval2_row = rows[10]
my_strange_peaks_fraction_pioneer_in_interval2_row = [i*100 for i in my_strange_peaks_fraction_pioneer_in_interval2_row]
my_strange_peaks_steps_agents_using_interval2_row = rows[11]

my_strange_peaks_fraction_pioneer_in_interval1_row =[]
for e in my_strange_peaks_fraction_pioneer_after_interval1_row:
    my_strange_peaks_fraction_pioneer_in_interval1_row.append(100-e)

pioneer_steps_in_interval_1 = []
pioneer_steps_in_interval_2 = []
pioneer_steps_in_common_dfs = my_strange_peaks_steps_pioneer_after_interval2_row
for i in range(0, len(my_strange_peaks_pionner_steps_row)):
    pioneer_steps_in_interval_1.append(my_strange_peaks_pionner_steps_row[i] - my_strange_peaks_steps_pioneer_after_interval1_row[i])
    pioneer_steps_in_interval_2.append(my_strange_peaks_steps_pioneer_after_interval1_row[i] - my_strange_peaks_steps_pioneer_after_interval2_row[i])

""" plt.plot(header, my_strange_peaks_pionner_steps_row, 'x-', label = "Total")
plt.plot(header, pioneer_steps_in_interval_1, 'x-', label = "First interval")
plt.plot(header, pioneer_steps_in_interval_2, 'x-', label = "Second interval")
plt.plot(header, pioneer_steps_in_common_dfs, 'x-', label = "Common DFS") """



plt.plot(header, my_strange_peaks_fraction_pioneer_in_interval1_row, 'x-', label = "First interval")
plt.plot(header, my_strange_peaks_fraction_pioneer_in_interval2_row, 'x-', label = "Second interval")
plt.plot(header, my_strange_peaks_fraction_pioneer_after_interval2_row, 'x-', label = "Common DFS")


""" plt.plot(header, tarry_steps_row, label = "TARRY: Average of steps")
plt.plot(header, my_steps_row, label = "TG: Average of steps")

plt.plot(header, tarry_pionner_steps_row, label = "TARRY: Pionner's average of steps")
plt.plot(header, my_pionner_steps_row, label = "TG: Pionner's average of steps") """

""" plt.plot(header, tarry_fraction_row, label = "TARRY: Fraction of maze explored")
#plt.plot(header, my_fraction_row, label = "TG: Fraction of maze explored")
plt.plot(header, my_fraction_pionner, label = "TG: Fraction of maze explored until pionner") """

""" plt.plot(header, my_steps_row, label = "TG - Average of steps")
plt.plot(header, my_pionner_steps_row, label = "TG - Pionner's average of steps")
plt.plot(header, my_v2_steps_row, label = "TG (new) - Average of steps")
plt.plot(header, my_v2_pionner_steps_row, label = "TG (new) - Pionner's average of steps") """

""" plt.plot(header, my_fraction_row, label = "TG - Fraction of maze explored")
plt.plot(header, my_fraction_pionner, label = "TG - Fraction of maze explored until pionner")
plt.plot(header, my_v2_fraction_row, label = "TG (new) - Fraction of maze explored")
plt.plot(header, my_v2_fraction_pionner, label = "TG (new) - Fraction of maze explored until pionner") """


""" plt.plot(header, tarry_steps_row, label = "TARRY: Average")
plt.plot(header, tarry_stdev_row, label = "TARRY: STDEV")
plt.plot(header, tarry_steps_from_first_to_last_row, label = "TARRY: Average Steps From First to Last")
#plt.plot(header, tarry_fraction_row, label = "TARRY (matlab): Fraction of maze explored") """


plt.xlabel('No. of agents')
#plt.ylabel('No. of steps')
#plt.ylabel('Fraction of maze explored (%)')
plt.ylabel('Fraction of all 250 mazes (40x40) (%)')
plt.title('40x40 maze - 2 intervals policy - when does pioneer find the goal?')

plt.grid()
plt.legend()
plt.savefig('anomalous.pdf',format="pdf")
plt.show()