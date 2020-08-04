#!/usr/bin/env python3
#nnclient test config
#Use ssh-key in production.

try:
    from ncclient import manager
    from ncclient.xml_ import new_ele, sub_ele
except ImportError as err:
    print(err)

#connect to routers.
routers = [f'192.168.1.{n}' for n in range(99, 103)]

def conn(username, passwd, port):
    for router, n in zip(routers, range(1, 5)):
        #junos config data. 
        with manager.connect(host= router,
                username= username,
                password= passwd,
                port= port,
                timeout= 10,
                device_params= {'name': 'junos'},
                hostkey_verify= False) as dev:

            if dev:
                print(f'{router} - connected.')

                #configure hostname
                hostname= new_ele('system')
                sub_ele(hostname, 'host-name').text= f'router{n}'

                #lock config
                dev.lock()

                #load hostname configuration
                dev.load_configuration(config= hostname)

                #validate configuration
                dev.validate()

                #commit confirm configuration
                dev.commit(confirmed= True, timeout= '300')

                #unlock configuration
                dev.unlock()
            
            else:
                print('Han nga mabalin.')

if __name__ == '__main__':
        conn('root', 'password123', '830')
