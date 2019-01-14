from contentful import Client

client = Client('wjuty07n9kzp', 'de842675273a862fc0578632df2c95cf97ea6590de1820075c0abf2853e5ac22', environment='mast')


space = client.spaces().find('wjuty07n9kzp')
