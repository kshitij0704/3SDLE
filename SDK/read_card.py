from smartcard.System import readers
from Crypto.Cipher import AES 
from smartcard.util import PACK,HexListToBinString, BinStringToHexList,toBytes

r=readers()
print(r[0])

#####


key = "31323334353637383132333435363738"
key_as_binstring = HexListToBinString( toBytes( key ) )

KEYB="90 90 90 90 90 90"
READER_AUTH_APDU="FF 82 00 00 06 "




#####

#####
connection=r[0].createConnection()
connection.connect()


#####

def load_auth_key():
	data,sw1,sw2=connection.transmit(toBytes(READER_AUTH_APDU+KEYB))
	#print(data,sw1,sw2,"loaded auth keys")

def decrypt_user_data(user_data):
	print("data",user_data)
	cipher = AES.new(key_as_binstring,AES.MODE_ECB )
	decrypted_as_string = cipher.decrypt(HexListToBinString(user_data))
	return decrypted_as_string

	
def authenticate(blockNo):
	AUTHN=[0xFF,0x88,0x00,blockNo,0x60, 0x00]
	data,sw1,sw2=connection.transmit(AUTHN)
	#print(data,sw1,sw2,"auth")



def get_block_no(sector,block):
	#print("block no",(sector*4)+block)
	return (sector*4)+block

def get_user_data(blockNo):
	READ=[0xFF, 0xB0,0x00,blockNo,0x10]
	data,sw1,sw2=connection.transmit(READ)
	print(data,sw1,sw2)
	return data

load_auth_key()	
sector_no=input("enter the sector(< 16)")
block=input("enter the block (< 3)")
authenticate(get_block_no(sector_no,block))
user_data_en=get_user_data(get_block_no(sector_no,block))
print(user_data_en,"...")
user_data=decrypt_user_data(user_data_en)
print("user data = ",user_data)
