# MetawearServer

#### Requirements

1. Sqlalchemy - `pip install sqlalchemy`
2. flask - `pip install flask`
3. pymysql (only if using DB) - `pip install pymysql`
4. MySql (only if using DB) - Get it [here](https://dev.mysql.com/downloads/mysql/)

#### To Run

To run server simply run -

For mac/Linux

    $ export FLASK_APP=server.py
    $ python -m flask run

For windows

    $ set FLASK_APP=server.py
    $ python -m flask run

Now, this will setup the server on your local machine (running
on port 5000 by default). To share your local host through
tunnelling to remote devices, you need ngrok (see below).

#### Use ngrok to share local host

Get ngrok from [here](https://ngrok.com/download). Once downloaded
on your machine, locate the folder where the runnable ngrok file is present (extract files
if you need to). Finally, assuming your local host is running on
port 5000, run

    $ ./ngrok http 5000

or on windows

    $ ngrok.exe http 5000

This will start sharing your local host through ngrok tunnels.
The shareable url should be visible in the terminal next to the
`forwarding` text on the terminal output. It should look something like
`https://5dbcb8e6.ngrok.io`. That is your shareable url.

Finally, connect the pi to a screen and keyboard and login to it. Once in, cd into the
folder `pymetawear/examples` and open `accelerometer.py` in it look for the variable `server_url`, change
it to whatever you get from ngrok. This would also be a good time to configure the wi-fi credentials.

After doing this, restart the pi and look out on the console wherever the server is running for messages indicating
the number of samples received. The server console will also indicate when the pi loses connection to the metawear.
There is a wait of 20 seconds for each connection attempt, it may take 1-2 connection attempts to start the initial connection.
