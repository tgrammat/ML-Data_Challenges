# helper functions to add (generate) calendar days in data set
import calendar
import graphlab as gl
import numpy as np

def add_running_year(month_sf, start_year):
    
    year_attrib = []
    
    for row_idx in range(len(month_sf)):
        running_month = month_sf[row_idx]
        
        if row_idx == 0:
            year = start_year
            year_attrib.append(year)
        
        if row_idx > 0:
            prev_running_month = month_sf[row_idx-1]
            
            if(running_month >= prev_running_month):
                year_attrib.append(year)
            else:
                year +=1
                year_attrib.append(year)
        
    year_sf = gl.SArray(year_attrib)
    
    return year_sf

def add_month_running_date(data, year_column_name, month_column_name, wkday_column_name):
    calendar.setfirstweekday(calendar.SUNDAY)

    year_sf = data[year_column_name].astype(int)
    month_sf = data[month_column_name].astype(int)
    wkday_sf = data[wkday_column_name].astype(int)
    monthcal_date_sf = []

    prev_running_date = 0

    for row_idx in range(len(data)):
        running_year = year_sf[row_idx]
        running_month = month_sf[row_idx]
        running_wkday = wkday_sf[row_idx]
        
        monthcal = calendar.monthcalendar(running_year, running_month)
        
        if(row_idx == 0):
            prev_running_year = running_year
            prev_running_month = running_month
            prev_running_wkday = running_wkday
            month_week = 0
        else:
            prev_running_year = year_sf[row_idx-1]
            prev_running_month = month_sf[row_idx-1]
            prev_running_wkday = wkday_sf[row_idx-1]
            if(running_wkday < prev_running_wkday):
                month_week += 1
    
        for week in range(month_week, len(monthcal)):
            date = monthcal[week][running_wkday]
            if(row_idx == 0):
                prev_running_date = date
            if((date is not 0) & (running_wkday < prev_running_wkday) & (date > prev_running_date)):
                running_date = date
                prev_running_date = date
                month_week = week
                monthcal_date_sf.append(running_date)
                break
            if((date is not 0) & (running_wkday == prev_running_wkday) & (date == prev_running_date)):
                running_date = date
                prev_running_date = date
                month_week = week
                monthcal_date_sf.append(running_date)
                break
            if((date is not 0) & (running_wkday > prev_running_wkday) & (date > prev_running_date)):
                running_date = date
                prev_running_date = date
                month_week = week
                monthcal_date_sf.append(running_date)
                break
        
    monthcal_date_sf = gl.SArray(monthcal_date_sf)
                       
    return monthcal_date_sf

def add_running_date(data, year_column_name, month_column_name, wkday_column_name):
    year_sf = data[year_column_name]
    month_sf = data[month_column_name]
    data_sf = []
    
    for row_idx in range(len(data)):
        running_year = year_sf[row_idx]
        running_month = month_sf[row_idx]
        
        if(row_idx == 0):
            monthdata = data.filter_by(running_year, year_column_name).filter_by(running_month, month_column_name)
            monthcal_date_sf = add_month_running_date(monthdata, year_column_name, month_column_name, wkday_column_name)
            data_sf.extend(monthcal_date_sf)
        else:
            prev_running_year = year_sf[row_idx-1]
            prev_running_month = month_sf[row_idx-1]
            if((running_year != prev_running_year) | (running_month != prev_running_month)):
                monthdata = data.filter_by(running_year, year_column_name).filter_by(running_month, month_column_name)
                monthcal_date_sf = add_month_running_date(monthdata, year_column_name, month_column_name, wkday_column_name)
                data_sf.extend(monthcal_date_sf)
        
    data_sf = gl.SArray(data_sf)
    
    return data_sf