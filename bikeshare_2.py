import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
days = ['All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print()
    print('-'*40)
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('\nWhich city do you want to analyze?')
    while True:
        city = input('Please select from (Chicago, New York City, Washington)\n')
        city = city.lower()
        if city not in CITY_DATA:
            print('WRONG INPUT!!\n')
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    print('\nWhich month do you want to filter by?')
    while True:
        month = input('Please select from (January, February, March, April, May, June) or input "all" to apply no month filter\n')
        month = month.title()
        if month not in months:
            print('WRONG INPUT!!\n')
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nWhich day of week do you want to filter by?')
    while True:
        day = input('Please select from (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) or input "all" to apply no day filter\n')
        day = day.title()
        if day not in days:
            print('WRONG INPUT!!\n')
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'All':
        df = df[df['month'] == month]
    if day != 'All':
        df = df[df['day_of_week']  == day]
    
    
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'All':
        print('The most common month is ({})'.format(df['month'].value_counts().index[0]), 'with ({:.0f}%) of months'.format(df['month'].value_counts().values[0]/df.shape[0] * 100))

    # TO DO: display the most common day of week
    if day == 'All':
        print('The most common day of week is ({})'.format(df['day_of_week'].value_counts().index[0]), 'with ({:.0f}%) of the days'.format(df['day_of_week'].value_counts()[0]/df.shape[0] * 100))

    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.strftime('%I %p')
    print('The most common start hour is ({})'.format(df['start_hour'].value_counts().index[0]), 'with ({:.0f}%) of the day hours'.format(df['start_hour'].value_counts().values[0]/df.shape[0] * 100))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station is ({})'.format(df['Start Station'].value_counts().index[0]), 'with ({:.0f}%) of start stations'.format(df['Start Station'].value_counts().values[0]/df.shape[0] * 100))

    # TO DO: display most commonly used end station
    print('The most commonly used end station is ({})'.format(df['End Station'].value_counts().index[0]), 'with ({:.0f}%) of end stations'.format(df['End Station'].value_counts().values[0]/df.shape[0] * 100))

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end station'] = df['Start Station'].add(' to ' + df['End Station'])
    print('The most frequent trip is ({})'.format(df['start_end station'].value_counts().index[0]), 'with ({:.3f}%) of trips'.format(df['start_end station'].value_counts().values[0]/df.shape[0] * 100))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time:', df['Trip Duration'].sum(), 'sec')

    # TO DO: display mean travel time
    print('Average travel time:', df['Trip Duration'].mean(), 'sec')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User types:')
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if city != 'washington':
        print('\nGender:')
        print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print('\nEarliest year of birth:', int(df['Birth Year'].min()))
        print('Most recent year of birth:', int(df['Birth Year'].max()))
        print('Most common year of birth:', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        df = df.drop(columns=['month', 'day_of_week', 'start_hour', 'start_end station'])
        print('would you like to see a 5 lines of raw data?')
        df = df.reset_index(drop = True)
        answer = input()
        if answer.lower() == 'yes':
            row = 4
            while (row - 4) <= df.shape[0]:
                print(df.loc[row - 4: row])
                row += 5
                print('would you like to see another 5 lines of raw data?')
                answer = input()
                if answer.lower() != 'yes':
                    break
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
