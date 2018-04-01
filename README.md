# gsm-module
A module for accessing AT commands to use with a SIM module

## Usage
First to establish the connection:

```python
from gsmmodule import GSM

ob = GSM()
ob.connect() # connects automatcially with found port and starts non blocking listener
```

To send an AT command:
```python
ob.send('AT+OK')
ob.send('AT+CMGR=1')
# response will be received in listener and printed out immediately
```

To send an SMS:
```python
from gsmmodule import SMS

# connects automatically with the device (if already not connected)
ob = SMS()
ob.send_sms("+880171231121", "Hello World")
```
