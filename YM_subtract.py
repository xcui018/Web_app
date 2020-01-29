# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#User defined function
#Year-month subtraction
def year_month_subtract_month (Ym,step):
    
    str_ym = str(Ym)
    year = str_ym[0:4]
    month = str_ym[4:]
    month_diff = int(month) - step
    if month_diff >0:
        final_year = year
        final_monthA = month_diff
        if final_monthA <10:
            final_month = '0'+str(final_monthA)
        else:
            final_month = str(final_monthA)

    elif month_diff==0:
        final_year = int(year)-1
        final_month = 12

    else:
        if abs(step)>=12:
            Y_subtractor = int(step/12)
            Remainder = step%12
            
            final_year = int(year)-Y_subtractor
            if step>Remainder:
                temp = int(month)-Remainder
                
                if temp ==0:
                    final_year = final_year-1
                    final_month = str(12)
                elif temp<0:
                    final_year = final_year-1
                    temp_final_month = 12-abs(temp)
                    if temp_final_month<10:
                        final_month = '0'+str(temp_final_month)
                    else:
                        final_month = str(temp_final_month)
                else:
                    temp_final_month = temp
                    if temp_final_month <10:
                        final_month = '0'+str(temp_final_month)
                    else:
                        final_month = str(temp_final_month)

        else:
            final_year = int(year)-1
            temp_final_month = 12-abs(month_diff)
            if temp_final_month <10:
                final_month = '0'+str(temp_final_month)
            else:
                final_month = temp_final_month
            
    output =str(final_year)+str(final_month)
    return output
        #print('Something is wrong. It appears you did not subtract by 1 month')
        
def color_negative_red(val):
    """Takes a scalar and returns a strnig with the css property 'color:red' for negative strings, black otherwise."""

    color = 'red' if val<0 else 'black' 
    return 'color: %s' % color

def color_threshold_red(val,p):
    """Takes a scalar and returns a strnig with the css property 'color:red' for negative strings, black otherwise."""

    color = 'red' if abs(val)>=p else 'black' 
    return 'color: %s' % color