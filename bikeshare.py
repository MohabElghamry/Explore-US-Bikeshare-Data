import calendar
import datetime
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 500)
import os
import sys

cities = ['chicago', 'new york city', 'washington']

# list with months name from january to june
months = [calendar.month_name[x+1].lower() for x in range(6)]
months.append('all')

# list with days of the week
days = [calendar.day_name[x].lower() for x in range(7)]
days.append('all')

def get_filters(variable, list):
    '''
    this function asks the user for his input whether city, month, or day
    takes two variable which is the type of filter
    the list we are checking against

    Returns
    print a statements to state what we are analyzing
    the filter the user want to implement '''

    user_input = input('\nPlease choose a {} to analyze from {}..'.format(variable, list))
    while True:
        if user_input.lower().strip() not in list:
            print('\n{} is not a viable {}'.format(user_input, variable))
            user_input = input('Please choose a viable {} to analyze ({})..'.format(variable, list))
        else:
            break
    print('\nAnalyzing the data of {}..'.format(user_input.title()))
    return user_input

#Running the function to get the city filter
city_filter = get_filters('city', cities)

#reading the csv file as pandas dataframe
data = pd.read_csv(city_filter.strip().replace(' ', '_').lower() + '.csv')

#Running the function to get the months and day filter
months_filter = get_filters('month', months)
day_filter = get_filters('day', days)

#producing 3 new columns for months, day, hour, and trip
data['Start Time'] = pd.to_datetime(data['Start Time'])
data['month'] = data['Start Time'].dt.strftime("%B")
data['day'] = data['Start Time'].dt.strftime("%A")
data['Hour'] = data['Start Time'].dt.strftime("%H")
data['Trip'] = data['Start Station'] + ' to ' + data['End Station']


#filtering the data based on the user's choices
if months_filter.lower() != 'all':
    data = data[data['month'] == months_filter.title()]
if day_filter.lower() != 'all':
    data = data[data['day'] == day_filter.title()]

#if user wants to see raw data
def raw_data():
    '''prompt the user if they want to see 5 lines of raw data'''
    i = 0
    while True:
        raw_data = input("Do you want to see 5 rows of the raw data? \nType yes if you do or no if you don't\n")
        if raw_data.lower() == 'yes':
            print(data[i: i+5])
            i +=5
        elif raw_data.lower() == 'no':
            break
        else:
            print('\n{} is invalid option. Please enter a viable option\n'.format(raw_data))

def popular_times_of_travel():
    """Displays statistics on the most frequent times of travel."""

    if months_filter.lower() != 'all':
        statement1 = '\nYou are currently viewing the month of {}, \nTo view the statistics of most common month please filter for all\n'.format(months_filter.title())
    else:
        most_common_month = data['month'].mode().values[0]
        statement1 = '\n{} is the most common month.'.format(most_common_month)

    if day_filter.lower() != 'all':
        statement2 = '\n\nYou are currently viewing {} statistics,\nTo view the statistics of most common day please filter for all\n'.format(day_filter.title())
    else:
        most_common_day = data['day'].mode().values[0]
        statement2 = '\n{} is the most common day.'.format(most_common_day)

    most_common_hour = data['Hour'].mode().values[0]
    statement3 = '\n{}:00 is the most common hour.'.format(most_common_hour)

    print('\nCalculating The Most Popular Times of Travel based on your filters...\n', statement1, statement2, statement3, '\n' +'-'*40)


def popular_stations_and_trip():
    '''Displays statistics on the most popular stations and trip.'''
    most_common_start = data['Start Station'].mode().values[0]
    statement1 = '\n{} is the most common start station.'.format(most_common_start)

    most_common_end =  data['End Station'].mode().values[0]
    statement2 = '\n{} is the most common end station.'.format(most_common_end)

    most_common_Trip =  data['Trip'].mode().values[0]
    statement3 = '\n{} is the most common trip.'.format(most_common_Trip)

    print('\nCalculating The Most Popular Stations and Trip based on your filters...\n', statement1, statement2, statement3, '\n' +'-'*40)

def trip_duration():
    """Displays statistics on the total and average trip duration."""

    total_travel_time = round(data['Trip Duration'].sum(), 2)
    statement1 = '\n{} seconds is the total travel time.'.format(total_travel_time)

    average_travel_time = round(data['Trip Duration'].mean(), 2)
    statement2 = '\n{} seconds is the average travel time.'.format(average_travel_time)

    print('\nCalculating Trip Durations based on your filters...\n', statement1, statement2, '\n' +'-'*40)

def user_stats():
    """Displays statistics on bikeshare users."""

    user_type = data.groupby(['User Type'])['User Type'].count()
    statement1 = '\nBreak down of user types\n {}\n'.format(user_type)

    if city_filter.lower() != 'washington':
        user_gender = data.groupby(['Gender'])['Gender'].count()
        statement2 = '\nBreak down of user genders\n {}\n'.format(user_gender)
        statement3 = '\nthe earliest year of birth is {}\nthe most recent year of birth is {}\nthe most common year of birth is {}'.format(int(data['Birth Year'].min()), int(data['Birth Year'].max()), int(data['Birth Year'].mode().values[0]))
    else:
        statement2 = '\nInformation about gender is not available'
        statement3 = '\nInformation about birth year is not available'

    print('\nCalculating user stats based on your filters...\n', statement1, statement2, statement3, '\n' +'-'*40)

def restart():
    while True:
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'yes':
            os.system('python bikeshare.py')
            exit()
        elif restart.lower() == 'no':
            sys.exit()
        else:
            print('\n{} is invalid option. Please enter a viable option\n'.format(restart))

def main():
    while True:
        raw_data()
        popular_times_of_travel()
        popular_stations_and_trip()
        trip_duration()
        user_stats()
        restart()





if __name__ == "__main__":
	main()
