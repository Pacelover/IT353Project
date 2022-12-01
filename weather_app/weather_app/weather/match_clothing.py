# https://www.engineeringtoolbox.com/air-properties-viscosity-conductivity-heat-capacity-d_1509.html
thrm_cond = {-190+273.15:7.82,	
    -150+273.15:11.69,
    -100+273.15:16.20,
    -75+273.15:18.34,
    -50+273.15:20.41,
    -25+273.15:22.41,
    -15+273.15:23.20,
    -10+273.15:23.59,
    -5+273.15:23.97,
    0+273.15:24.36,
    5+273.15:24.74,
    10+273.15:25.12,
    15+273.15:25.50,
    20+273.15:25.87,
    25+273.15:26.24,
    30+273.15:26.62,
    40+273.15:27.35,
    50+273.15:28.08,
    60+273.15:28.80,
    80+273.15:30.23,	
    100+273.15:31.62,	
    125+273.15:33.33,	
    150+273.15:35.00,	
    175+273.15:36.64,	
    200+273.15:38.25,	
    225+273.15:39.83,	
    300+273.15:44.41,	
    412+273.15:50.92,	
    500+273.15:55.79,	
    600+273.15:61.14,
    700+273.15:66.32,	
    800+273.15:71.35,	
    900+273.15:76.26,	
    1000+273.15:81.08,	
    1100+273.15:85.83}

def required_clo(temp, meta_heat):
    #human skin surface area ~= 1.75 meters        
    return abs((temp-304.15)/(-0.190*meta_heat))

def get_survive_time(temp):
    healthK = 310.15 # == 98.6 degrees F
    if temp-healthK==0:
        return 28800
    elif temp<healthK:
        return 28800
    
    
    healthC = 35.2 #degrees C == 95.35 degrees F -- avg whole body temp (98.6 is core temp)
    vol = 0.5833 #assumed volume of a human in meters cubed
    shc = 4.186 #specific heat capacity of water
    
    #https://physics.stackexchange.com/questions/248202/calculating-the-time-for-two-bodies-to-reach-thermodynamic-equilibrium#:~:text=In%20a%20nutshell%3A%20it%20takes,body%20temperature%2C%20an%20exactness%20of%20.
    cap = (shc*(0.7*(vol*1000))*healthC) # num of joules energy capacity of human body assuming an average 70% water weight and volume proportional to average human surface area (assume a spherical man)
    
    
    hflx = 0
    for tmp in thrm_cond.keys():
        if temp<=float(tmp):
            hflx = thrm_cond.get(tmp)*(temp-273.15)
            break
    htc = hflx/(abs(temp-healthK))
    
    dt = 0
    t = 0
    cur = healthK
    while(True):        
        dt = ((htc*1.75)/cap)*(temp-cur)
        cur+=dt
        t+=1
        if cur>=315.15 or t>=28800:
            break
        
    
    return t
    
    
    
    
    
    
    
def get_kelvin(temp,unit):
    assert(type(unit)==str)
    if unit=='F':
        return get_kelvin(round((temp-32)*(5.0/9.0),2),'C')
    elif unit=='C':
        return temp+273.15
    elif unit=='K':
        return temp
    else:
        raise Exception("\""+unit+"\" is not a valid temperature measurement unit.")
    
