from smartcard.System import readers
from smartcard.util import toHexString,toBytes

r=readers()
print(r[0])

######
SECTOR=0
BLOCK_NO=3
#SECTOR_TRAILER_DATA
#TODO
ACCESS_BYTES=toBytes("78 77 88 69")
KEYA=[144,144,144,144,144,144]
KEYB=[144,144,144,144,144,144]
READER_AUTH_APDU=[0xFF, 0x82, 0x00,0x00,0x06 ,0xFF ,0xFF,0xFF ,0xFF, 0xFF ,0xFF]


######

######
connection=r[0].createConnection()
connection.connect()

######
def load_auth_key(keyNo):
	READER_AUTH_APDU=[0xFF, 0x82, 0x00,keyNo,0x06 ,0xFF ,0xFF,0xFF ,0xFF, 0xFF ,0xFF]
	data,sw1,sw2=connection.transmit(READER_AUTH_APDU)
	print(data,sw1,sw2,"loaded auth keys")
	
def authenticate(blockNo):
	AUTHN=[0xFF,0x88,0x00,blockNo,0x60, 0x00]
	data,sw1,sw2=connection.transmit(AUTHN)
	print(data,sw1,sw2,"authenticated card")

def get_block_no(i):
	return (i*4)+3

def write_to_sector_trailer(block_no,block_data):
	WRITE="FF D6 00 "+toHexString([block_no])+" 10 "+toHexString(block_data)
	print(WRITE)
	data,sw1,sw2=connection.transmit(toBytes(WRITE))
	print(data,sw1,sw2)



def get_sector_trailer_data():
	sector_data=KEYA+ACCESS_BYTES+KEYB	
	#print(sector_data)
	return sector_data
def create_card():
	for i in range(16):
		authenticate(get_block_no(i))
		write_to_sector_trailer(get_block_no(i),get_sector_trailer_data())

load_auth_key(0)
load_auth_key(1)
create_card()		
	

