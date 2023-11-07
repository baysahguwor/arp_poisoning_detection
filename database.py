import sqlite3

DATABASE_NAME = 'arp_aware_db.sqlite'

def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    # Create the email_settings table
    c.execute('''
              CREATE TABLE IF NOT EXISTS email_settings (
                  smtp_server TEXT,
                  smtp_port INTEGER,
                  smtp_username TEXT,
                  smtp_password TEXT
              )
              ''')
    
    
    # Create the attack_logs table
    c.execute('''
              CREATE TABLE IF NOT EXISTS attack_logs (
                  date TEXT ,
                  time TEXT,
                  attacker_mac TEXT,
                  router_mac TEXT
              )
              ''')
    
    conn.commit()
    conn.close()

def save_email_settings(smtp_server, smtp_port, smtp_username, smtp_password):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM email_settings')
    c.execute('INSERT INTO email_settings VALUES (?, ?, ?, ?)',
              (smtp_server, smtp_port, smtp_username, smtp_password))
    conn.commit()
    conn.close()

def get_email_settings():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('SELECT smtp_server, smtp_port, smtp_username , smtp_password FROM email_settings')
    settings = c.fetchone()
    conn.close()
    return settings


def save_attack_log(current_date, current_timenow, attacker_mac, router_mac):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO attack_logs (date, time, attacker_mac, router_mac) VALUES (?, ?, ?, ?)', (current_date, current_timenow, attacker_mac, router_mac))
    conn.commit()
    conn.close()
