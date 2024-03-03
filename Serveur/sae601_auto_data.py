import sae503_Meross
import sae503_bdd_get
import sae503_bdd_set
import sae503_MQTT
import sae503_shelly
import csv
import ipaddress
import time
from datetime import datetime

start=time.time()
todays_date=datetime.now()
todays_date_reformated=todays_date.strftime("%d_%m_%Y-%H_%M_%S")
filename="/log/sae601_auto_data.py_log_"+todays_date_reformated+".csv"

with open(filename,'w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time','Action','Status'])
    
    shelly_ip = "192.168.1.128"


    cli=sae503_MQTT.mqtt_client("192.168.1.105",1883,16)
    if(cli==0):
        writer.writerow([datetime.now().strftime('%H:%M:%S'),'connexion to MQTT Broker','error'])
    else:
        writer.writerow([datetime.now().strftime('%H:%M:%S'),'connexion to MQTT Broker','OK'])
    cli.loop_start()


    plug_list=sae503_bdd_get.execute_stored_procedure("GET_objets",1)
    print(plug_list)
    try:
        test=plug_list[0]
        writer.writerow([datetime.now().strftime('%H:%M:%S'),'retrieve all plugs from database','OK'])
        for plug in plug_list:
            writer.writerow([datetime.now().strftime('%H:%M:%S'),'Current switch : '+str(plug[2]),'running ...'])
            try:
                if("," in str(plug[2])):
            
                    shelly_output=sae503_shelly.get_switch_details(shelly_ip,0)
            
                    writer.writerow([datetime.now().strftime('%H:%M:%S'),'connexion to shelly switch : '+str(shelly_ip),'OK'])
                    id_prise=str(plug[2]).split(",")[1]
            
                    prise_data=shelly_output["switch:"+id_prise]
                    prise_w=prise_data["apower"]
                    prise_v=prise_data["voltage"]
                    prise_a=prise_data["current"]
                    print(prise_w,prise_v,prise_a)
                    print( str(plug[2]))
                 
                    sae503_bdd_set.executer_procedure( prise_w,"W", str(plug[2]))
                    sae503_bdd_set.executer_procedure( prise_v,"V", str(plug[2]))
                    sae503_bdd_set.executer_procedure( prise_a,"A",str(plug[2]))

                    writer.writerow([datetime.now().strftime('%H:%M:%S'),'data storage for shelly switch','OK'])
                else:
            
                    ip=ipaddress.ip_address(plug[2])
                    print("MQTT",ip)
                    sae503_MQTT.subscribe_to_topics(cli,"mesures/"+plug[2])
                    print("MQTT TO ",plug[2])            
                    sae503_MQTT.mqtt_publish(cli,"mesures/"+plug[2],"get_mesures")

                    writer.writerow([datetime.now().strftime('%H:%M:%S'),'connexion to MQTT switch : '+str(plug[2]),'OK'])
            except ValueError as v:
                print(plug)
                print(v)
            except Exception as e:
                writer.writerow([datetime.now().strftime('%H:%M:%S'),'connexion to switch : '+str(plug[2]),'error'])
                print(plug)
                pass
        
        try:     
            sae503_Meross.get_mesures()
            writer.writerow([datetime.now().strftime('%H:%M:%S'),'connexion to Meross cloud','running ...'])
            for Meross_Switch_data in sae503_Meross.mesures:
                name=Meross_Switch_data["name"]
                power=Meross_Switch_data["power"]
                voltage=Meross_Switch_data["voltage"]
                current=Meross_Switch_data["current"]
                writer.writerow([datetime.now().strftime('%H:%M:%S'),'adding data for '+name+' in the database','ok'])
                sae503_bdd_set.executer_procedure( power,"W", name)
                sae503_bdd_set.executer_procedure( voltage,"V", name)
                sae503_bdd_set.executer_procedure( current,"A",name)
                writer.writerow([datetime.now().strftime('%H:%M:%S'),'data for '+name+' successfully added into database','ok'])
        except:
            writer.writerow([datetime.now().strftime('%H:%M:%S'),'connexion to Meross cloud','error'])
            pass
        
        end=time.time()
        exec_duration=end-start
        writer.writerow([datetime.now().strftime('%H:%M:%S'),'End of execution : '+str(exec_duration)+"s",'OK'])
    except:
    
        writer.writerow([datetime.now().strftime('%H:%M:%S'),'retrieve all plugs from database','error'])
        end=time.time()
        exec_duration=end-start
        
        writer.writerow([datetime.now().strftime('%H:%M:%S'),'End of execution : '+str(exec_duration)+"s",'error'])
