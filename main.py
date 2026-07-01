import time
import requests
import datetime as dt
import smtplib

is_on = True
count = 0
count_mail = 0
my_email = ""
password = ""
MY_LATITUDE = 13.963251
MY_LONGITUDE = 121.324281
BEBU_LATITUDE = 25.280950
BEBU_LONGITUDE = 51.549810
my_location = {"lat": MY_LATITUDE,
               "lng": MY_LONGITUDE,
               "tzid": "Asia/Manila",
               "formatted": 0}

#-----------------------------ISS API-----------------------------#
while is_on:
    response = requests.get(url = "http://api.open-notify.org/iss-now.json")
    # print(response.raise_for_status())

    data_iss = response.json()

    iss_longitude = float(data_iss["iss_position"]["longitude"])
    iss_latitude = float(data_iss["iss_position"]["latitude"])

    #-----------------------------SUNRISE SUNSET API-----------------------------#
    response = requests.get(url = "https://api.sunrise-sunset.org/json", params=my_location)
    data_sun = response.json()
    sunrise = int(data_sun["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_sun["results"]["sunset"].split("T")[1].split(":")[0])

    response2 = requests.get(url="https://api.sunrise-sunset.org/json", params=bebu_location)
    data_sun2 = response2.json()

    time_now = dt.datetime.now()
    hour_now = time_now.hour

    #-----------------------------CHECK IF ISS IS NEAR AT NIGHTTIME-----------------------------#
    latitude_difference = round(abs(MY_LATITUDE - iss_latitude),4)
    longitude_difference = round(abs(MY_LONGITUDE - iss_longitude),4)

    if latitude_difference <= 5 and longitude_difference <= 5:
        if hour_now <= sunrise or hour_now >= sunset:
            count_mail +=1
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs=my_email,
                                    msg=f"Subject: Look UP at the ISS!\n\nAt {time_now}, has passed over Tiaong, Quezon. Sent thru Python.")

    count +=1
    print(f"Tiaong, PH: Latitude diff: {latitude_difference} / Longitude diff: {longitude_difference}")
    print(f"Checking again after 2-3 minutes. Count: {count} / Mail sent: {count_mail}")

    if count % 2 == 0:
        time.sleep(120)
    else:
        time.sleep(150)
