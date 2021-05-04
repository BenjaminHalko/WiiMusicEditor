import os
import sys
import getpass
import time
import subprocess
import configparser
import pathlib
from shutil import copyfile
import tempfile
import mido
from math import floor
import AutoUpdate

time.sleep(0.05)

#Song Names
SongNames = [
'A Little Night Music',
'American Patrol',
'Animal Crossing',
'Animal Crossing K.K. Blues',
'Bridal Chorus',
'Carmen',
'Chariots of Fire',
'Daydream Believer',
'Do-Re-Mi',
'Every Breath You Take',
'F-Zero',
'Frere Jacques',
'From Santurtzi to Bilbao',
'From the New World',
'Happy Birthday to You',
'Ill Be There',
'Ive Never Been to Me',
'Jingle Bell Rock',
'La Bamba',
'La Cucaracha',
'Little Hans',
'Long Long Ago',
'Material Girl',
'Minuet in G Major',
'My Grandfathers Clock',
'O-Christmas Tree',
'Ode To Joy',
'Oh My Darling Clementine',
'Over the Waves',
'Please Mr. Postman',
'Sakura Sakura',
'Scarborough Fair',
'September',
'Sukiyaki',
'Super Mario Bros',
'Sur le Pont d Avignon',
'Swan Lake',
'The Blue Danube',
'The Entertainer',
'The Flea Waltz',
'The Legend of Zelda',
'The Loco Motion',
'Troika',
'Turkey in the Straw',
'Twinkle Twinkle Little Star',
'Wake Me Up Before You Go-Go',
'Wii Music',
'Wii Sports',
'Woman',
'Yankee Doodle',
'Menu Song']

#Offsets
SongOffsets = [
'60A700',
'6185A0',
'680780',
'63DD00',
'5F9500',
'5FEBA0',
'656CE0',
'652180',
'612AC0',
'654700',
'682860',
'635240',
'640E80',
'627F20',
'610AE0',
'665E60',
'672200',
'0',
'62A700',
'646960',
'63B940',
'62EB60',
'6601A0',
'60DF80',
'625440',
'639B00',
'5F6620',
'6227E0',
'649D20',
'65CE20',
'64D040',
'62C9A0',
'65A200',
'64F3A0',
'674B20',
'632F20',
'5FC280',
'6073A0',
'614E40',
'637040',
'678CE0',
'663180',
'6441E0',
'61C0A0',
'6311A0',
'66C1E0',
'602CE0',
'67D360',
'66F780',
'61F620',
'72BA40']

ScoreOffsets = [
'60C660',
'61A540',
'681AE0',
'63F240',
'5FAFE0',
'600CE0',
'658640',
'653600',
'613FC0',
'655A80',
'684040',
'636320',
'642720',
'6295E0',
'611C40',
'6675C0',
'673500',
'0',
'62B740',
'648480',
'63CD40',
'62FFC0',
'661900',
'60F8A0',
'626B00',
'63AAC0',
'5F7F60',
'623F20',
'64B640',
'65EA80',
'64E261',
'62DB80',
'65B900',
'650E80',
'676C00',
'6340C0',
'5FD780',
'608B00',
'616CC0',
'6387C0',
'67AD80',
'664900',
'645840',
'61DB80',
'632260',
'66DEA0',
'605520',
'67EE40',
'670FC0',
'620F60',
['72DCA0','730600','732C40','735600','7381C0']]

SongFileLengths = [
'1F50',
'1FA0',
'1360',
'1540',
'1AE0',
'2140',
'19C0',
'1480',
'1500',
'1380',
'17E0',
'10E0',
'18A0',
'16C0',
'1160',
'1760',
'1300',
'0',
'1040',
'1B20',
'1400',
'1460',
'1760',
'1920',
'16C0',
'FC0',
'1940',
'1740',
'1920',
'1C60',
'1220',
'11E0',
'1700',
'1AE0',
'20E0',
'11A0',
'1500',
'17C0',
'1E80',
'1780',
'20A0',
'1780',
'1660',
'1AE0',
'10C0',
'1CC0',
'2840',
'1AE0',
'1840',
'1940',
'2260']

ScoreFileLengths = [
'1920',
'1B60',
'D80',
'1C40',
'12A0',
'2000',
'1BC0',
'1100',
'E80',
'1260',
'19E0',
'D20',
'1AC0',
'1120',
'E80',
'1600',
'1620',
'0',
'1260',
'18A0',
'FC0',
'11E0',
'1880',
'1240',
'1420',
'E80',
'15A0',
'1520',
'1A00',
'1720',
'113F',
'FE0',
'1520',
'1300',
'20E0',
'1180',
'1420',
'1C00',
'18E0',
'1340',
'25E0',
'1560',
'1120',
'1AA0',
'C00',
'18E0',
'1E80',
'1940',
'1240',
'1880',
['2960','2640','29C0','2BC0','29A0']]

