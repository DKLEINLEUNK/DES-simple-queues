# DES-simple-queues

Project by:

- David - 12992976
- Holly - 15055108
- Nina  - 12896934


## TO-DO

### Code-related

- [ ] Utilizing different distributions (currently: exponential).
- [ ] Incorporate system loads.
- [ ] Analyzing simulation data.
- [ ] Plotting simulation data.
- [ ] Add doc-strings.
- [ ] ...
- [x] Extending to n > 1 servers.
- [x] Exporting relevant simulation data.

### Project-related

- [ ] Add introduction section.
- [ ] Consider CLI interface.
- [ ] Consider Jupyter Notebook interface.
- [ ] Specify code requirements.
- [ ] ...


## Project Structure

```
├── examples/               # Example code for SimPy
│   ├── example_queue.py
│   └── example_simpy.py
│
├── main.py                 # Orchastrates simulation
├── Queue.py                # DES class
│
└── README.md               # Overview of project
```


## Example Output

```
Running queueing system simulation...
[ 0.0000s] ID 1: Arrived (waited  0.000s)
[ 1.1457s] ID 2: Arrived (waited  0.000s)
[ 3.8181s] ID 1: Finished.
[ 3.8181s] ID 3: Arrived (waited  1.749s)
[ 4.2015s] ID 3: Finished.
[ 4.2015s] ID 4: Arrived (waited  1.380s)
[12.8656s] ID 4: Finished.
[12.8656s] ID 5: Arrived (waited  9.842s)
[22.1201s] ID 2: Finished.
[22.1201s] ID 6: Arrived (waited 18.395s)
[25.3431s] ID 5: Finished.
[25.3431s] ID 7: Arrived (waited 19.379s)
[29.7051s] ID 6: Finished.
[29.7051s] ID 8: Arrived (waited 23.316s)
[33.5127s] ID 7: Finished.
[33.5127s] ID 9: Arrived (waited 26.515s)
[33.5942s] ID 8: Finished.
[33.5942s] ID 10: Arrived (waited 26.558s)
[42.0918s] ID 10: Finished.
[42.0918s] ID 11: Arrived (waited 33.308s)
[43.5158s] ID 11: Finished.
[43.5158s] ID 12: Arrived (waited 34.367s)
[43.7037s] ID 12: Finished.
[43.7037s] ID 13: Arrived (waited 33.876s)
[46.2328s] ID 9: Finished.
[46.2328s] ID 14: Arrived (waited 32.129s)
[47.9059s] ID 14: Finished.
[47.9059s] ID 15: Arrived (waited 33.200s)
[50.4893s] ID 13: Finished.
[50.4893s] ID 16: Arrived (waited 35.045s)
[54.7224s] ID 16: Finished.
[54.7224s] ID 17: Arrived (waited 38.492s)
[54.8483s] ID 15: Finished.
[54.8483s] ID 18: Arrived (waited 38.430s)
[57.3752s] ID 17: Finished.
[57.3752s] ID 19: Arrived (waited 40.795s)
[63.2804s] ID 19: Finished.
[63.2804s] ID 20: Arrived (waited 45.680s)
[66.9018s] ID 18: Finished.
[66.9018s] ID 21: Arrived (waited 49.134s)
[75.4779s] ID 20: Finished.
[75.4779s] ID 22: Arrived (waited 56.196s)
[77.2659s] ID 22: Finished.
[77.2659s] ID 23: Arrived (waited 56.640s)
[83.8125s] ID 21: Finished.
[83.8125s] ID 24: Arrived (waited 61.628s)
[84.8492s] ID 24: Finished.
[84.8492s] ID 25: Arrived (waited 62.415s)
[90.0508s] ID 25: Finished.
[90.0508s] ID 26: Arrived (waited 66.711s)
[95.4569s] ID 26: Finished.
[95.4569s] ID 27: Arrived (waited 71.973s)
[96.3144s] ID 27: Finished.
[96.3144s] ID 28: Arrived (waited 71.639s)
[98.3117s] ID 23: Finished.
[98.3117s] ID 29: Arrived (waited 73.050s)
```