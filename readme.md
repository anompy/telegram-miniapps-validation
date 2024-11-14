Validating initData from miniapps is not as difficult as getting a girlfriend

Just copy the source code in this repository into the source.py file



### Example
```python 
bot_token = "your-bot-token"
init_data = "init-data-from-mini-apps"
#custom data expiration time of mini app (default 3600)
expiration_time = 600 #10 minutes

try:
    valid = validate_init_data(init_data=init_data, bot_token=bot_token, expiration_time=expiration_time)
except Exception as err:
    print(err)

if valid:
    print("This data is valid")
else:
    print("invalid data")
    
```

Don't forget to drink mineral water, because your work requires high focus:)