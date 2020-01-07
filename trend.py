from datetime import datetime, date, time, timedelta
import requests


def convert_time(date_string):
	date_format = "%Y%m%d%H%M%S"
	formatted_date = datetime.strptime(date_string, date_format)
	return formatted_date

def rest_call_bi_data(station_name, interval, start_date, end_date):
	dates = calculate_new_date(start_date, end_date, interval)
	i = 0
	while i < len(dates):
		if i == len(dates)-1:
			break
		base_url = "http://secondary.mesonet.k-state.edu/rest/wimsstationdata?stn=%s&int=%s&t_start=%s&t_end=%s" % (station_name, interval, dates[i], dates[i+1])
		i+=1
		res = requests.get(base_url)
		returned_data = (res.text)

		f = open("./%s_%s_data.txt" % (station_name, interval), "w")
		f.write(returned_data)
		
		data_dict = {}

		for line in returned_data.splitlines()[1:-2]:
			bi_value = (line.split(",")[12])
			date_time = line.split(",")[0]
			day = date_time.split("-")[-1][:2]
			month = date_time.split("-")[1]
			key_value = month + " - " + day
			
			if key_value in data_dict:
				data_dict[key_value].append(bi_value)
			else:
				data_dict[key_value] = [bi_value]
		
		return data_dict	

		
		f.close()

def calculate_max_bi(bi_value_dict, day_key):
	bi_max_dict = {}
	for key in bi_value_dict:
		bi_arr = bi_value_dict[key]
		for bi in bi_arr:
			if bi == "M":
				bi_arr.remove(bi)
		bi_max_dict[key] = max(bi_arr)
	return bi_max_dict[day_key]

def get_3day_trend():

	keys_arr = []
	
	today = datetime.today()
		
	yesterday = today - timedelta(days=1)
	yesterday_key = yesterday.strftime('%m - %d')

	yesterday_1day = yesterday - timedelta(days=1)
	yesterday_1day_key = yesterday_1day.strftime('%m - %d')

	yesterday_2day = yesterday_1day - timedelta(days=1)
	yesterday_2day_key = yesterday_2day.strftime('%m - %d')
	
	keys_arr.append(yesterday_key)
	keys_arr.append(yesterday_1day_key)
	keys_arr.append(yesterday_2day_key)

	return ["09 - 29", "09 - 28", "09 - 27"]
		


def calculate_break_time(time_interval):	
	if(time_interval=="5min"):
		break_time = 900000
	elif(time_interval=="hour"):
		break_time = 3000 * 60 * 60
	elif(time_interval=="day"):
		break_time= 864000 * 300
	return break_time

def calculate_seconds_elapsed(start_date, end_date):
	converted_start_date = convert_time(start_date)
	converted_end_date = convert_time(end_date)
	diff_time = converted_end_date - converted_start_date
	diff_seconds = diff_time.total_seconds()
	return diff_seconds

def parse_datetime(datetime_obj):
	year = datetime_obj.year
	month = datetime_obj.month
	day = datetime_obj.day
	hour = datetime_obj.hour
	minute = datetime_obj.minute
	second = datetime_obj.second
	parsed_date = "%s%02d%02d%02d%02d%02d" % (year, month, day, hour, minute, second)
	return parsed_date	

def calculate_new_date(start_date, end_date, time_interval):
	converted_start_date = convert_time(start_date)
	converted_end_date = convert_time(end_date)
	seconds_elapsed= calculate_break_time(time_interval)	
	formatted_start_dates = []
	while(converted_start_date <= convert_time(end_date)):
		formatted_start_dates.append(parse_datetime(converted_start_date))
		converted_start_date = converted_start_date + timedelta(seconds=seconds_elapsed)
		if converted_start_date>=convert_time(end_date):
			break
	formatted_start_dates.append(parse_datetime(converted_end_date))
	return formatted_start_dates



bi_value = rest_call_bi_data("Manhattan","day","20190319000000", "20191001000000")
bi_keys = get_3day_trend()
for keys in bi_keys:
	print(keys)
	bi_max = calculate_max_bi(bi_value, keys)
	print(bi_max)