SongMemoryOffsets = [
'025a08a8',
'025a0c54',
'025a2780',
'025a1758',
'025a04fc',
'025a0674',
'025a1df4',
'025a1c7c',
'025a0adc',
'025a1d38',
'025a283c',
'025a1468',
'025a1814',
'025a1000', 
'025a0a20',
'025a21a0',
'025a2490',
'025a2318',
'025a10bc',
'025a198c',
'025a169c',
'025a1234',
'025a2028',
'025a0964',
'025a0f44',
'025a15e0',
'',
'025a0e88',
'025a1a48',
'025a1f6c',
'025a1b04',
'025a1178',
'025a1eb0',
'025a1bc0',
'025a254c',
'025a13ac',
'025a05b8',
'025a07ec',
'025a0b98',
'025a1524',
'025a2608',
'025a20e4',
'025a18d0',
'025a0d10',
'025a12f0',
'025a23d4',
'025a0730',
'025a26c4',
'025a23d4',
'025a0dcc',
['8059ACB3','8059ACD7','8059ACFB','8059AD1F']]

StyleNames = [
'Jazz',
'Rock',
'Latin',
'March',
'Electronic',
'Pop',
'Japanese',
'Tango',
'Classical',
'Hawaiian',
'Reggae',
'Twinkle Twinkle Little Star',
'Yankee Doodle',
'Oh My Darling Clementine',
'Scarborough Fair',
'Carmen',
'O Christmas Tree',
'Over The Waves',
'Every Breath You Take',
'Chariots of Fire',
'September',
'Material Girl',
'Ill Be There',
'Woman',
'Ive Never Been to Me',
'The Legend of Zelda',
'Wii Sports',
'Animal Crossing',
'Minuet in G Major',
'The Entertainer',
'Happy Birthday to You',
'La Cucaracha',
'From Santurtzi to Bilbao',
'A Little Night Music',
'The Blue Danube',
'Animal Crossing K.K. Blues',
'Wii Music',
'Super Mario Bros',
'Menu Style Main',
'Menu Style Electronic',
'Menu Style Japanese',
'Menu Style March']

StyleMemoryOffsets = [
'0659A65F',
'0659A683',
'0659A6A7',
'0659A6CB',
'0659A6EF',
'0659A713',
'0659A737',
'0659A75B',
'0659A77F',
'0659A7A3',
'0659A7C7',
'0659A7EB', #Default Styles
'0659A80F',
'0659A833',
'0659A856',
'0659A87B',
'0659A89F',
'0659A8C3',
'0659A8E7',
'0659A90B',
'0659A92F',
'0659A953',
'0659A977',
'0659A99B',
'0659A9BF',
'0659A9E3',
'0659AA07',
'0659AA2B',
'0659AA4F',
'0659AA73',
'0659AA97',
'0659AABB',
'0659AADF',
'0659AB03',
'0659AB27',
'0659AB4B',
'0659AB6F',
'8059AC8F',
'0659ACB3',
'0659ACD7',
'0659ACFB',
'0659AD1F'] 

InstrumentNames = [
'Piano',
'Marimba',
'Vibraphone',
'Steel Drum',
'Dulcimer',
'Handbell',
'Harpsichord',
'Timpani',
'Galactic Piano',
'Toy Piano',
'Dog',
'Cat',
'Rapper',
'Guitar',
'Electric Guitar',
'Electric Bass',
'Double Bass',
'Ukulele',
'Banjo',
'Sitar',
'Shamisen',
'Harp',
'Galactic Guitar',
'Galactic Bass',
'Jews Harp',
'Violin',
'Cello',
'Trumpet',
'Saxophone',
'Flute',
'Clairenet',
'Tuba',
'Accordion',
'Harmonica',
'Bagpipe',
'Recorder',
'Galactic horn',
'Nes',
'Singer',
'Another Singer',
'Basic Drums',
'Rock Drums',
'Jazz Drums',
'Latin Drums',
'Ballad Drums',
'Congas',
'Maracas',
'Tambourine',
'Cuica',
'Cowbell',
'Clap',
'Bells',
'Castanets',
'Guiro',
'Timpales',
'Djembe',
'Taiko Drum',
'Cheerleader',
'Snare Drum',
'Bass Drum',
'Galactic Drums',
'Galactic Congas',
'DJ Turntables',
'Kung Fu Person',
'Reggae Drums',
'Whistle',
'Beatbox']

