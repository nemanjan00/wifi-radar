import random
import matplotlib.pyplot as plt
import numpy as np
import argparse

from scapy.all import *

parser = argparse.ArgumentParser(description="WiFi radar")

parser.add_argument("--interface", help="Name of interface in monitoring mode", required=True)
parser.add_argument("--ssid", help="Name of WiFi AP to measure", required=True)

args = parser.parse_args()

interface = args.interface
ssid = args.ssid

# buffer for results
size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = [0] * size

plot = []

def configurePlot():
	plt.style.use('ggplot')

	plt.ion()

	fig = plt.figure(figsize=(13,6))
	ax = fig.add_subplot(111)
	plot, = ax.plot(x_vec,y_vec,'-o',alpha=0.8)

	plt.ylabel('Signal (dBm)')
	plt.title('SSID: {}'.format(ssid))
	plt.show()

	return plot

def draw():
	plot.set_ydata(y_vec)

	if np.min(y_vec) <= plot.axes.get_ylim()[0] or np.max(y_vec) >= plot.axes.get_ylim()[1]:
		plt.ylim([np.min(y_vec)-np.std(y_vec),np.max(y_vec)+np.std(y_vec)])

	plt.pause(0.1)

def randomMAC():
	mac = [
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff)
	]

	return ':'.join(map(lambda x: "%02x" % x, mac))

def getSignalStrength(ssid):
	recipients_mac_adress= 'ff:ff:ff:ff:ff:ff'
	your_mac_adress= randomMAC()
	channel = chr(1)

	frame= RadioTap()\
		/Dot11(type=0, subtype=4, addr1=recipients_mac_adress, addr2=your_mac_adress, addr3= recipients_mac_adress)\
		/Dot11ProbeReq()\
		/Dot11Elt(ID='SSID', info=ssid)\
		/Dot11Elt(ID='Rates', info=b'\x82\x84\x8b\x96\x8c\x12\x98\x24')\
		/Dot11Elt(ID='ESRates', info=b'\xb9\x48\x60\x6c')

	answer = srp1(frame, iface=interface, timeout=0.1, verbose=0)

	if answer == None:
		return 0

	return answer.dBm_AntSignal

plot = configurePlot()

while True:
	signal = getSignalStrength(ssid)

	if signal != 0:
		y_vec[-1] = signal

		draw()
		y_vec = np.append(y_vec[1:],0.0)
