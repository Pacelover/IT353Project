# https://www.engineersedge.com/heat_transfer/thermal_energy_created_13777.htm
# https://www.engineeringtoolbox.com/air-properties-viscosity-conductivity-heat-capacity-d_1509.html
# https://en.wikipedia.org/wiki/Clothing_insulation


def match_clothing(temp,windchill,humidity):
    #heat measured in Watts 
    #measures averaged across humanity
    activity_to_metabolic_heat = {'resting':103, 'walking':201 ,'jogging':263 , 'sprinting':385}
    thermal_conductivity_by_temp = {}
    #human skin surface area ~= 1.75 meters
    transfer_area = 1.75
    material_thickness = {'skin':0.001, }
    #at 100% humidity, thermal conductivity is amplified by 3% (e.g. 0% hum: 100% therm_cond; 100% hum: 103% therm_cond)
    humidity_amp = 0.03 * (humidity/100.0)
    
    
    
    #conductive_heat_transfer = (thermal_conductivity/material_thickness)* transfer_area * 1 (one hour)
    
    
