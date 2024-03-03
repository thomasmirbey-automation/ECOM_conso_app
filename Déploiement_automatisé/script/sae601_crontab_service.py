import os
import subprocess

def check_and_add_cron_line(cron_line):
    # Get the current crontab content
    try:
        current_crontab = subprocess.check_output(["crontab", "-l"], text=True)
    except subprocess.CalledProcessError:
        current_crontab = ""
    
    # Check if the line already exists in the crontab
    if cron_line not in current_crontab:
        # Append the line to the crontab
        new_crontab = current_crontab.strip() + "\n" + cron_line.strip() + "\n"
        
        # Install the modified crontab
        subprocess.run(["echo", new_crontab], stdout=subprocess.PIPE, text=True)
        subprocess.run(["crontab", "-"], input=new_crontab, text=True)
        
        print("Cron line added.")
    else:
        print("Cron line already exists.")

def create_service_file(servicename):
    service_file_path = "/etc/systemd/system/"+servicename+".service"
    
    # Check if the service file already exists
    if not os.path.exists(service_file_path):
        # Define the content of the service file
        service_content = f"""[Unit]
        Description={servicename}
        After=network.target

        [Service]
        Type=simple
        ExecStart=python3 /script/{servicename}.py
        Restart=always

        [Install]
        WantedBy=multi-user.target
        """
        
        # Write the content to the service file
        with open(service_file_path, 'w') as service_file:
            service_file.write(service_content)
        
        # Reload systemd
        os.system("systemctl daemon-reload")
        
        print("Service file created.")
    else:
        print("Service file already exists.")

if __name__ == "__main__":
    create_service_file("ipDiscover")
    create_service_file("listenerLoRa")
    check_and_add_cron_line("*/15 * * * * python3 /script/sae601_auto_data.py")
    #check_and_add_cron_line("newline")

    


