# dham


## Client
Is Written on Micropyhon 3.


Initial settings required:
Update first_boot_wifi.txt.example with your SSID and PASSWORD (and rename it to first_boot_wifi.txt) and run ./first_boot command, to load initial firmware. After firmware will be uploaded, please, check your ip address and fill it in wifi.json.example together with other parameters (also renaming it to wifi.json). Now you can upload some functional firmware to your controller.

## Server
Is written on Django 3.


To start using it, please, set up initial settings using environment variables: DHAM_SECRET_KEY, DHAM_DEBUG, DHAM_ALLOWED_HOSTS
