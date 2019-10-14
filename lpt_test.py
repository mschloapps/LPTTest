## Time to complete 3 hours, 10 min.
## Python 3.7.4
## Used matplotlib v.3.1.1 for plotting the data.
import matplotlib.pyplot as plt

## Import mysql interface library
import mysql.connector

## Import struct library to interpret bytes
import struct


## found this function on Wikipedia (https://en.wikipedia.org/wiki/Two's_complement)
## could have used to calculte value of a signed integer, but used struct library instead
#def twos_complement(input_val, num_bits):
#    mask = 2**(num_bits-1)
#    return -(input_val&mask)+(input_val&~mask)

## create a connection to the mysql database
conn = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="lpttest"
)

## create a cursor
cur = conn.cursor()

## SQL query to get data from database. Gets the blob and the time stamp.
sql = "SELECT HEX(trace_data) as `data`, trace_time FROM test"

## execute the SQL query
cur.execute(sql)

## return the query results
res = cur.fetchall()

## put the data from MySQL into a list
blobs = []
for i in res:
    blobs.append(i)

## create a list to contain all the data
data = []

## loop through each blob
for b in blobs:
    ## break each blob into 4-byte chunks
    datapoints = []    
    for i in range(0, len(b[0]), 8):
        ## get hex string for the 4 bytes
        hstring = str(b[0][i:i+8])
        ## get unsigned integer
        uint_val = int(hstring,16)
        ## pack unsigned integer into bytes
        bt = struct.pack('I', uint_val)
        ## unpack bytes as signed integer
        int_val = struct.unpack('i', bt)[0]
        ## calculate the value of each data point
        value = float(int_val/1000)
        ## append each datapoint he data to 
        datapoints.append(value)
    ## append data points and time stamp
    data.append([datapoints, b[1]])

## infinate loop
while(1):
    ## loop through the data array
    for dt in data:
        ## draw grid on the plot
        plt.grid()
        ## set y label
        plt.ylabel('dBm')
        ## set limits of y-axis
        plt.ylim(-130,-30)
        ## draw the time stamp on the screen
        plt.text(200,-120,dt[1])
        ## plot the datapoints
        plt.plot(dt[0])
        ## delay for 1 second
        plt.pause(1)
        ## clear the screen
        plt.clf()
        
## show the plot
plt.show()
    