MenuInstruments = [
'Saxophone',
'Violin',
'Shamisen',
'Flute',
'Clairenet',
'Piano',
'Vibraphone',
'Tuba',
'Electric bass',
'Galactic Guitar',
'Galactic Bass',
'Singer',
'Another Singer',
'Basic Drums',
'Snare Drum',
'DJ Turntables',
'Beatbox',
'Taiko Drum',
'Galactic Drums']


SongMemoryOrder = [
'Ode To Joy',
'Bridal Chorus',
'Swan Lake',
'Carmen',
'Wii Music',
'The Blue Danube',
'A Little Night Music',
'Minuet in G Major',
'Happy Birthday to You',
'Do-Re-Mi',
'The Entertainer',
'American Patrol',
'Turkey in the Straw',
'Yankee Doodle',
'Oh My Darling Clementine',
'My Grandfathers Clock',
'From the New World',
'La Bamba',
'Scarborough Fair',
'Long Long Ago',
'Twinkle Twinkle Little Star',
'Sur le Pont d Avignon',
'Frere Jacques',
'The Flea Waltz',
'O-Christmas Tree',
'Little Hans',
'Animal Crossing K.K. Blues',
'From Santurtzi to Bilbao',
'Troika',
'La Cucaracha',
'Over the Waves',
'Sakura Sakura',
'Sukiyaki',
'Daydream Believer',
'Every Breath You Take',
'Chariots of Fire',
'September',
'Please Mr. Postman',
'Material Girl',
'The Loco Motion',
'Ill Be There',
'Jingle Bell Rock',
'Wake Me Up Before You Go-Go',
'Woman',
'Ive Never Been to Me',
'Super Mario Bros',
'The Legend of Zelda',
'Wii Sports',
'Animal Crossing',
'F-Zero']

TextType = ['Song','Desc','Genre']
TextOffset = ['c8','190','12c']

#Functions
def AddPatch(PatchName,PatchInfo):
	global CodePath
	if(os.path.exists(CodePath)):
		codes = open(CodePath,'r')
		lineText = codes.readlines()
		codes.close()
		geckoExists = -1
		songExists = -1
		geckoEnabled = -1
		songEnabled = -1
		for num in range(len(lineText)):
			if(lineText[num].rstrip() == '[Gecko]'):
				geckoExists = num
			if(lineText[num].rstrip() == '$'+PatchName+' [WiiMusicEditor]'):
				songExists = num

		if(geckoExists == -1):
			lineText.insert(0,'[Gecko]\n'+'$'+PatchName+' [WiiMusicEditor]\n'+PatchInfo)
		elif(songExists == -1):
			lineText.insert(geckoExists+1,'$'+PatchName+' [WiiMusicEditor]\n'+PatchInfo)
		else:
			while True:
				if(len(lineText) <= songExists+1):
					break
				elif(not lineText[songExists+1][0].isnumeric()):
					break
				else:
					lineText.pop(songExists+1)
			lineText.insert(songExists+1,PatchInfo)
		
		for num in range(len(lineText)):
			if(lineText[num].rstrip() == '[Gecko_Enabled]'):
				geckoEnabled = num
			if(lineText[num].rstrip() == '$'+PatchName):
				songEnabled = num

		if(geckoEnabled == -1):
			lineText.insert(len(lineText),'[Gecko_Enabled]\n'+'$'+PatchName+'\n')
		elif(songEnabled == -1):
			lineText.insert(geckoEnabled+1,'$'+PatchName+'\n')
		
		codes = open(CodePath,'w')
		codes.writelines(lineText)
		codes.close()
	else:
		codes = open(CodePath,'w')
		codes.write('[Gecko]\n')
		codes.write('$'+PatchName+' [WiiMusicEditor]\n')
		codes.write(PatchInfo)
		codes.write('[Gecko_Enabled]\n')
		codes.write('$'+PatchName+'\n')
		codes.close()

