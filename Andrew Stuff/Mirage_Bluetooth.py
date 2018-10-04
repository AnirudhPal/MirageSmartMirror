# Import Standard Modules
import os
import dbus
import subprocess

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

# Bluezero Peripheral import
from bluezero import peripheral
from bluezero import constants
from bluezero import adapter
from bluezero import advertisement
from bluezero import localGATT
from bluezero import GATT

# UUID Constants

WIFI_MONITOR_SRVC = 'c30b8a67-d1a2-40e3-a407-9f126001b6cc'
WIFI_STAT_CHRC = '43ec4c0c-6d53-44a6-ae81-a6e6518269d4'
WIFI_SSID_CHRC = '1249e241-7624-4158-acd5-86226f7637c8'
WIFI_PASS_CHRC = '290d03b7-6e73-4e1e-ab70-ac8997cc0506'


def get_wifi_status() :
	# Check WiFi connectivity
	f = os.popen('iwgetid')
	now = f.read()
	if not now == '':
		return 1
	else:
		return 0


def get_wifi_ssids() :
	# Execute sudo iwlist wlan0 scan | grep -e ESSID | grep -oP 'ESSID:"\K[^"]+' | sort -u
        return

def try_connecting_to_network(essid, password) :
	os.system('iwconfig wlan0 essid ' + essid + ' key s:' + password)
	return

def setup_password_prompt(ssid):
	return

def enter_password(password):
	fb = open('passphrase.txt', 'a+')
	fb.write(password)
	fb.close()
	os.system('wpa_passphrase \"' + WiFiSSIDChrc.ssid + '\" < passphrase.txt | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null')
	os.system('wpa_cli -i wlan0 reconfigure')
	os.system('rm -f passphrase.txt')
	# Should also remove plaintext password from wpa_supplicant.conf with sudo grep -vh '^[[:space:]]*#' /etc/wpa_supplicant/wpa_supplicant.conf 
class WiFiSSIDChrc(localGATT.Characteristic):
	ssid = ""
	def __init__(self, service):
		localGATT.Characteristic.__init__(self,
						  2,
						  WIFI_SSID_CHRC,
						  service,
						  "",
						  False,
						  ['write'])


	def WriteValue(self, value, options):
		WiFiSSIDChrc.ssid = ""	# Clean the value from any previous attempts
		WiFiSSIDChrc.ssid = ''.join([chr(byte) for byte in value])
		setup_password_prompt(WiFiSSIDChrc.ssid)
		self.wifiSSID_cb()

	def wifiSSID_cb(self):
		self.props[constants.GATT_CHRC_IFACE]['Value'] = WiFiSSIDChrc.ssid
		self.PropertiesChanged(constants.GATT_CHRC_IFACE,
				       {'Value': dbus.Array(WiFiSSIDChrc.ssid)},
				       [])

class WiFiPASSChrc(localGATT.Characteristic):
	wifiPass = ""
	def __init__(self, service):
		localGATT.Characteristic.__init__(self,
						  3,
					   	  WIFI_PASS_CHRC,
						  service,
						  "",
						  False,
						  ['write'])

	def WriteValue(self, value, options):
		WiFiPASSChrc.wifiPass = ""	# Clean the value from any previous attempts
		WiFiPASSChrc.wifiPass = ''.join([chr(byte) for byte in value])
		enter_password(WiFiPASSChrc.wifiPass)
		self.wifiPass_cb()

	def wifiPass_cb(self):
		self.props[constants.GATT_CHRC_IFACE]['Value'] = WiFiPASSChrc.wifiPass
		self.PropertiesChanged(constants.GATT_CHRC_IFACE,
				       {'Value': dbus.Array(WiFiPASSChrc.wifiPass)},
				       [])


