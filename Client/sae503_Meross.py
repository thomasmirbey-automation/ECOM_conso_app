import asyncio
import os
from tkinter import messagebox
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.controller.mixins.electricity import ElectricityMixin
from sae503_bdd_set import *

EMAIL = "kyllian.cuevas@gmail.com"
PASSWORD = 'Pepito68*'
API_BASE_URL = "https://iotx-eu.meross.com"
plug_name=""
plug_status=""
power=""
voltage=""
current=""
plugs_list=[]
mesures=[]

async def main(name,status):
    global plug_name,plug_status,power,voltage,current
    # Setup the HTTP client API from user-password
    try:
        http_api_client = await MerossHttpClient.async_from_user_password(
            api_base_url=API_BASE_URL,
            email=EMAIL,
            password=PASSWORD,
        )

        # Setup and start the device manager
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()

        # Retrieve all the MSS310 devices that are registered on this account
        await manager.async_device_discovery()
        plugs = manager.find_devices(device_type="mss310")
        plug_object=[]
        for plug in plugs:
            #print(plug.name)
            if(str(plug.name==str(name))):
            #if(str(plug).startswith(str(name))):
                plug_object = [plug]
        
        
        if len(plug_object) == 0:
            print("No MSS310 plugs found...")
        else:
            # Turn it on channel 0
            # Note that the channel argument is optional for MSS310 as they only have one channel
            dev = plug_object[0]

            # Update device status: this is needed only the very first time we play with this device (or if the
            #  connection goes down)
            if(status=="on" or status=="off"):
                await dev.async_update()
                
                instant_consumption = await dev.async_get_instant_metrics()
                #print(f"Current consumption data: {instant_consumption}")
                #print(instant_consumption.power)
                if(status=="on"):
                    print(f"Turning on {dev.name}...")
                    await dev.async_turn_on(channel=0)
                    plug_name=name
                    plug_status="on"
                #,instant_consumption.power,instant_consumption.voltage,instant_consumption.current
                else:
                    print(f"Turning off {dev.name}")
                    await dev.async_turn_off(channel=0)
                    plug_name=name
                    plug_status="off"
                    
            else:
                return name,"error"

        # Close the manager and logout from http_api
        manager.close()
        await http_api_client.async_logout()
    except:
        pass

async def get_data():
    global plug_name,power,voltage,current,mesures,plugs
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(
        api_base_url=API_BASE_URL,
        email=EMAIL,
        password=PASSWORD,
    )

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS310 devices that are registered on this account
    await get_all_plugs()
    for plug in plugs_list:
        #print(plug.name)
        plug_object = [plug]
        
        # Turn it on channel 0
        # Note that the channel argument is optional for MSS310 as they only have one channel
        dev = plug

        # Update device status: this is needed only the very first time we play with this device (or if the
        #  connection goes down)
        
        await dev.async_update()
        instant_consumption = await dev.async_get_instant_metrics()
        
        plug_name,power,voltage,current=plug.name,instant_consumption.power,instant_consumption.voltage,instant_consumption.current
        mesure={"name":plug_name,"power":power,"voltage":voltage,"current":current}
        mesures.append(mesure)
    
    

                
    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

async def get_all_plugs():
    global plugs_list
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(
        api_base_url=API_BASE_URL,
        email=EMAIL,
        password=PASSWORD,
    )

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()
    await manager.async_device_discovery()
    plugs_list = manager.find_devices(device_type="mss310")
    


def exec_meross(name,status):
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(name,status))
    if status == "on":
        messagebox.showinfo("Etat de la prise", "La prise est allumée")
    else:
        messagebox.showinfo("Etat de la prise", "La prise est éteinte")
    #loop.run_until_complete(get_data())
    loop.stop()

def get_mesures():
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(get_data())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
   
   
def get_plugs():
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_all_plugs())
    loop.stop()
    

"""exec_meross("Prise1", "on")

get_mesures()
print(mesures)
for prise in mesures:
    executer_procedure(prise['power'],"W",prise["name"])
    executer_procedure(prise['voltage'],"V",prise["name"])
    executer_procedure(prise['current'],"A",prise["name"])"""
    