def FindGameFolder():
	global GamePath
	global BrsarPath
	global MessagePath
	if(not os.path.isdir(GamePath+'/files')):
		while True:
			GamePath = input("\nDrag Decompressed Wii Music Directory: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
			if(os.path.isdir(GamePath+'/DATA/files')) or (os.path.isdir(GamePath+'/files')):
				if(os.path.isdir(GamePath+'/DATA')):
					GamePath = os.path.dirname(GamePath+'/DATA/files').replace('\\','/')
				else:
					GamePath = os.path.dirname(GamePath+'/files').replace('\\','/')
				SaveSetting('Paths','GamePath',GamePath)
				BrsarPath = GamePath+'/files/sound/MusicStatic/rp_Music_sound.brsar'
				MessagePath = GamePath+'/files/US/Message/message.carc'
				break
			else:
				print("\nERROR: Unable to Locate Valid Wii Music Directory")

def FindDolphin():
	global DolphinPath
	if(not os.path.isfile(DolphinPath)):
		while True:
			DolphinPath = input("\nDrag Dolphin.exe Over Window: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
			if(os.path.isfile(DolphinPath+'/dolphin.exe')):
				DolphinPath = DolphinPath.replace('\\','/')
				DolphinPath = DolphinPath+'/dolphin.exe'
				SaveSetting('Paths','DolphinPath',DolphinPath)
				break
			elif (os.path.isfile(DolphinPath)) and (DolphinPath[len(DolphinPath)-11:len(DolphinPath):1] == 'Dolphin.exe'):
				DolphinPath = DolphinPath.replace('\\','/')
				SaveSetting('Paths','DolphinPath',DolphinPath)
				break
			else:
				print("\nERROR: Unable to Locate Valid Dolphin Directory")

def InitializeBrseq():
	global BrseqPath
	global BrseqInfo
	global BrseqLength
	global ProgramPath
	global Tempo
	global MidiBeats
	global MidiBeatsString
	ExceptedSongExtensions = ['.midi','.mid','.brseq','.rseq']
	if(len(sys.argv) < 2):
		BrseqPath = ''
	else:
		BrseqPath = sys.argv[1]
	if(not os.path.isfile(BrseqPath)) or (not pathlib.Path(BrseqPath).suffix in ExceptedSongExtensions):
		while True:
			BrseqPath = input("\nDrag Song File Over Window [.midi, .mid, .brseq, .rseq] (Or Drag It On The .Bat File): ").replace('&', '').replace('\'', '').replace('\"', '').strip()
			if(os.path.isfile(BrseqPath)) and (pathlib.Path(BrseqPath).suffix in ExceptedSongExtensions):
				break
			else:
				print("\nERROR: Not A Valid File!")

	with tempfile.TemporaryDirectory() as directory:
		prefix = pathlib.Path(BrseqPath).suffix
		if(prefix == '.mid'): prefix = '.midi'
		copyfile(BrseqPath,directory+'/z'+prefix)
		if(os.path.isfile(directory+'/z.rseq')):
			subprocess.run('\"'+ProgramPath+'/Helper/SequenceCmd/GotaSequenceCmd.exe\" assemble \"'+directory+'/z.rseq\"')
		if(os.path.isfile(directory+'/z.brseq')):
			subprocess.run('\"'+ProgramPath+'/Helper/SequenceCmd/GotaSequenceCmd.exe\" to_midi \"'+directory+'/z.brseq\"')
		else:
			subprocess.run('\"'+ProgramPath+'/Helper/SequenceCmd/GotaSequenceCmd.exe\" from_midi \"'+directory+'/z.midi\"')
		mid = mido.MidiFile(directory+"/z.midi")
		Tempo = 'Could Not Locate'
		MidiBeats = 0
		for msg in mid.tracks[0]:
			if(msg.type == 'set_tempo'):
				Tempo = floor(mido.tempo2bpm(msg.tempo))
		MidiBeats = mid.length*Tempo/60
		MidiBeatsString = str(floor(MidiBeats))
		Tempo = str(Tempo)
		Brseq = open(directory+"/z.brseq","rb")
		Brseq.seek(0)
		BrseqInfo = Brseq.read()
		Brseq.close()
		BrseqLength = format(os.stat(directory+"/z.brseq").st_size,'x').upper()


def ChangeName(SongToChange,newText,TypeOfText):
	global ProgramPath
	subprocess.run('\"'+ProgramPath+'\\Helper\\Wiimms\\decode.bat\" '+MessageFolder(),capture_output=True)
	message = open(MessageFolder().replace('\"','')+'/message.d/new_music_message.txt','rb')
	textlines = message.readlines()
	message.close()
	offset = format(int(TextOffset[TextType.index(TypeOfText)],16)+SongMemoryOrder.index(SongNames[SongToChange]),'x').lower()
	offset = ' ' * (4-len(offset))+offset+'00 @'
	for num in range(len(textlines)):
		if offset in str(textlines[num]):
			while bytes('@','utf-8') not in textlines[num+1]:
				textlines.pop(num+1)
			textlines[num] = bytes(offset+str(textlines[num])[10:24:1]+newText+'\r\n','utf-8')
			break
	message = open(MessageFolder().replace('\"','')+'/message.d/new_music_message.txt','wb')
	message.writelines(textlines)
	message.close()
	subprocess.run('\"'+ProgramPath+'\\Helper\\Wiimms\\encode.bat\" '+MessageFolder(),capture_output=True)

def MessageFolder():
	return '\"'+(os.path.dirname(MessagePath)).replace('/','\\')+'\"'

def LoadSetting(section,key,default):
	ini = configparser.ConfigParser()
	ini.read('settings.ini')
	if(ini.has_option(section, key)):
		return ini[section][key]
	else:
		return default

def SaveSetting(section,key,value):
	ini = configparser.ConfigParser()
	ini.read('settings.ini')
	if(not ini.has_section(section)):
		ini.add_section(section)
	ini.set(section,key,value)
	print(str(ini))
	with open('settings.ini', 'w') as inifile:
		ini.write(inifile)

def PrintSectionTitle(Text):
	print("\n//////////////////// "+Text+":")

def CheckForUpdates():
	global ProgramPath
	print('Checking for Updates...')
	AutoUpdate.set_url(updateUrl[beta])
	AutoUpdate.set_download_link(updateDownload[beta])
	version = open(ProgramPath+'/Helper/Update/Version.txt')
	AutoUpdate.set_current_version(version.read())
	version.close()
	if not AutoUpdate.is_up_to_date():
		if(input("\nNew Update Avalible!\nWould you Like to Download it? [y/n] ") == 'y'):
			print('\nDownloading...')
			AutoUpdate.download('WiiMusicEditor.zip')
			print('\nExtracting...')
			subprocess.run('tar -xf WiiMusicEditor.zip')
			newPath = '/WiiMusicEditor-main'
			if(not os.path.isdir(ProgramPath+newPath)):
				newPath = '/WiiMusicEditor-beta'
			subprocess.Popen(ProgramPath+newPath+'/Helper/Update/Update.bat '+newPath.replace('/',''))
			quit()

	else:
		print('\nUp to Date!')

#Default Paths
GamePath = LoadSetting('Paths','GamePath','None')
BrsarPath = GamePath+'/files/sound/MusicStatic/rp_Music_sound.brsar'
MessagePath = GamePath+'/files/US/Message/message.carc'
CodePath = "C:/Users/"+getpass.getuser()+"/Documents/Dolphin Emulator/GameSettings/R64E01.ini"
SaveDataPath = "C:/Users/"+getpass.getuser()+"/Documents/Dolphin Emulator/Wii/title/00010000/52363445/data"
DolphinPath = LoadSetting('Paths','DolphinPath','None')
ProgramPath = os.path.dirname(__file__)

#Update
beta = True
uptodate = False
updateUrl = ['https://github.com/BenjaminHalko/WiiMusicEditor',
'https://github.com/BenjaminHalko/WiiMusicEditor/tree/beta']
updateDownload = ['https://github.com/BenjaminHalko/WiiMusicEditor/archive/refs/heads/main.zip',
'https://github.com/BenjaminHalko/WiiMusicEditor/archive/refs/heads/beta.zip']

#Main Loop
while True:
	#Options
	print("//////////////////////////////")
	print("//                          //")
	print("//        Welcome To        //")
	print("//         The Wii          //")
	print("//       Music Editor       //")
	print("//                          //")
	print("//////////////////////////////\n")
	if(not uptodate):
		CheckForUpdates()

	PrintSectionTitle('Options')
	print("(#1) Add Custom Song To Wii Music")
	print("(#2) Change Song Names")
	print("(#3) Change All Wii Music Text (Advanced)")
	print("(#4) Edit Styles")
	print("(#5) Overwrite Save File With 100% Save")
	print("(#6) Load Wii Music")
	print("(#7) Change File Paths")
	print("(#8) Credits")
	while True:
		mode = input("\nPlease Select An Option: ")
		if(mode == '1') or (mode == '2') or (mode == '3') or (mode == '4') or (mode == '5') or (mode == '6') or (mode == '7') or (mode == '8'):
			break
		else:
			print("\nERROR: Not a Valid Option!")

	if(mode == '1'):
		#Check For Brsar
		FindGameFolder()

		#Load Brseq
		InitializeBrseq()

		#Song Selection
		PrintSectionTitle('Song List')
		for num in range(len(SongNames)):
			if(num != 50):
				SongMinLength = min(int(SongFileLengths[num],16),int(ScoreFileLengths[num],16))
			else:
				SongMinLength = int(SongFileLengths[num],16)
			if(int(BrseqLength,16) > SongMinLength):
				print('~UNAVALIBLE~ '+str(SongNames[num])+' ('+format(SongMinLength,'x').upper()+')')
			else:
				print('(#'+str(num)+') '+str(SongNames[num])+' ('+format(SongMinLength,'x').upper()+')')
			time.sleep(0.005)

		#Brseq Info
		PrintSectionTitle("File Info")
		print("Number of Beats: "+MidiBeatsString)
		print("Tempo: "+Tempo)
		print("File Size: "+BrseqLength)

		#Song Selection
		PrintSectionTitle('Song Selection')
		while True:
			SongSelected = input("Enter The Song Number You Want To Replace: ")
			if(SongSelected.isnumeric()) and (int(SongSelected) < len(SongNames)):
				SongSelected = int(SongSelected)
				if(SongSelected != 50):
					minLength = min(int(SongFileLengths[SongSelected],16),int(ScoreFileLengths[SongSelected],16))
				else:
					minLength = int(SongFileLengths[SongSelected],16)
				if(int(BrseqLength,16) <= minLength):
					break
				else:
					print("ERROR: Brseq Filesize is over the maximum filesize for this song!\n")
			else:
				print("\nERROR: Not a Valid Number\n")

		#Length, Tempo, Time Signature Patch
		if(SongSelected != 50):
			PrintSectionTitle("Length, Tempo, Time Signature Patch")
			AutoFill = 'n'
			if(Tempo != 'Could Not Locate') or (MidiBeats != 0):
				MetaDataFound = ''
				if(MidiBeats != 0): MetaDataFound = 'Length'
				if(Tempo != 'Could Not Locate'):
					if(MetaDataFound == ''): MetaDataFound = 'Tempo'
					else: MetaDataFound = MetaDataFound+', Tempo'
				print('Meta Data Found: '+MetaDataFound)
				AutoFill = input("\nWe Have Automatically Located Some Meta Data! Would You Like To Autofill It: [y/n] ")
			
			if(AutoFill != 'y') or (MidiBeats == 0):
				while True:
					Length = input("\nHow Many Measures Does Your Song Have: ")
					if(Length.isnumeric()): 
						break
					else:
						print("\nERROR: Not a Valid Number\n")

			if(AutoFill != 'y') or (not Tempo.isnumeric()):
				while True:
					Tempo = input("\nWhat is the Tempo of Your Song: ")
					if(Tempo.isnumeric()):
						break
					else:
						print("\nERROR: Not a Valid Number")

			Tempo = format(int(Tempo),'x').upper()

			while True:
				TimeSignature = input("\nWhat Time Signature is Your Song? (4 = 4/4, 3 = 3/4): ")
				if(TimeSignature == '3') or (TimeSignature == '4'):
					break
				else:
					print("\nERROR: Please Press Ether 4 or 3")

			if(AutoFill == 'y') and (MidiBeats != 0):
				Length = str(round(MidiBeats/int(TimeSignature)))
			else:	
				Length = format(int(Length) * int(TimeSignature),'x').upper()

			#Final Writting
			LengthCode = '0'+format(int(SongMemoryOffsets[SongSelected],16)+6,'x').lower()+' '+'0'*(8-len(Length))+Length+'\n'
			TempoCode = '0'+format(int(SongMemoryOffsets[SongSelected],16)+10,'x').lower()+' '+'0'*(8-len(Tempo))+Tempo+'\n'
			TimeCode = SongMemoryOffsets[SongSelected]+' 00000'+TimeSignature+'00\n'

		if(input('\nAre You Sure You Want to Override '+SongNames[SongSelected]+'?\nYou Will NOT Be Able to Restore the Song Unless You Have Made a Backup! [y/n] ') == 'y'):
			#Brsar Writing
			brsar = open(BrsarPath, "r+b")
			brsar.seek(int(SongOffsets[SongSelected],16))
			brsar.write(bytes(int(SongFileLengths[SongSelected],16)))
			brsar.seek(int(SongOffsets[SongSelected],16))
			brsar.write(BrseqInfo)
			if(type(ScoreOffsets[SongSelected]) != str):
				for num in range(len(ScoreOffsets[SongSelected])):
					brsar.seek(int(ScoreOffsets[SongSelected][num],16))
					brsar.write(bytes(int(ScoreFileLengths[SongSelected][num],16)))
					brsar.seek(int(ScoreOffsets[SongSelected][num],16))
					brsar.write(BrseqInfo)
			else:
				brsar.seek(int(ScoreOffsets[SongSelected],16))
				brsar.write(bytes(int(ScoreFileLengths[SongSelected],16)))
				brsar.seek(int(ScoreOffsets[SongSelected],16))
				brsar.write(BrseqInfo)
			brsar.close()
			if(SongSelected != 50): AddPatch(SongNames[SongSelected]+' Song Patch',LengthCode+TempoCode+TimeCode)
			print("\nPatch Complete")
			time.sleep(0.5)
			if(SongSelected != 50) and (input('\nWould Like to Change the Song Text? [y/n] ') == 'y'):
				ChangeName(SongSelected,input('\nPlease Input the New Song Title: '),'Song')
				ChangeName(SongSelected,input('\nPlease Input the New Song Description: (Use \\n For New Line) '),'Desc')
				ChangeName(SongSelected,input('\nPlease Input the New Song Genre: '),'Genre')
				print("\nEditing Successful!\n")
			else: print('')
		else:
			print("Aborted...")
	elif(mode == '2'):
		FindGameFolder()
		#Song Selection
		PrintSectionTitle("Song List")
		for num in range(len(SongNames)):
			print('(#'+str(num)+') '+str(SongNames[num]))
			time.sleep(0.005)

		while True:
			PrintSectionTitle("Song Selection")
			SongSelected = input("\nWhich Song Do You Want To Change The Name Of: ")
			if(SongSelected.isnumeric()) and (int(SongSelected) < len(SongNames)):
				SongSelected = int(SongSelected)
				break
			else:
				print("\nERROR: Not a Valid Number")
		
		ChangeName(SongSelected,input('\nPlease Input the New Song Title: '),'Song')
		ChangeName(SongSelected,input('\nPlease Input the New Song Description: (Use \\n For New Line) '),'Desc')
		ChangeName(SongSelected,input('\nPlease Input the New Song Genre: '),'Genre')
		print("\nEditing Successful!\n")
	elif(mode == '3'):
		FindGameFolder()
		subprocess.run('\"'+os.path.dirname(__file__)+'/Helper/Wiimms/decode.bat\" '+MessageFolder(),capture_output=True)
		time.sleep(0.5)
		print("\nWaiting For User to Finish Editing and for Notepad to Close...")
		subprocess.run('notepad \"'+MessageFolder().replace('\"','')+'/message.d/new_music_message.txt\"',capture_output=True)
		subprocess.run('\"'+os.path.dirname(__file__)+'/Helper/Wiimms/encode.bat\" '+MessageFolder(),capture_output=True)
		print("\nEditing Successful!\n")
	elif(mode == '4'):
		PrintSectionTitle("Style List")
		for num in range(len(StyleNames)):
			print('(#'+str(num)+') '+str(StyleNames[num]))
			time.sleep(0.005)
		PrintSectionTitle("Style Selection")
		while True:
			StyleSelected = input("\nEnter The Style Number You Want To Replace: ")
			if(StyleSelected.isnumeric()) and (int(StyleSelected) < len(StyleNames)):
				StyleSelected = int(StyleSelected)
				break
			else:
				print("\nERROR: Not a Valid Number")
		PrintSectionTitle("Intrument List")
		for num in range(40):
			if(StyleSelected < len(StyleNames)-4) or (InstrumentNames[num] in MenuInstruments):
				print('(#'+str(num)+') '+str(InstrumentNames[num]))
			else:
				print('(UNAVALIBLE) '+str(InstrumentNames[num]))
			time.sleep(0.005)
		PrintSectionTitle("Instrument Selection")
		while True:
			Melody = input("Enter The Instrument Number You Want For Melody: ")
			if(Melody.isnumeric()) and (int(Melody) < 40) and ((StyleSelected < len(StyleNames)-4) or (InstrumentNames[int(Melody)] in MenuInstruments)):
				Melody = format(int(Melody),'x').upper()
				Melody = '0'*(2-len(Melody))+Melody
				break
			else:
				print("\nERROR: Not a Valid Number\n")
		while True:
			Harmony = input("\nEnter The Instrument Number You Want For Harmony: ")
			if(Harmony.isnumeric()) and (int(Harmony) < 40) and ((StyleSelected < len(StyleNames)-4) or (InstrumentNames[int(Harmony)] in MenuInstruments)):
				Harmony = format(int(Harmony),'x').upper()
				Harmony = '0'*(2-len(Harmony))+Harmony
				break
			else:
				print("\nERROR: Not a Valid Number")
		while True:
			Chord = input("\nEnter The Instrument Number You Want For Chord: ")
			if(Chord.isnumeric()) and (int(Chord) < 40) and ((StyleSelected < len(StyleNames)-4) or (InstrumentNames[int(Chord)] in MenuInstruments)):
				Chord = format(int(Chord),'x').upper()
				Chord = '0'*(2-len(Chord))+Chord
				break
			else:
				print("\nERROR: Not a Valid Number")
		while True:
			Bass = input("\nEnter The Instrument Number You Want For Bass: ")
			if(Bass.isnumeric()) and (int(Bass) < 40) and ((StyleSelected < len(StyleNames)-4) or (InstrumentNames[int(Bass)] in MenuInstruments)):
				Bass = format(int(Bass),'x').upper()
				Bass = '0'*(2-len(Bass))+Bass
				break
			else:
				print("\nERROR: Not a Valid Number")
		PrintSectionTitle("Intrument List")
		for num in range(40,len(InstrumentNames)):
			if(StyleSelected < len(StyleNames)-4) or (InstrumentNames[num] in MenuInstruments):
				print('(#'+str(num-40)+') '+str(InstrumentNames[num]))
			else:
				print('(UNAVALIBLE) '+str(InstrumentNames[num]))
			time.sleep(0.005)
		while True:
			Perc1 = input("\nEnter The Instrument Number You Want For Percussion 1: ")
			if(Perc1.isnumeric()) and (int(Perc1) < len(InstrumentNames)-40) and ((StyleSelected < len(StyleNames)-4) or (InstrumentNames[int(Perc1)+40] in MenuInstruments)):
				Perc1 = format(int(Perc1)+40,'x').upper()
				Perc1 = '0'*(2-len(Perc1))+Perc1
				break
			else:
				print("\nERROR: Not a Valid Number")
		while True:
			Perc2 = input("\nEnter The Instrument Number You Want For Percussion 2: ")
			if(Perc2.isnumeric()) and (int(Perc2) < len(InstrumentNames)-40) and ((StyleSelected < len(StyleNames)-4) or (InstrumentNames[int(Perc2)+40] in MenuInstruments)):
				Perc2 = format(int(Perc2)+40,'x').upper()
				Perc2 = '0'*(2-len(Perc2))+Perc2
				break
			else:
				print("\nERROR: Not a Valid Number")

		AddPatch(StyleNames[StyleSelected]+' Style Patch',StyleMemoryOffsets[StyleSelected]+' 00000018\n'+Melody+'000000 '+Harmony+'000000\n'+Chord+'000000 '+Bass+'000000\n'+Perc1+'000000 '+Perc2+'000000\n')
		print("\nPatch Complete")
		time.sleep(0.5)
		print("")
	elif(mode == '5'):
		if(input("\nAre You Sure You Want To Overwrite Your Save Data? [y/n] ") == 'y'):
			subprocess.run('robocopy \"'+ProgramPath+'/Helper/WiiMusicSave\" \"'+SaveDataPath+'\" /MIR /E',capture_output=True)
			print("\nOverwrite Successfull\n")
		else:
			print("\nAborted...\n")
	elif(mode == '6'):
		FindGameFolder()
		FindDolphin()
		PrintSectionTitle("Running Dolphin")
		subprocess.run('\"'+DolphinPath+'\" -e \"'+GamePath+'/sys/main.dol\"',capture_output=True)
		print("")
	elif(mode == '7'):
		PrintSectionTitle("Path Editor")
		print("(#0) Back To Main Menu")
		print("(#1) Game Path (Current Path: "+GamePath+')')
		print("(#2) Dolphin Path (Current Path: "+DolphinPath+')')
		while True:
			PathSelected = input("\nWhich Path Do You Want To Change: ")
			if(PathSelected.isnumeric()) and (int(PathSelected) < 3):
				PathSelected = int(PathSelected)
				break
			else:
				print("\nERROR: Not a Valid Number")
		if(PathSelected == 1):
			GamePath = ''
			FindGameFolder()
			print("")
		elif(PathSelected == 2):
			DolphinPath = ''
			FindDolphin()
			print("")
	elif(mode == '8'):
		PrintSectionTitle('Credits')
		print('\n-----Created By:-----')
		print('- Benjamin Halko')
		print('\n-----Tested By:-----')
		print('- FasterHumans')
		print('- RainbowKappa')
		print('\n-----Song File Offsets Discovered By:-----')
		print('- JimmyKaz')
		print('\n-----Song Memory Offsets Discovered By:-----')
		print('- Checker Mii Out Channel')
		print('\n-----Brsar Conversion Made Possible By:-----')
		print('- GotaSequenceCmd')
		print('\n-----Text Extraction Made Possible By:-----')
		print('- WiiMMS')
		input('')