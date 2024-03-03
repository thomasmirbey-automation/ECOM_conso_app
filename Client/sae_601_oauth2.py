import requests

ip="192.168.1.105"
port="8080"


def get_token(ip,port,username,password):
    url = "http://"+ip+":"+port+"/realms/master/protocol/openid-connect/token"
    payload = 'client_id=admin-cli&username='+str(username)+'&password='+str(password)+'&grant_type=password'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return(response.json())
    except:
        return {}
    
def get_user_list(ip,port,token):

    url = "http://"+ip+":"+port+"/admin/realms/master/users/"

    payload = {}
    headers = {
      'Authorization': 'Bearer '+str(token)
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        return(response.json())
    except:
        return {}


    
def get_user_groups(ip,port,token,userid):

    url = "http://"+ip+":"+port+"/admin/realms/master/users/"+userid+"/groups"

    print(url)
    payload = {}
    headers = {
      'Authorization': 'Bearer '+token
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        return(response.json())
    except Exception as e:
        print(e)
        return {}

username="script"

    
