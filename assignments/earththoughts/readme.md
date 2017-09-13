Availability: 24/7 (until next assignment)  
URL: https://vagrant.ssilva.work  
About: this project puts text from [/r/Showerthoughts](https://www.reddit.com/r/Showerthoughts/) over images from [/r/EarthPorn](https://www.reddit.com/r/EarthPorn/). 

### How to use
1. run `vagrant up` to start the vm
2. run `vagrant ssh` to ssh into the vm
3. create a reddit app at https://www.reddit.com/prefs/apps and note the client id and secret
4. inside the vm run `export CLIENT_ID=[your client id]` and `export CLIENT_SECRET=[your client secret]`
5. run `cd /var/www/scripts` to change to the directory with `app.py`
6. run `python app.py`
7. the vm is setup to connect Apache (the webpage server) to host port 4567 and flask (the api server) to port 4568.  change the api url in `www/html/index.html` to match how you will be serving the site (http://localhost:4568/api/) if you only want to access it locally).