class WiFiStatChrc(localGATT.Characteristic):
	def __init__(self, service):
		localGATT.Characteristic.__init__(self,
						  1,
						  WIFI_STAT_CHRC,
						  service,
						  get_wifi_status(),
						  False,
						  ['read', 'notify'])

	def wifiStatus_cb(self):
		status = [get_wifi_status()]
		#print('Getting wifi status',
		#	status,
		#	self.props[constants.GATT_CHRC_IFACE]['Notifying'])
		self.props[constants.GATT_CHRC_IFACE]['Value'] = status

		self.PropertiesChanged(constants.GATT_CHRC_IFACE,
					{'Value': dbus.Array(status)},
					[])

		#print('Value: ', status)
		return self.props[constants.GATT_CHRC_IFACE]['Notifying']


	def ReadValue(self, options):
		status = [get_wifi_status()]
		self.props[constants.GATT_CHRC_IFACE]['Value'] = status
		return dbus.Array(self.props[constants.GATT_CHRC_IFACE]['Value'])


	def _update_wifi_status(self):
		if not self.props[constants.GATT_CHRC_IFACE]['Notifying']:
			return

		print('Starting timer event')
		GObject.timeout_add(500, self.wifiStatus_cb)


	def StartNotify(self):
		if self.props[constants.GATT_CHRC_IFACE]['Notifying']:
			print ('Already notifying, nothing to do')
			return
		print('Notifying on')
		self.props[constants.GATT_CHRC_IFACE]['Notifying'] = True
		self._update_wifi_status()

	def StopNotify(self):
		if not self.props[constant.GATT_CHRC_IFACE]['Notifying']:
			print ('Not notifying, nothing to do')
			return

		print('Notifying off')
		self.props[constants.GATT_CHRC_IFACE]['Notifying'] = False
		self._update_wifi_status()



class ble:
	def __init__(self):
		self.bus = dbus.SystemBus()
		self.app = localGATT.Application()
		self.srv = localGATT.Service(1, WIFI_MONITOR_SRVC, True)

		# Setup Characteristics

		self.wifiStatusCharc = WiFiStatChrc(self.srv)
		self.wifiSSIDCharc = WiFiSSIDChrc(self.srv)
		self.wifiPASSCharc = WiFiPASSChrc(self.srv)

		self.wifiStatusCharc.service = self.srv.path
		self.wifiSSIDCharc.service = self.srv.path
		self.wifiPASSCharc.service = self.srv.path

		# If needed, do anything with Descriptors here


		# Add Services, Characteristics to Application

		self.app.add_managed_object(self.srv)
		self.app.add_managed_object(self.wifiStatusCharc)
		self.app.add_managed_object(self.wifiSSIDCharc)
		self.app.add_managed_object(self.wifiPASSCharc)

		# Register Application

		self.srv_mng = GATT.GattManager(adapter.list_adapters()[0])
		self.srv_mng.register_application(self.app, {})

		# Setup Advertisement on DBus adapter 1

		self.dongle = adapter.Adapter(adapter.list_adapters()[0])
		self.advert = advertisement.Advertisement(1, 'peripheral')

		# Assign Service UUID

		self.advert.service_UUIDs = [WIFI_MONITOR_SRVC]

		if not self.dongle.powered:
			self.dongle.powered = True

		# Register Advertisement

		self.ad_manager = advertisement.AdvertisingManager(self.dongle.address)
		self.ad_manager.register_advertisement(self.advert, {"local-name":"Pi"})

	def add_call_back(self, callback):
		self.wifiStatusCharc.PropertiesChanged = callback

	def start_bt(self):
		self.app.start()

	def stop_bt(self):
		self.ad_manager.unregister_advertisement(self.advert)

if __name__ == '__main__':
	print('Wifi status is {}'.format(get_wifi_status()))
	print(get_wifi_status())

	try:
		pi_wifi_monitor = ble()
		pi_wifi_monitor.start_bt()
	except KeyboardInterrupt:
		pi_wifi_monitor.stop_bt()
