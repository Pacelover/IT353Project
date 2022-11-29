# https://www.engineersedge.com/heat_transfer/thermal_energy_created_13777.htm
# https://www.engineeringtoolbox.com/air-properties-viscosity-conductivity-heat-capacity-d_1509.html
# https://en.wikipedia.org/wiki/Clothing_insulation


def required_clo(temp,windchill, meta_heat):
    #human skin surface area ~= 1.75 meters
    transfer_area = 1.75
        
    return (0.155 * temp * transfer_area)/meta_heat

    
def get_kelvin(temp,unit):
    assert(type(unit)==str)
    if unit=='F':
        return get_kelvin((temp-32)*(5.0/9.0),'C')
    elif unit=='C':
        return temp+273.15
    elif unit=='K':
        return temp
    else:
        raise Exception("\""+unit+"\" is not a valid temperature measurement unit.")
    
def get_clothing(temp,units,windchill,humidity):
    
    #heat measured in Watts 
    activity_to_metabolic_heat = {'resting':103, 'walking':201 ,'jogging':263 , 'sprinting':385}
    #at 100% humidity, thermal conductivity is amplified by 3% (e.g. 0% hum: 100% therm_cond; 100% hum: 103% therm_cond)
    humidity_amp = 0.03 * (humidity/100.0)
    #temp must be in Kelvin
    temp_in_kelvin = get_kelvin(temp, units)
    
    if temp<294.817:
        temp-=humidity_amp*temp
        for act in activity_to_metabolic_heat.keys():
        
        
    else:
        temp+=humidity_amp*temp
    
    
    
    
    
        
    
    clothing_to_clo = {}