def get_clothing(temp,units,windchill,humidity):
    # https://www.engineersedge.com/heat_transfer/thermal_energy_created_13777.htm
    #heat measured in Watts 
    activity_to_metabolic_heat = {'resting':70, 'walking':115 ,'jogging':150 , 'sprinting':220}
    #at 100% humidity, thermal conductivity is amplified by 3% (e.g. 0% hum: 100% therm_cond; 100% hum: 103% therm_cond)
    humidity_amp = 0.03 * (humidity/100.0)
    #temp must be in Kelvin
    temp_in_kelvin = get_kelvin(temp, units)
    
    # https://en.wikipedia.org/wiki/Clothing_insulation
    clothing_to_clo = {0:"naked",
                       1:"normal",
                       2:"light",
                       2.5:"medium",
                       3:"heavy",
                       4:"pro"
                       }
    
    if temp_in_kelvin<294.817:
        if windchill<temp:
            temp_in_kelvin=get_kelvin(windchill, units)
            
        temp_in_kelvin-=temp_in_kelvin*humidity_amp
        
        req = []
        
        for act in activity_to_metabolic_heat.keys():
            clo = required_clo(temp_in_kelvin, activity_to_metabolic_heat.get(act))
            # print(clo)
            for clt in clothing_to_clo.keys():
                if clo<=float(clt) or (clo>4 and clo<=4.2 and clothing_to_clo.get(clt)=="pro"):
                    req.append((act,clothing_to_clo.get(clt)))
                    break
                    
            
        if len(req)==0:
            return "I would recommend staying inside."
        
        for pair in req:
            if pair[0]=="resting":
                if pair[1]=="naked":
                    return "Nudity works for today.\nGo out and give the twins some air... And make your neighbors regret their windows."
                elif pair[1]=="normal":
                    return "Casual attire.\nI don't need to tell you what to wear. You'll be fine."
                elif pair[1]=="light":
                    return "Long pants and sleeved shirts.\nA decent sweater should get you by."
                elif pair[1]=="medium":
                    return "Thick down or fur coats. Hats and gloves.\nHats and gloves and jackets. Keep your limbs and fleshy bits warm."
                elif pair[1]=="heavy":
                    return "The. Warmest. Thing. You. Own.\nBundle up. Batten down the hatches. It's cold."
                elif pair[1]=="pro":
                    return "If you own some Arctic-Grade equipment, now's a good time to wear it. If you don't, you should be sure to keep moving if you go outside."
                
            elif pair[0]=="walking":
                if pair[1]=="naked":
                    return "Nudity works for today.\nYou can have a walk about town in your \"Birthday Suit\" if you like."
                elif pair[1]=="normal":
                    return "Casual attire.\nSo long as you don't sit still, you won't notice the chill no matter what you wear."
                elif pair[1]=="light":
                    return "Long pants and sleeved shirts.\nGrab a coat and have a walk."
                elif pair[1]=="medium":
                    return "Thick down or fur coats. Hats and gloves.\nWear something warm and keep moving."
                elif pair[1]=="heavy":
                    return "The. Warmest. Thing. You. Own.\nIf you don't look like a bundled up Pillsbury Doughboy walking down the street, you will be cold."
                elif pair[1]=="pro":
                    return "Dust off your moose-hide parkas, it's time to walk to the next ice-fishing hole."
                
            elif pair[0]=="jogging":
                if pair[1]=="naked":
                    return "Nudity works for today.\nIf you plan on jogging the whole way, you should be able to survive going naked."
                elif pair[1]=="normal":
                    return "Casual attire.\nIf you're going on an exercise run, a T-Shirt will work."
                elif pair[1]=="light":
                    return "Long pants and sleeved shirts.\nIt is a cold day, even for joggers. No one wears shorts on a day like this."
                elif pair[1]=="medium":
                    return "Thick down or fur coats. Hats and gloves.\nYou will want to get dressed. It is not warm. And, if you do anything other than go for a run, you'll feel it."
                elif pair[1]=="heavy":
                    return "The. Warmest. Thing. You. Own.\nIf you must go outside, dress VERY warmly and don't stop moving."
                elif pair[1]=="pro":
                    return "The seal hunt is starting without you. Grab your mukluks and get a move on."
                
            elif pair[0]=="sprinting":
                if pair[1]=="naked":
                    return "Nudity works for today.\nRun like a headless chicken and you will be plenty warm."
                elif pair[1]=="normal":
                    return "Casual attire.\nIf today's the marathon, you can leave your coat behind. Otherwise..."
                elif pair[1]=="light":
                    return "Long pants and sleeved shirts.\nGrab your Cliff-Bar, running shoes and coat. It is chilly out there."
                elif pair[1]=="medium":
                    return "Thick down or fur coats. Hats and gloves.\nEven if you're running for your life, I hope you're dressed well. Frostbite awaits otherwise."
                elif pair[1]=="heavy":
                    return "The. Warmest. Thing. You. Own.\nYou should run. As fast as you can. Back home to grab as many coats as you can wear."
                elif pair[1]=="pro":
                    return "Run like you are a well-insulated Arctic researcher and a polar bear is chasing you."
        
    else:
        temp_in_kelvin+=humidity_amp*temp_in_kelvin
        
        #https://richmond.com/limits-of-survival/article_ab7ee429-8e27-5a55-85ee-47e3e82276d5.html
        t = get_survive_time(temp_in_kelvin)
        if t==28800:
            return "I don't need to tell you what to wear. You'll be fine."
        else:
            t=t/(humidity*(temp/333.15))
        if t>=60**2:
            #hours
            return "You should wear as little as possible. Bring plenty of water."
        elif t>=60:
            return "If you're going outside, it's hot. Really. Hot. Go naked, and bring plenty of water. Not kidding."
        else:
            return "I would recommend staying inside."
            
# if __name__=="__main__":
#     # get_clothing(-80, 'C', 70, 50)
#     for i in range(-80,22):
#         print(i,end=":\n")
#         print(get_clothing(i, 'C', i, 50))
#         # print()