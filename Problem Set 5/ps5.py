# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

import warnings
warnings.simplefilter('ignore', pylab.RankWarning)

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # Initialize a models list that will store the different model arrays
    models = []
    
    # For every degree, create a polyfit model and append it to the models list
    for deg in degs:
        model = pylab.polyfit(x, y, deg)
        models.append(pylab.array(model))
        
    # Return the list of the model arrays
    return models
        

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # Calculate the numerator and the denominator of the second term of the r_squared equation
    num = ((y - estimated)**2).sum()
    denom = ((y - y.mean())**2).sum()
    
    # Calculate and return the r_squared
    r_squared = 1 - num / denom
    return r_squared
    
    
def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # Flag for coming through the first time
    first_time_through = True
    
    # For every model
    for model in models:
        
        # Create the fitted curve for the model
        esty = pylab.polyval(model,x)
        
        # Calculate the r_squared of the model
        r_sq = r_squared(y, esty)
        
        # Plot the curve with the respective model regression
        pylab.figure()
        pylab.plot(x, y, 'bo',
                   label = 'Measured data')
        
        # have a differente title when the model is a linear regression/first model:
        if first_time_through:
            se_slope = se_over_slope(x, y, esty, model)
            pylab.title('Measured Temperatures with a regression fit of degree '+str(len(model)-1)+',\n' \
                        + 'r squared = '+str(round(r_sq, 4)) + ',\n' \
                        + 'se over slope = '+ str(round(se_slope, 4)) )
            first_time_through = False
        else:
            pylab.title('Measured Temperatures with a regression fit of degree '+str(len(model)-1)+',\n' \
                        + 'r squared = '+str(round(r_sq, 4)) )

        # Label the axes and plot the regression
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (Degrees Celsius)')
        pylab.plot(x, esty, 'r',
                   label = 'Fit of degree ' +str(len(model)-1)+', r_sq = '
                   + str(round(r_sq, 4)))
        pylab.legend(loc = 'best')

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # Instantiate a year list to append the average yearly temperatures of the cities 
    yearly_avg_tmp = []
    
    # For every year
    for year in years:
        
        # Create an empty list tmp_list that will store all the recorded temperatures in the
        # data sample we want to look into
        tmp_list = []
        
        # For every  city, grab all of the city's temperature measurements and 
        # append them into the tmp_list
        for city in multi_cities:
            all_temps = climate.get_yearly_temp(city, year)
            for i in all_temps:
                tmp_list.append(i)
        
        # Average the tmp_list and append it to the yearly_avg_tmp list
        avg = sum(tmp_list) / len(tmp_list)
        yearly_avg_tmp.append(avg)
    
    # Convert the yearly_avg_tmp list to an array and return it
    temps = pylab.array(yearly_avg_tmp)
    return temps
        

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # Create an empty list to append the results of the moving averages
    moving_average = []
    
    # For the range from 0 until the window_length - 1
    for i in range(window_length-1):
        
        # Calculate the moving average and append it to the moving_average list
        # Create an empty list to sum all of the elements from 0 until i
        sum_ = 0
        for j in range(i+1):
            sum_ += y[j]
            
        # Calculate the average and append it
        avg = sum_ / (i+1)
        moving_average.append(avg)
        
    # For the range from window_length - 1 until the end of the range of the y dataset,
    # calculate the moving averages and append them to the moving_average list
    for i in range(window_length - 1, len(y)):
        sum_ = 0
        for j in range(i-window_length+1, i+1):
            sum_ += y[j]
        avg = sum_ / window_length
        moving_average.append(avg)
    
    # Convert the moving averages list to an array and return it
    moving_average = pylab.array(moving_average)
    return moving_average

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # Calculate the sum of the square of the differences
    sq_diffs_sum = ((y - estimated)**2).sum()
    
    # Calculate the rmse
    rmse = pylab.sqrt(sq_diffs_sum / len(y))
    
    # Return the rmse
    return rmse

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # Instantiate a year list to append the average yearly std devs of the temps for the cities
    yearly_stddev_tmp = []
    
    # For every year
    for year in years:
        
        # Create an empty list avg_daily_list that will store all the avg daily temperatures in the
        # year, for the data sample we want to look into
        avg_daily_list = []
        
        # For every day, calculate the average temperature accross all the cities and append it to
        # the avg_daily_list list
        days = 31
        months = 12
        for month in range(1, months+1):
            for day in range(1, days+1):
                
                # Create an empty day_list list to append the values of the temperatures in one day
                # across all cities
                day_list = []
                
                # For every  city, grab all of the city's temperature measurements and 
                # append them into the tmp_list
                for city in multi_cities:
                    if day not in climate.rawdata[city][year][month]:
                        continue
                    day_list.append(climate.get_daily_temp(city, month, day, year))
                
                if len(day_list) == 0:
                    continue
                
                # Calculate the average of the day_list and append it to avg_daily_list
                avg = sum(day_list) / len(day_list)
                avg_daily_list.append(avg)
        
        # Get the standard deviation of the avg_daily_list and append it to the yearly_stddev_temp list
        avg_daily_list = pylab.array(avg_daily_list)
        stddev = pylab.sqrt(((avg_daily_list - avg_daily_list.mean())**2).sum() / len(avg_daily_list))
        yearly_stddev_tmp.append(stddev)
    
    # Convert the yearly_stddev_tmp list to an array and return it
    temps = pylab.array(yearly_stddev_tmp)
    return temps

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # For every model
    for model in models:
        
        # Create the fitted curve for the model
        esty = pylab.polyval(model,x)
        
        # Calculate the rmse of the model
        RMSE = rmse(y, esty)
        
        # Plot the curve with the respective model regression
        pylab.figure()
        pylab.plot(x, y, 'bo',
                   label = 'Measured data')
        
        pylab.title('Measured Temperatures with a regression fit of degree '+str(len(model)-1)+',\n' \
                        + 'with an RMSE of '+str(round(RMSE, 4)) )

        # Label the axes and plot the regression
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (Degrees Celsius)')
        pylab.plot(x, esty, 'r',
                   label = 'Fit of degree ' +str(len(model)-1)+', RMSE = '
                   + str(round(RMSE, 4)))
        pylab.legend(loc = 'best')

