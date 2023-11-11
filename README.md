# shevark
for this setup you need your bot token and your id (find @botfather in tg for the token and @userinfobot for the id)

1. Download the .zip file
2. Unzip it using `unzip shevark-main.zip` (if not installed use `sudo apt install unzip` )
3. Navigate inside the dir `cd shevark-main`
4. Run `cat .env.example > .env`
5. Replace my-token with your actual bot token and run `sed -i 's/TOKEN=.*/TOKEN=my-token/' .env`
6. Replace my-id with your telegram id and run `sed -i 's/ADMIN_ID=.*/ADMIN_ID=my-id/' .env`
7. Run `docker-compose up -d`
