# Warframe.market parser

### Description
This application is a tool that automatically uses the warframe.market API to check a user's current item sell prices against other items being sold, and notifies the user of the price difference.


### Getting Started

1. Download the application
- Click on the green download code button, then download the ZIP file. 
- Extract to a directory of your choosing

Note: Some anti-viruses flag this as a trojan. It's a false flag, but if this concerns you, you can build from the source code (main.py) by using a tool such as Py2Exe or Pyinstaller.

2. Get your cookie
- Note: Instructions are for Google Chrome, but similar steps are used for other web browsers.
- Log in to warframe.market and press `ctrl+shift+i` to open the developer tools
- Navigate to the `Application` tab, open `Cookies` on the sidebar, and select `https://warframe.market`
- There should be a cookie with `Name: JWT`. Copy the `Value` field of this, and make note of it. You'll reuse it in a later step!
- Note: This is your authentication key to warframe.market, so don't give it out!
3. Generate the configuration file
- The application expects a file called "config.txt" to be placed in the same directory as it.
- The layout of the file is as follows (copy and paste)

        [Default]
        username = [your username goes here]
        threshold = [your threshold goes here]
        cookie = [your cookie goes here]

4. Run the application
- Run main.exe, which will automatically take the information placed in the configuration file and store it internally.
- Once the application has loaded, press `Start` to have the application automatically contact warframe.market.
- The application will display the items and prices that it is fetching, and store them in a .csv file called `prices.csv`.

5. That's it!
- Once you have the prices laid out, it's up to you to decide what to do with your newfound information. Enjoy!
