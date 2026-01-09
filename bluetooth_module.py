
import asyncio
from bleak import BleakScanner, BleakClient
import threading
import time

# Standard Heart Rate UUIDs
HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

class BluetoothManager:
    def __init__(self):
        self.connected_device = None
        self.client = None
        self.current_hr = 0
        self.is_scanning = False
        self.scan_results = []
        
    def start_scan(self, callback):
        """ Scans for BLE devices in a separate thread """
        self.is_scanning = True
        
        def _scan():
            async def run():
                # Try to prefer Heart Rate devices
                # We can't strictly filter by UUID during discover because some devices don't advertise it until connected.
                # But we can check `metadata` if needed.
                # For now, let's just show everything but sort better.
                devices = await BleakScanner.discover(timeout=5.0)
                
                # Sort by RSSI if available, else default to -100
                self.scan_results = sorted(devices, key=lambda d: getattr(d, 'rssi', -100), reverse=True)
                
                # Filter out devices with no name
                filtered = [d for d in self.scan_results if d.name and "Unknown" not in d.name]
                print(f"Found {len(filtered)} named devices.")
                self.is_scanning = False
                callback(filtered)
                
            asyncio.run(run())
            
        t = threading.Thread(target=_scan)
        t.daemon = True
        t.start()

    def connect_device(self, address, success_callback, error_callback):
        """ Connects to a device by address """
        def _connect():
            async def run():
                print(f"Connecting to {address}...")
                try:
                    self.client = BleakClient(address)
                    await self.client.connect()
                    
                    if self.client.is_connected:
                        print(f"Connected to {address}")
                        self.connected_device = address
                        
                        # Start HR Notification
                        await self.client.start_notify(HR_MEASUREMENT_UUID, self._hr_notification_handler)
                        success_callback()
                        
                        # Keep alive
                        while self.client.is_connected:
                            await asyncio.sleep(1)
                    else:
                        error_callback("Failed to connect")
                except Exception as e:
                    print(f"BLE Error: {e}")
                    error_callback(str(e))
                    
            asyncio.run(run())
            
        t = threading.Thread(target=_connect)
        t.daemon = True
        t.start()

    def _hr_notification_handler(self, sender, data):
        """ Parses standard HR Measurement format """
        # Byte 0: Flags
        # Byte 1: HR Value (if uint8)
        # Check flag bit 0: 0=uint8, 1=uint16
        
        flag = data[0]
        if flag & 0x01: # 16-bit
            hr = int.from_bytes(data[1:3], byteorder='little')
        else: # 8-bit
            hr = data[1]
            
        self.current_hr = hr
        if hr > 0:
            print(f"Heart Rate: {hr} BPM")

# Global instance
bt_manager = BluetoothManager()
