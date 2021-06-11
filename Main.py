import numpy as np
import pandas as pd

def create_events(enmo, threshold, percent):
	i = 0
	store = []
	while i < len(enmo):
		j = 0
		if enmo[i] >= threshold:
			arr = enmo[i]
			while np.mean(arr) >= (percent * threshold):
				j = j + 1

				if (i + j) > len(enmo):
					store.append([i, j - 1])
					return store

				arr = enmo[i:(i + j)]
			store.append([i, j - 1])
			i = i + j
		else:
			i = i + 1
	return store

class Event:

	def __init__(self, start, length, acc, ts, day_no):
		self.start_loc = start
		self.end_loc = start + length
		self.duration = length
		self.volume = np.sum(acc)
		self.sd = np.std(acc)
		self.intensity = self.volume / self.duration
		self.median = np.median(acc)
		self.fifth_percent = np.percentile(acc, 5)
		self.ninety_fifth_percent = np.percentile(acc, 95)
		self.date = ts.split(' ')[0]
		self.time = ts.split(' ')[1]
		self.day_no = day_no + 1

	def return_all(self):
		return np.array([self.start_loc, self.end_loc,
		                 self.duration, self.volume, self.sd, self.intensity, self.median,
		                 self.fifth_percent, self.ninety_fifth_percent,
		                 self.date, self.time, self.day_no])


loc = 'C:\\Users\\x\\Data'

def func(file_loc):
	file = pd.read_table(file_loc, compression = 'gzip')

	times = file['timestamp'].values
	ENMO = file['ENMO_mg'].values

	# Compute day number here in case days are missing events
	day_no = pd.factorize(file['timestamp'].astype(str).str[:10])[0]

	threshold_values = np.minimum(ENMO, 40)
	# Identify event locations
	events = create_events(threshold_values, 40, 0.80)
	long_events = [e for e in events if e[1]>9]

	# create Events
	event_list = [Event(x[0], x[1], ENMO[x[0]:x[0]+x[1]], times[x[0]], day_no[x[0]]) for x in long_events]
	tab = [e.return_all() for e in event_list]

	cols = ['Start', 'End', 'Dur', 'Vol', 'SD', 'Int', 'Med', '5th', '95th', 'Date', 'Time', 'Day_No']
	table = pd.DataFrame(tab, columns = cols)
	table['Day_Name'] = [pd.to_datetime(str(x)).day_name() for x in table['Date'].values]

	# table.to_csv()
	return table
