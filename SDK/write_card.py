from smartcard.System import readers
from smartcard.util import toHexString , toBytes,padd
from smartcard.util import toASCIIBytes,toASCIIString
from Crypto.Hash import SHA
from Crypto.Cipher import AES

from smartcard.util import PACK,HexListToBinString, BinStringToHexList

r=readers()
print(r[0])

#####
KEYB="90 90 90 90 90 90"
READER_AUTH_APDU="FF 82 00 00 06 "

key = "31323334353637383132333435363738"
key_as_binstring = HexListToBinString( toBytes( key ) )

#####

#####
connection=r[0].createConnection()
connection.connect()


#####


def load_auth_key():
	
	data,sw1,sw2=connection.transmit(toBytes(READER_AUTH_APDU+KEYB))
	print(data,sw1,sw2,"loaded auth keys")

def encrypt_user_data(user_data):
	#TODO
#	binstring = HexListToBinString( user_data )
	user_data=padd(toASCIIBytes(user_data),16)
	cipher = AES.new(key_as_binstring,AES.MODE_ECB )
	encrypted_as_string = cipher.encrypt(toASCIIString(user_data)).encode('hex')
	decrypted_as_string = cipher.decrypt( encrypted_as_string )

	print("ans",encrypted_as_string,decrypted_as_string)
	return  toBytes(encrypted_as_string)

	#return user_data

	
def authenticate(blockNo):
	AUTHN=[0xFF,0x88,0x00,blockNo,0x61, 0x00]
	data,sw1,sw2=connection.transmit(AUTHN)
	print(data,sw1,sw2)

def get_block_no(sector,block):
	if(block==3):
		print("Warning ! that is a sector trailer")
		return -1
	return (sector*4)+block

def write_to_block(block_no,block_data):
	#TODO
	WRITE = "FF D6 00 "+toHexString([block_no])+" 10 "+toHexString(block_data)
	print(WRITE)
	data,sw1,sw2=connection.transmit(toBytes(WRITE))
	print(data,sw1,sw2)


user_data=raw_input("enter the data to be inserted")	
sector_no=input("enter the sector(<16)")
block=input("enter the block (<3)")
load_auth_key()
user_data_en=encrypt_user_data(user_data)
authenticate(get_block_no(sector_no,block))
write_to_block(get_block_no(sector_no,block),user_data_en)


