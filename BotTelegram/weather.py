import pyowm

owm = pyowm.OWM("f71c23329ecc0fff8824830092b7b9a8")




#sity = input("Какой город вас интересует? ")
sity = "Пушкино"
mgr = owm.weather_manager()
observation = mgr.weather_at_place(sity)
w = observation.weather


#Temperature
MidleTemperature = w.temperature('celsius')['temp']
MaxTemperature = w.temperature('celsius')['temp_max']
MinTemperature = w.temperature('celsius')['temp_min']

wind = w.wind()['speed']
rain = w.rain
clouds = w.clouds 
status = w.detailed_status    
    


print(sity,":", MidleTemperature,"°, " "💨Ветер: ", wind,"м/с, " " 🌫 Облачность: ",clouds, "%", '\n', status)
#rint(status)
if status == 'light rain':
  print("Сейчас идет маленький дождь 🌧")
elif status == 'overcast clouds':
  print("Пасмурно 🌧")
elif status == 'rain':
  print("Сейчас идет дождь 🌧")
elif status == 'moderate rain':
  print("Умеренный дождь 🌧")