if __name__ == '__main__':
    
    # Load the file into the climate class
    filename = 'data.csv'
    climate = Climate(filename)    

#    # Part A.4.1
#    # Generate data samples from 1961 to 2009 in the training_interval
#    x = pylab.array(TRAINING_INTERVAL)
#    
#    # Fill up a list of the temperatures for each year in the training interval
#    # and in NYC and convert it to an array
#    y = []
#    for year in TRAINING_INTERVAL:
#        y.append(climate.get_daily_temp('NEW YORK', 10, 1, year))
#    y = pylab.array(y)
#    
#    # Compute the models for the degrees required    
#    degs = [1]
#    models = generate_models(x, y, degs)
#    
#    # Plot the measured points and the regression curve
#    evaluate_models_on_training(x, y, models)
    
#    # Part A.4.2
#    # Generate data samples from 1961 to 2009 in the training_interval
#    x = pylab.array(TRAINING_INTERVAL)
#    
#    # Fill up a list of the temperatures for the average temperature of each year 
#    # in the training interval and in NYC and convert it to an array
#    y = []
#    for year in TRAINING_INTERVAL:
#        tmp_array = climate.get_yearly_temp('NEW YORK', year)
#        avg = tmp_array.sum() / len(tmp_array)  
#        y.append(avg)
#    y = pylab.array(y)
#    
#    # Compute the models for the degrees required    
#    degs = [1]
#    models = generate_models(x, y, degs)
#    
#    # Plot the measured points and the regression curve
#    evaluate_models_on_training(x, y, models)
    
#    # Part B
#    # Generate data samples from 1961 to 2009 in the training_interval
#    x = pylab.array(TRAINING_INTERVAL)
#    
#    # Fill up a list of the temperatures for the average temperature of each year 
#    # in the training interval and in all the cities and convert it to an array
#    multi_cities = CITIES
#    y = gen_cities_avg(climate, multi_cities, TRAINING_INTERVAL)
#    
#    # Compute the models for the degrees required    
#    degs = [1]
#    models = generate_models(x, y, degs)
#    
#    # Plot the measured points and the regression curve
#    evaluate_models_on_training(x, y, models)
    
#    # Part C
#    # Generate data samples from 1961 to 2009 in the training_interval
#    x = pylab.array(TRAINING_INTERVAL)
#    
#    # Fill up a list of the temperatures for the average temperature of each year 
#    # in the training interval and in all the cities and convert it to an array
#    multi_cities = CITIES
#    y = gen_cities_avg(climate, multi_cities, TRAINING_INTERVAL)
#    window_length = 5
#    moving_avg_y = moving_average(y, window_length)
#    
#    # Compute the models for the degrees required    
#    degs = [1, 2]
#    models = generate_models(x, moving_avg_y, degs)
#    
#    # Plot the measured points and the regression curve
#    evaluate_models_on_training(x, moving_avg_y, models)

#    # Part D.2
#    # Generate data samples from 1961 to 2009 in the training_interval
#    x = pylab.array(TRAINING_INTERVAL)
#    
#    # Fill up a list of the temperatures for the average temperature of each year 
#    # in the training interval and in all the cities and convert it to an array; get the 
#    # moving average of the array with a window length of 5 years
#    multi_cities = CITIES
#    y = gen_cities_avg(climate, multi_cities, TRAINING_INTERVAL)
#    window_length = 5
#    moving_avg_y = moving_average(y, window_length)
#    
#    # Compute the models for the degrees required; in this case: 1, 2, 20    
#    degs = [1, 2, 20]
#    models = generate_models(x, moving_avg_y, degs)
#    
#    # Plot the measured points and the regression curves
#    evaluate_models_on_training(x, moving_avg_y, models)
#    
#    # Create the test data samples with the 5-year moving averages for the years 2010-2015
#    test_samples = gen_cities_avg(climate, multi_cities, TESTING_INTERVAL)
#    test_samples_moving_avgs = moving_average(test_samples, window_length)
#    
#    # Graph the predicted and real observations for the testing interval
#    x = pylab.array(TESTING_INTERVAL)
#    evaluate_models_on_testing(x, test_samples_moving_avgs, models)

    # Part E
    # Generate data samples from 1961 to 2009 in the training_interval
    x = pylab.array(TRAINING_INTERVAL)
    
    # Fill up a list of the std devs of the temperatures for each year 
    # in the training interval and in all the cities and convert it to an array; get the 
    # moving average of the array with a window length of 5 years
    multi_cities = CITIES
    y = gen_std_devs(climate, multi_cities, x)
    window_length = 5
    moving_stddev_y = moving_average(y, window_length)
    
    # Compute the models for the degrees required; in this case: 1    
    degs = [1]
    models = generate_models(x, moving_stddev_y, degs)
    
    # Plot the measured points and the regression curves
    evaluate_models_on_training(x, moving_stddev_y, models)
    
