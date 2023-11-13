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

rows = []
with open("my_1to80agents_250iterations_20x20.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

my_steps_row = rows[1]
my_pionner_steps_row = rows[2]
my_fraction_row = rows[3]
my_stdev_row = rows[4]
my_fraction_pionner = rows[5]

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
with open("my_1to40agents_250iterations_40x40_v2_anomaly_2.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

anomaly_steps_row = rows[1]
anomaly_pionner_steps_row = rows[2]
anomaly_fraction_row = rows[3]
anomaly_stdev_row = rows[4]
anomaly_fraction_pionner = rows[5]

anomaly_firstSearch = rows[6]
anomaly_firstInterval = rows[7]
anomaly_backtracking = rows[8]
anomaly_secondSearch = rows[9]
anomaly_secondInterval = rows[10]
anomaly_residue = rows[11]

anomaly_firstSearch_pioneer = rows[12]
anomaly_firstInterval_pioneer = rows[13]
anomaly_backtracking_pioneer = rows[14]
anomaly_secondSearch_pioneer = rows[15]
anomaly_secondInterval_pioneer = rows[16]
anomaly_residue_pioneer = rows[17]

""" plt.plot(header, anomaly_firstSearch, label = "First Search")
plt.plot(header, anomaly_firstInterval, label = "First Interval") """
plt.plot(header, anomaly_backtracking, label = "Backtracking")
""" plt.plot(header, anomaly_secondSearch, label = "Second Search")
plt.plot(header, anomaly_secondInterval, label = "Second Interval")
plt.plot(header, anomaly_residue, label = "DFS") """

""" plt.plot(header, anomaly_firstSearch_pioneer, label = "Pioneer: First Search")
plt.plot(header, anomaly_firstInterval_pioneer, label = "Pioneer: First Interval")
plt.plot(header, anomaly_backtracking_pioneer, label = "Pioneer: Backtracking")
plt.plot(header, anomaly_secondSearch_pioneer, label = "Pioneer: Second Search")
plt.plot(header, anomaly_secondInterval_pioneer, label = "Pioneer: Second Interval")
plt.plot(header, anomaly_residue_pioneer, label = "Pioneer: DFS") """


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
plt.ylabel('No. of steps')
#plt.ylabel('Fraction of maze explored')
plt.title('Anomaly - All agents - 40x40 maze')

plt.grid()
plt.legend()
plt.savefig('anomaly_allagents_40x40_backtracking.pdf', format="pdf")
plt.show()