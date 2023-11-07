from scapy.all import Ether, ARP, srp, sniff, conf
import time
from sentmail import send_email
import socket 
import sound
import sys
import scapy.all as scapy
from database import save_attack_log
from datetime import datetime

# Define a global variable to track the last alert time and attack ongoing flag
last_alert_time = 0
attack_ongoing = False

# Configure time for logging
current_timenow = None
current_date = None

def get_mac(ip):
    """
    Returns the MAC address of `ip`, if it is unable to find it
    for some reason, throws `IndexError`
    """
    p = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    result = srp(p, timeout=3, verbose=False)[0]
    return result[0][1].hwsrc

def get_pc_name():
    """
    Returns the current PC's name (hostname)
    """
    return socket.gethostname()

def process(packet):
    global last_alert_time
    global attack_ongoing
    global current_timenow
    global current_date

    # if the packet is an ARP packet
    if packet.haslayer(ARP):
        # if it is an ARP response (ARP reply)
        if packet[ARP].op == 2:
            try:
                # get the real MAC address of the sender
                real_mac = get_mac(packet[ARP].psrc)
                # get the MAC address from the packet sent to us
                response_mac = packet[ARP].hwsrc
                # if they're different, definitely there is an attack
                if real_mac != response_mac:
                    current_time = time.time()

                    if not attack_ongoing:
                        attack_ongoing = True

                    if current_time - last_alert_time >= 20:
                        last_alert_time = current_time
                        pc_name = get_pc_name()
                        sound.start_sound()
                        alert_message = f"You are under attack, Attacker-MAC: {real_mac.upper()}, FAKE-MAC: {response_mac.upper()}"
                        attacker_mac = f"{real_mac.upper()}"
                        router_mac = f"{response_mac.upper()}"
                        print(alert_message)
                     
                        # Save the attack log to the database
                        save_attack_log(current_date, current_timenow, attacker_mac, router_mac)
                        send_email(f"PC is Under Attack!!!", f"We have detected that your PC [{pc_name}] is under attack. {alert_message}")
                      
                       

            except IndexError:
                pass

        else:
            # Reset the attack state if no longer under attack
            attack_ongoing = False

    # Update the current time and date
    now = datetime.now()
    current_timenow = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

def stop_monitoring():
    global monitoring_enabled
    global attack_ongoing

    monitoring_enabled = False
    attack_ongoing = False

def start_monitoring(interface):
    global monitoring_enabled
    global attack_ongoing

    monitoring_enabled = True

    try:
        while monitoring_enabled:
            scapy.sniff(iface=interface, store=False, prn=process)
            time.sleep(1)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        pass

    print(f"Monitoring on interface {interface} stopped.")

if __name__ == "__main__":
    import sys
    try:
        iface = sys.argv[1]
    except IndexError:
        iface = conf.iface
    sniff(store=False, prn=process, iface=iface)
    
