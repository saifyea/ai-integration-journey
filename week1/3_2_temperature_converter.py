#Celcius to Fahrenheit converter function
def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return celsius,fahrenheit

celsius, fahrenheit_value = celsius_to_fahrenheit(100)
print(celsius, "°C is equal to", fahrenheit_value, "°F")

temperature = 25
def celsius_to_fahrenheit(temperature):
    fahrenheit = (temperature * 9/5) + 32
    return fahrenheit

fahrenheit_value = celsius_to_fahrenheit(temperature)
print(temperature, "°C is equal to", fahrenheit_value, "°F")

def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    print(celsius, "°C =", fahrenheit, "°F")
    return fahrenheit

celsius_to_fahrenheit(35)