import ipaddress
#import sae503_Meross
import sae503_bdd_get
import sae503_bdd_set
import sae503_MQTT
import sae503_shelly

shelly_ip = "192.168.1.128"

cli=sae503_MQTT.mqtt_client("192.168.1.105",1883,16)

cli.loop_start()


plug_list=sae503_bdd_get.execute_stored_procedure("GET_objets",1)
print(plug_list)
for plug in plug_list:
    try:
        if("," in str(plug[2])):
            
            shelly_output=sae503_shelly.get_switch_details(shelly_ip,0)
            
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
        else:
            
            ip=ipaddress.ip_address(plug[2])
            #print("MQTT",ip)
            #sae503_MQTT.subscribe_to_topics(cli, plug[2]+"/measures")
            print("MQTT TO ",plug[2])            
            sae503_MQTT.mqtt_publish(cli,"mesures/"+plug[2],"get_mesures")
    except Exception as e:
        pass
'''
try:     
    #sae503_Meross.get_mesures()
    for Meross_Switch_data in sae503_Meross.mesures:
        name=Meross_Switch_data["name"]
        power=Meross_Switch_data["power"]
        voltage=Meross_Switch_data["voltage"]
        current=Meross_Switch_data["current"]
        sae503_bdd_set.executer_procedure( power,"W", name)
        sae503_bdd_set.executer_procedure( voltage,"V", name)
        sae503_bdd_set.executer_procedure( current,"A",name)
except:
    pass
'''
