import os
import sys
import getpass
import time
import subprocess
import configparser
import pathlib
import tempfile
from shutil import copyfile, rmtree
from math import floor, ceil
import webbrowser

#Special Imports
while True:
	try:
		import requests
		import mido
		from colorama import Fore, Style, init
		from tqdm import tqdm
		from selenium import webdriver
		break
	except ImportError:
		subprocess.run('python -m pip install --upgrade pip')
		subprocess.run('pip install mido requests colorama tqdm selenium')

init(convert=True)

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
'0', #1940
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
'0']

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
'025a23d4',
'025a0730',
'025a26c4',
'025a23d4',
'025a0dcc',
['8059ACB3','8059ACD7','8059ACFB','8059AD1F']]

StyleNames = [
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
'Menu Style Main',
'Menu Style Electronic',
'Menu Style Japanese',
'Menu Style March',
'Replace All Normal Styles',
'Replace All Menu Styles']

StyleMemoryOffsets = [
'0659A7E8',
'0659A80C',
'0659A830',
'0659A854',
'0659A878',
'0659A89C',
'0659A8C0',
'0659A8E4',
'0659A908',
'0659A92C',
'0659A950',
'0659A974',
'0659A998',
'0659A9BC',
'0659A9E0',
'0659AA04',
'0659AA28',
'0659AA4C',
'0659AA70',
'0659AA94',
'0659AAB8',
'0659AADC',
'0659AB00',
'0659AB24',
'0659AB48',
'0659AB6C',
'0659AC8C',
'0659A65C',
'0659A680',
'0659A6A4',
'0659A6C8',
'0659A6EC',
'0659A710',
'0659A724',
'0659A758',
'0659A77C',
'0659A7A0',
'0659A7C4',
'0659ACB0',
'0659ACD4',
'0659ACF8',
'0659AD1C']

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
'Beatbox',
'None']

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
'Rock Drums',
'Latin Drums',
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

#Functions
def AddPatch(PatchName,PatchInfo):
	global GamePath
	global CodePath
	global DefaultStyleMethod
	global ProgramPath
	if(type(PatchName) == str):
		PatchName = [PatchName]
		PatchInfo = [PatchInfo]
	for patchNum in range(len(PatchName)):
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
				if(lineText[num].rstrip() == '$'+PatchName[patchNum]+' [WiiMusicEditor]'):
					songExists = num

			if(geckoExists == -1):
				lineText.insert(0,'[Gecko]\n'+'$'+PatchName[patchNum]+' [WiiMusicEditor]\n'+PatchInfo[patchNum])
			elif(songExists == -1):
				lineText.insert(geckoExists+1,'$'+PatchName[patchNum]+' [WiiMusicEditor]\n'+PatchInfo[patchNum])
			else:
				while True:
					if(len(lineText) <= songExists+1):
						break
					elif(not lineText[songExists+1][0].isnumeric() and (lineText[songExists+1][0] != 'f')):
						break
					else:
						lineText.pop(songExists+1)
				lineText.insert(songExists+1,PatchInfo[patchNum])
			
			for num in range(len(lineText)):
				if(lineText[num].rstrip() == '[Gecko_Enabled]'):
					geckoEnabled = num
				if(lineText[num].rstrip() == '$'+PatchName[patchNum]):
					songEnabled = num

			if(geckoEnabled == -1):
				lineText.insert(len(lineText),'[Gecko_Enabled]\n'+'$'+PatchName[patchNum]+'\n')
			elif(songEnabled == -1):
				lineText.insert(geckoEnabled+1,'$'+PatchName[patchNum]+'\n')
			
			codes = open(CodePath,'w')
			codes.writelines(lineText)
			codes.close()
		else:
			codes = open(CodePath,'w')
			codes.write('[Gecko]\n')
			codes.write('$'+PatchName[patchNum]+' [WiiMusicEditor]\n')
			codes.write(PatchInfo[patchNum])
			codes.write('[Gecko_Enabled]\n')
			codes.write('$'+PatchName[patchNum]+'\n')
			codes.close()

def FindGameFolder():
	global GamePath
	global BrsarPath
	global MessagePath
	global WiiDiskFolder
	if(not os.path.isdir(GamePath+'/files')):
		ExceptedFileExtensions = ['.iso','.wbfs']
		while True:
			GamePath = input("\nDrag the Decompressed Wii Music Directory or a Wii Music Disk on to the Window: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
			if(os.path.isdir(GamePath+'/DATA/files')) or (os.path.isdir(GamePath+'/files')):
				if(os.path.isdir(GamePath+'/DATA')):
					GamePath = os.path.dirname(GamePath+'/DATA/files').replace('\\','/')
				else:
					GamePath = os.path.dirname(GamePath+'/files').replace('\\','/')
				SaveSetting('Paths','GamePath',GamePath)
				BrsarPath = GamePath+'/files/sound/MusicStatic/rp_Music_sound.brsar'
				MessagePath = GamePath+'/files/US/Message/message.carc'
				FindWiiDiskFolder()
				break
			elif(os.path.isfile(GamePath)) and (pathlib.Path(GamePath).suffix in ExceptedFileExtensions):
				subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/extractdisk.bat\" \"'+os.path.dirname(GamePath)+'\" \"'+os.path.splitext(os.path.basename(GamePath))[0]+'\" '+os.path.splitext(os.path.basename(GamePath))[1])
				GamePath = os.path.dirname(GamePath).replace('\\','/')+'/'+os.path.splitext(os.path.basename(GamePath))[0]+'/DATA'
				SaveSetting('Paths','GamePath',GamePath)
				BrsarPath = GamePath+'/files/sound/MusicStatic/rp_Music_sound.brsar'
				MessagePath = GamePath+'/files/US/Message/message.carc'
				FindWiiDiskFolder()
				break
			else:
				print("\nERROR: Unable to Locate Valid Wii Music Directory")

def FindWiiDiskFolder():
	global GamePath
	global WiiDiskFolder
	WiiDiskFolder = os.path.basename(GamePath)
	if(WiiDiskFolder == 'DATA') and (os.path.isdir(GamePath)):
		LastSlash = len(GamePath)-1
		while(LastSlash >= 0) and (GamePath[LastSlash].isalpha()):
			LastSlash -= 1
		WiiDiskFolder = os.path.basename(GamePath[0:LastSlash:1])

def FindDolphin():
	global DolphinPath
	global DolphinSaveData
	global CodePath
	global SaveDataPath
	if(not os.path.isfile(DolphinPath)):
		while True:
			DolphinPath = input("\nDrag Dolphin.exe or the Dolphin Folder on to the Window: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
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
		if(os.path.isfile(DolphinPath[0:len(DolphinPath)-11:1]+'portable.txt')):
			print('\nPortable Version Detected!')
			if(input('Do You Want to Set the Dolphin Save Directory to the User Folder? [y/n] ') == 'y'):
				DolphinSaveData = DolphinPath[0:len(DolphinPath)-11:1]+'User'
				if(not os.path.isdir(DolphinSaveData)): os.mkdir(DolphinSaveData)
				if(not os.path.isdir(DolphinSaveData+'/Wii')): os.mkdir(DolphinSaveData+'/Wii')
				CodePath = DolphinSaveData+"/GameSettings/R64E01.ini"
				SaveDataPath = DolphinSaveData+"/Wii/title/00010000/52363445/data"
				SaveSetting('Paths','DolphinSaveData',DolphinSaveData)

def FindDolphinSave():
	global DolphinSaveData
	global CodePath
	global SaveDataPath
	if(not os.path.isdir(DolphinSaveData+'/Wii')):
		while True:
			DolphinSaveData = input("\nDrag the Dolphin Save Directory Over the Window: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
			if(os.path.isdir(DolphinSaveData+'/Wii')):
				DolphinSaveData = DolphinSaveData.replace('\\','/')
				CodePath = DolphinSaveData+"/GameSettings/R64E01.ini"
				SaveDataPath = DolphinSaveData+"/Wii/title/00010000/52363445/data"
				SaveSetting('Paths','DolphinSaveData',DolphinSaveData)
				break
			else:
				print("\nERROR: Unable to Locate Valid Dolphin Save Directory")

def InitializeBrseq():
	global BrseqPath
	global BrseqInfo
	global BrseqLength
	global ProgramPath
	global Tempo
	global Length
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
		Length = 0
		for msg in mid.tracks[0]:
			if(msg.type == 'set_tempo'):
				Tempo = floor(mido.tempo2bpm(msg.tempo))
		Length = str(ceil(mid.length*Tempo/60))
		Tempo = str(Tempo)
		Brseq = open(directory+"/z.brseq","rb")
		Brseq.seek(0)
		BrseqInfo = Brseq.read()
		Brseq.close()
		BrseqLength = format(os.stat(directory+"/z.brseq").st_size,'x').upper()


def ChangeName(SongToChange,newText):
	global ProgramPath
	TextOffset = ['c8','190','12c']
	subprocess.run('Helper/Wiimms/decode.bat '+MessageFolder(),capture_output=True)
	for typeNum in range(3):
		message = open(MessageFolder().replace('\"','')+'/message.d/new_music_message.txt','rb')
		textlines = message.readlines()
		message.close()
		offset = format(int(TextOffset[typeNum],16)+SongMemoryOrder.index(SongNames[SongToChange]),'x').lower()
		offset = ' ' * (4-len(offset))+offset+'00 @'
		for num in range(len(textlines)):
			if offset in str(textlines[num]):
				while bytes('@','utf-8') not in textlines[num+1]:
					textlines.pop(num+1)
				textlines[num] = bytes(offset+str(textlines[num])[10:24:1]+newText[typeNum]+'\r\n','utf-8')
				break
		message = open(MessageFolder().replace('\"','')+'/message.d/new_music_message.txt','wb')
		message.writelines(textlines)
		message.close()
	subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/encode.bat\" '+MessageFolder(),capture_output=True)

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

def CheckForUpdates(PrintMessages):
	global ProgramPath
	global beta
	global updateUrl
	if(PrintMessages): print('Checking for Updates...')
	version = open(ProgramPath+'/Helper/Update/Version.txt')
	currentVersion = version.read()
	version.close()
	try:
		newVersion = requests.get(updateUrl[beta])
		if (newVersion.text != currentVersion):
			if(input("\nNew Update Avalible!\nWould you Like to Download it? [y/n] ") == 'y'):
				DownloadUpdate()
		else:
			if(PrintMessages): print('\nUp to Date!')
	except (requests.ConnectionError, requests.Timeout) as exception:
		if(PrintMessages): print('\nFailed to Find Updates...')

def DownloadUpdate():
	global beta
	global updateDownload
	global ProgramPath
	print('\nDownloading...')
	try:
		response = requests.get(updateDownload[beta], stream=True)
		total_size_in_bytes= int(response.headers.get('content-length', 0))
		block_size = 1024
		progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
		with open('WiiMusicEditor.zip', 'wb') as file:
			for data in response.iter_content(block_size):
				progress_bar.update(len(data))
				file.write(data)
		progress_bar.close()
		if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
			print("\nERROR, something went wrong\n")
			return True
		else:
			print('\nExtracting...\n')
			subprocess.run('tar -xf WiiMusicEditor.zip')
			newPath = 'WiiMusicEditor-main'
			if(not os.path.isdir(newPath)):
				newPath = 'WiiMusicEditor-beta'
			os.rename(newPath, 'WiiMusicEditorNew')
			if(os.path.isfile(ProgramPath+'/WiiMusicEditorNew/.gitignore')): os.remove(ProgramPath+'/WiiMusicEditorNew/.gitignore')
			subprocess.run(ProgramPath+'/WiiMusicEditorNew/Helper/Update/Update.bat')
			quit()
			return False
	except (requests.ConnectionError, requests.Timeout) as exception:
		print('\nFailed to Download File...\n')
		return True

def SelectStyleInstrument(PartString,IsPercussion):
	global StyleNames
	global Selection
	global InstrumentNames
	global MenuInstruments
	global normalInstrumentNumber
	global unsafeMode
	global NormalStyleSelected
	print('')
	while True:
		PartType = input("Enter The Instrument Number You Want For "+PartString+": ")
		if(PartType.isnumeric()):
			PartType = int(PartType)
			if(IsPercussion) and (not unsafeMode): PartType = PartType + normalInstrumentNumber
			if(unsafeMode):
				if(PartType == len(InstrumentNames)-1):
					PartType = 'ffffffff'
					break
				elif (PartType < len(InstrumentNames)):
					PartType = format(PartType,'x').upper()
					PartType = '0'*(8-len(PartType))+PartType
					break
				else:
					print("\nERROR: Not a Valid Number\n")
			elif((PartType == normalInstrumentNumber and not IsPercussion) or (PartType == len(InstrumentNames)-1 and IsPercussion)) and (NormalStyleSelected):
				PartType = 'ffffffff'
				break
			elif((PartType < normalInstrumentNumber) != IsPercussion) and (PartType < len(InstrumentNames)) and ((NormalStyleSelected) or (InstrumentNames[PartType] in MenuInstruments)):
				PartType = format(PartType,'x').upper()
				PartType = '0'*(8-len(PartType))+PartType
				break
			else:
				print("\nERROR: Not a Valid Number\n")
		else:
			print("\nERROR: Not a Valid Number\n")
	return PartType

def MakeSelection(MessageRangeArray):
	while True:
		TempSelection = input("\n"+MessageRangeArray[0]+": ")
		if(TempSelection.isnumeric()) and ((len(MessageRangeArray) <= 1) or ((int(TempSelection) <= MessageRangeArray[2]) and (int(TempSelection) >= MessageRangeArray[1]))):
			break
		else:
			print("\nERROR: Not a Valid Number")
	return int(TempSelection)

def ChangeDefaultAnswer(ResponseOptions,iniKey):
	if(len(ResponseOptions) == 2):
		if(ResponseOptions.index(iniKey[1]) == 0): Selection = 1
		else: Selection = 0
	else:
		for num in range(len(ResponseOptions)):
			print('(#'+str(num)+') '+ResponseOptions[num])

		Selection = MakeSelection(['Select an Option',0,len(ResponseOptions)-1])
	SaveSetting('Default Answers', iniKey[0], ResponseOptions[Selection])
	print('')
	return ResponseOptions[Selection]

def CreateGct():
	global CodePath
	global ProgramPath
	if(os.path.isfile('R64E01.gct')): os.remove('R64E01.gct')
	patches = open(CodePath)
	textlines = patches.readlines()
	patches.close()
	codes = ''
	for text in textlines:
		if(text[0].isalpha() or text[0].isnumeric()):
			codes = codes + text
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"download.default_directory" : ProgramPath.replace('/','\\')}
	chromeOptions.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome('Helper/GctFiles/chromedriver.exe',options=chromeOptions)
	driver.get('https://mkwii.com/gct/')
	driver.find_element_by_id('game_id').send_keys("R64E01")
	driver.find_element_by_id('code_title').send_keys("Code List")
	driver.find_element_by_id('code').send_keys(codes)
	driver.find_element_by_id('add_code_b').click()
	driver.find_element_by_id('gct_b').click()
	time.sleep(1)
	driver.quit()

#Default Paths
ProgramPath = os.path.dirname(__file__).replace('\\','/')
os.chdir(ProgramPath)
GamePath = LoadSetting('Paths','GamePath','None')
BrsarPath = GamePath+'/files/sound/MusicStatic/rp_Music_sound.brsar'
MessagePath = GamePath+'/files/US/Message/message.carc'
DolphinSaveData = LoadSetting('Paths','DolphinSaveData',"C:/Users/"+getpass.getuser()+"/Documents/Dolphin Emulator")
CodePath = DolphinSaveData+"/GameSettings/R64E01.ini"
SaveDataPath = DolphinSaveData+"/Wii/title/00010000/52363445/data"
DolphinPath = LoadSetting('Paths','DolphinPath','None')
WiiDiskFolder = ''
FindWiiDiskFolder()

#Update
beta = int(LoadSetting('Updates', 'Branch', '0'))
AutoUpdate = bool(int(LoadSetting('Updates', 'AutoUpdate', '1')))
uptodate = False
updateUrl = ['https://raw.githubusercontent.com/BenjaminHalko/WiiMusicEditor/main/Helper/Update/Version.txt',
'https://raw.githubusercontent.com/BenjaminHalko/WiiMusicEditor/beta/Helper/Update/Version.txt']
updateDownload = ['https://github.com/BenjaminHalko/WiiMusicEditor/archive/refs/heads/main.zip',
'https://github.com/BenjaminHalko/WiiMusicEditor/archive/refs/heads/beta.zip']

#Default Answers
DefaultWantToReplaceSong = LoadSetting('Default Answers', 'Want To Replace Song', 'Yes')
DefaultReplacingReplacedSong = LoadSetting('Default Answers', 'Replacing Replaced Song', 'Yes')
DefaultReplaceSongNames = LoadSetting('Default Answers', 'Replace Song Names', 'Ask')
DefaultUseAutoLengthTempo = LoadSetting('Default Answers', 'Use Auto Length and Tempo', 'Ask')

#Unsafe Mode
unsafeMode = bool(int(LoadSetting('Unsafe Mode','Unsafe Mode','0')))

#Main Loop
while True:
	#Find Branch
	if(os.path.exists('settings.ini')):
		if(os.path.exists('README.md')):
			readme = open('README.md')
			if('Beta' in readme.read()):
				beta = 1
				SaveSetting('Updates', 'Branch', '1')
			else:
				beta = 0
				SaveSetting('Updates', 'Branch', '0')
			readme.close()
	#Finish Updates
	if(not uptodate):
		if(os.path.isdir('WiiMusicEditorNew') or os.path.isfile('WiiMusicEditor.zip')):
			print('Finishing Up...\n')
			if(os.path.isdir('WiiMusicEditorNew')): rmtree('WiiMusicEditorNew')
			if(os.path.isfile('WiiMusicEditor.zip')): os.remove('WiiMusicEditor.zip')
			uptodate = True

	#Title
	print("//////////////////////////////")
	print("//                          //")
	print("//        Welcome To        //")
	print("//         The Wii          //")
	print("//       Music Editor       //")
	print("//                          //")
	print("//////////////////////////////\n")
	
	#Updates
	if(AutoUpdate) and (not uptodate):
		uptodate = True
		CheckForUpdates(False)

	#First Run
	if(GamePath == 'None'):
		print('\nThanks for Downloading the Wii Music Editor!')
		print('\nLet\'s Setup Some File Paths for You!')
		FindGameFolder()
		if(input('\nWould You Like to Specify a Dolphin Directory? [y/n] ') == 'y'):
			FindDolphin()

	#Options
	PrintSectionTitle('Options')
	print("(#1) Add Custom Song To Wii Music")
	print("(#2) Change Song Names")
	print("(#3) Edit Styles")
	print("(#4) Advanced Tools")
	print("(#5) Load Wii Music")
	print("(#6) Overwrite Save File With 100% Save")
	print("(#7) Download Pre-Made Custom Songs")
	print("(#8) Help")
	print("(#9) Settings")
	print("(#10) Credits")

	Selection = MakeSelection(['Please Select an Option',1,10])

	if(Selection == 1): #////////////////////////////////////////Add Custom Song
		#Load Files
		FindGameFolder()
		FindDolphinSave()
		InitializeBrseq()

		#Applied Custom Songs
		appliedCustomSongs = list(LoadSetting('Applied Custom Songs', WiiDiskFolder, '').split(','))

		#Song List
		LowestSong = -1
		PrintSectionTitle('Song List')
		SongMinLength = []
		for num in range(len(SongNames)):
			if(num != 50):
				SongMinLength.append(min(int(SongFileLengths[num],16),int(ScoreFileLengths[num],16)))
			else:
				SongMinLength.append(int(SongFileLengths[num],16))
			if(int(BrseqLength,16) <= SongMinLength[num]) and (SongNames[num] not in appliedCustomSongs):
				if(LowestSong == -1): LowestSong = SongMinLength[num]
				else: LowestSong = min(SongMinLength[num],LowestSong)

		for num in range(len(SongNames)):
			if(int(BrseqLength,16) > SongMinLength[num]):
				print(Fore.RED+'~unavalible~ '+str(SongNames[num])+' ('+format(SongMinLength[num],'x').upper()+')'+Style.RESET_ALL)
			elif(SongNames[num] in appliedCustomSongs):
				print(Fore.YELLOW+'(#'+str(num)+') '+str(SongNames[num])+' ('+format(SongMinLength[num],'x').upper()+') ~[Already Replaced]~'+Style.RESET_ALL)
			elif (SongMinLength[num] == LowestSong):
				print(Fore.GREEN+'(#'+str(num)+') '+str(SongNames[num])+' ('+format(SongMinLength[num],'x').upper()+') ~[Smallest Song Avalible]~'+Style.RESET_ALL)
			else:
				print(Style.RESET_ALL+'(#'+str(num)+') '+str(SongNames[num])+' ('+format(SongMinLength[num],'x').upper()+')')
			time.sleep(0.005)

		#Brseq Info
		PrintSectionTitle("File Info")
		print("Number of Beats: "+Length)
		print("Tempo: "+Tempo)
		print("File Size: "+BrseqLength)

		#Song Selection
		PrintSectionTitle('Song Selection')
		while True:
			SongSelected = input("Enter The Song Number You Want To Replace: ")
			if(SongSelected.isnumeric()) and (int(SongSelected) < len(SongNames)):
				SongSelected = int(SongSelected)
				if(int(BrseqLength,16) <= SongMinLength[SongSelected]):
					if(SongNames[SongSelected] not in appliedCustomSongs) or (DefaultReplacingReplacedSong == 'No') or (input('\nWARNING: You Have Already Replaced this Song Before! Are You Sure You Want to Replace this Song?\n(If you Want to Reset the Replaced Song Database, go to the Settings Menu.) [y/n] ') == 'y'):
						break
					else:
						print('Aborted...\n')
				else:
					print("ERROR: Brseq Filesize is over the maximum filesize for this song!\n")
			else:
				print("\nERROR: Not a Valid Number\n")

		#Length, Tempo, Time Signature Patch
		if(SongSelected != 50):
			PrintSectionTitle("Length, Tempo, Time Signature Patch")
			AutoFill = 'n'
			if((Tempo != 'Could Not Locate') or (Length != '0')) and (DefaultUseAutoLengthTempo != 'No'):
				MetaDataFound = ''
				if(Length != '0'): MetaDataFound = 'Length'
				if(Tempo != 'Could Not Locate'):
					if(MetaDataFound == ''): MetaDataFound = 'Tempo'
					else: MetaDataFound = MetaDataFound+', Tempo'
				print('Meta Data Found: '+MetaDataFound)
				if(DefaultUseAutoLengthTempo == 'Yes'):
					AutoFill = 'y'
				else:
					AutoFill = input("\nWe Have Automatically Located Some Meta Data! Would You Like To Autofill It: [y/n] ")
			
			if(AutoFill != 'y') or (Length == '0'):
				Length = MakeSelection(['\nHow Many Measures in Your Song'])
			else:
				Length = format(int(Length),'x').upper()

			if(AutoFill != 'y') or (not Tempo.isnumeric()):
				Tempo = MakeSelection(['What is the Tempo of Your Song'])

			Tempo = format(int(Tempo),'x').upper()

			while True:
				TimeSignature = input("\nWhat Time Signature is Your Song? (4 = 4/4, 3 = 3/4): ")
				if(TimeSignature == '3') or (TimeSignature == '4'):
					break
				else:
					print("\nERROR: Please Press Ether 4 or 3")

			if(AutoFill != 'y') or (Length == 0):
				Length = format(int(Length) * int(TimeSignature),'x').upper()

			#Final Writting
			LengthCode = '0'+format(int(SongMemoryOffsets[SongSelected],16)+6,'x').lower()+' '+'0'*(8-len(Length))+Length+'\n'
			TempoCode = '0'+format(int(SongMemoryOffsets[SongSelected],16)+10,'x').lower()+' '+'0'*(8-len(Tempo))+Tempo+'\n'
			TimeCode = SongMemoryOffsets[SongSelected]+' 00000'+TimeSignature+'00\n'

		if(DefaultWantToReplaceSong == 'No') or (input('\nAre You Sure You Want to Override '+SongNames[SongSelected]+'?\nYou Will NOT Be Able to Restore the Song Unless You Have Made a Backup! [y/n] ') == 'y'):
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
			if(SongNames[SongSelected] not in appliedCustomSongs):
				if(appliedCustomSongs[0] == ''):
					appliedCustomSongs = [SongNames[SongSelected]]
				else:
					appliedCustomSongs.append(SongNames[SongSelected])
				SaveSetting('Applied Custom Songs', WiiDiskFolder, ','.join([str(elem) for elem in appliedCustomSongs]))
			print("\nPatch Complete")
			time.sleep(0.5)
			if(DefaultReplaceSongNames != 'No') and (SongSelected != 50) and ((DefaultReplaceSongNames == 'Yes') or (input('\nWould Like to Change the Song Text? [y/n] ') == 'y')):
				ChangeName(SongSelected,[input('\nPlease Input the New Song Title: '),input('\nPlease Input the New Song Description: (Use \\n For New Line) '),input('\nPlease Input the New Song Genre: ')])
				print("\nEditing Successful!\n")
			else: print('')
		else:
			print("Aborted...")
	elif(Selection == 2): #////////////////////////////////////////Change Song Names
		#Load Files
		FindGameFolder()

		#Song List
		PrintSectionTitle("Song List")
		for num in range(len(SongNames)):
			print('(#'+str(num)+') '+str(SongNames[num]))
			time.sleep(0.005)

		#Song Selection
		PrintSectionTitle("Song Selection")
		Selection = MakeSelection(['\nWhich Song Do You Want To Change The Name Of',0,len(SongNames)-1])
		
		ChangeName(Selection,[input('\nPlease Input the New Song Title: '),input('\nPlease Input the New Song Description: (Use \\n For New Line) '),input('\nPlease Input the New Song Genre: ')])
		print("\nEditing Successful!\n")
	elif(Selection == 3): #////////////////////////////////////////Change Style
		PrintSectionTitle("Style List")
		FindDolphinSave()
		SongStyles = 27
		NormalStyleNumber = 11
		MenuStyles = 4
		for num in range(len(StyleNames)):
			if(num == 0):
				print('\n//////////Song Specific Styles\n')
			elif(num == SongStyles):
				print('\n//////////Normal Styles\n')
			elif(num == NormalStyleNumber+SongStyles):
				print('\n//////////Menu Styles\n')
			elif(num == NormalStyleNumber+SongStyles+MenuStyles):
				print('\n//////////Replace All Styles\n')
			print('(#'+str(num)+') '+str(StyleNames[num]))
			time.sleep(0.005)
		Selection = MakeSelection(['\nEnter the Style Number You Want to Change',0,len(StyleNames)])
		NormalStyleSelected = (Selection < len(StyleNames)-6) or (Selection == len(StyleNames)-2)
		PrintSectionTitle("Instrument List")
		normalInstrumentNumber = 40
		
		if(not unsafeMode):
			for num in range(normalInstrumentNumber+1):
				realNum = num
				if(num == normalInstrumentNumber):
					num = len(InstrumentNames)-1
				if (InstrumentNames[num] not in MenuInstruments) and (not NormalStyleSelected):
					print(Fore.RED+'(UNAVALIBLE) '+str(InstrumentNames[num])+Style.RESET_ALL)
				else:
					print('(#'+str(realNum)+') '+str(InstrumentNames[num]))
				time.sleep(0.005)
		else:
			for num in range(len(InstrumentNames)):
				if ((InstrumentNames[num] in MenuInstruments) and (not NormalStyleSelected) and (num < normalInstrumentNumber)) or (((num < normalInstrumentNumber) or (num == len(InstrumentNames)-1)) and (NormalStyleSelected)):
					print(Style.RESET_ALL+'(#'+str(num)+') '+str(InstrumentNames[num]))
				elif (unsafeMode):
					if((InstrumentNames[num] in MenuInstruments) and (not NormalStyleSelected)) or (NormalStyleSelected):
						print(Fore.YELLOW+'(#'+str(num)+') '+str(InstrumentNames[num])+Style.RESET_ALL)
					else:
						print(Fore.RED+'(#'+str(num)+') '+str(InstrumentNames[num])+Style.RESET_ALL)
				time.sleep(0.005)
		PrintSectionTitle("Instrument Selection")
		Melody = SelectStyleInstrument('Melody',False)
		Harmony = SelectStyleInstrument('Harmony',False)
		Chord = SelectStyleInstrument('Chord',False)
		Bass = SelectStyleInstrument('Bass',False)
		PrintSectionTitle("Intrument List")
		if(not unsafeMode):
			for num in range(40,len(InstrumentNames)):
				if (InstrumentNames[num] not in MenuInstruments) and (not NormalStyleSelected):
					print(Fore.RED+'(UNAVALIBLE) '+str(InstrumentNames[num])+Style.RESET_ALL)
				else:
					print('(#'+str(num-40)+') '+str(InstrumentNames[num]))
				time.sleep(0.005)
		else:
			for num in range(len(InstrumentNames)):
				if ((InstrumentNames[num] in MenuInstruments) and (not NormalStyleSelected) and (num >= normalInstrumentNumber)) or (((num >= normalInstrumentNumber) or (num == len(InstrumentNames)-1)) and (NormalStyleSelected)):
					print(Style.RESET_ALL+'(#'+str(num)+') '+str(InstrumentNames[num]))
				elif (unsafeMode):
					if((InstrumentNames[num] in MenuInstruments) and (not NormalStyleSelected)) or (NormalStyleSelected):
						print(Fore.YELLOW+'(#'+str(num)+') '+str(InstrumentNames[num])+Style.RESET_ALL)
					else:
						print(Fore.RED+'(#'+str(num)+') '+str(InstrumentNames[num])+Style.RESET_ALL)
				time.sleep(0.005)

		Perc1 = SelectStyleInstrument('Percussion 1',True)
		Perc2 = SelectStyleInstrument('Percussion 2',True)

		if(Selection == len(StyleNames)-2):
			PatchName = []
			PatchInfo = []
			for num in range(len(StyleNames)-6):
				PatchName.append(StyleNames[num]+' Style Patch')
				PatchInfo.append(StyleMemoryOffsets[num]+' 00000018\n'+Melody+' '+Harmony+'\n'+Chord+' '+Bass+'\n'+Perc1+' '+Perc2+'\n')
			AddPatch(PatchName,PatchInfo)
		elif(Selection >= len(StyleNames)-6):
			PatchName = []
			PatchInfo = []
			for num in range(len(StyleNames)-6,len(StyleNames)-2):
				PatchName.append(StyleNames[num]+' Style Patch')
				PatchInfo.append(StyleMemoryOffsets[num]+' 00000018\n'+Melody+' '+Harmony+'\n'+Chord+' '+Bass+'\n'+Perc1+' '+Perc2+'\n')
			AddPatch(PatchName,PatchInfo)
		else:
			AddPatch(StyleNames[Selection]+' Style Patch',StyleMemoryOffsets[Selection]+' 00000018\n'+Melody+' '+Harmony+'\n'+Chord+' '+Bass+'\n'+Perc1+' '+Perc2+'\n')

		print("\nPatch Complete")
		time.sleep(0.5)
		print("")
	elif(Selection == 4): #////////////////////////////////////////Advanced Tools
		while True:
			PrintSectionTitle('Advanced Tools')
			print("(#0) Back to Main Menu")
			print("(#1) Change All Wii Music Text")
			print("(#2) Extract/Compile Wii Music Disk")
			print("(#3) Patch Main.dol With Gecko Codes")
			print("(#4) Create Riivolution Patch")

			Selection = MakeSelection(['Please Select an Option',0,4])

			if(Selection == 1): #////////////////////////////////////////Change Text
				#Load Files
				FindGameFolder()
				
				#Run Notepad
				subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/decode.bat\" '+MessageFolder(),capture_output=True)
				time.sleep(0.5)
				print("\nWaiting For User to Finish Editing and for Notepad to Close...")
				subprocess.run('notepad \"'+MessageFolder().replace('\"','')+'/message.d/new_music_message.txt\"',capture_output=True)
				subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/encode.bat\" '+MessageFolder(),capture_output=True)
				print("\nEditing Successful!\n")
			elif(Selection == 2): #////////////////////////////////////////Extract/Compile Disk
				PrintSectionTitle('Extract/Compile Disk')
				print("(#0) Back To Main Menu")
				print("(#1) Extract Disk")
				print("(#2) Compile Disk")

				Selection = MakeSelection(['Choose an Option',0,2])
				if(Selection == 1):
					ExceptedFileExtensions = ['.iso','.wbfs']
					while True:
						DiskPath = input("\nPlease Drag the Wii Music Disk: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
						if(os.path.isfile(DiskPath)) and (pathlib.Path(DiskPath).suffix in ExceptedFileExtensions):
							break
						else:
							print('ERROR: Not Supported File Type')
					subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/extractdisk.bat\" \"'+os.path.dirname(DiskPath)+'\" \"'+os.path.splitext(os.path.basename(DiskPath))[0]+'\" '+os.path.splitext(os.path.basename(DiskPath))[1])
					if(input('\nWould You Like to Set This Path as the Current Game Path? [y/n] ') == 'y'):
						GamePath = os.path.dirname(DiskPath).replace('\\','/')+'/'+os.path.splitext(os.path.basename(DiskPath))[0]+'/DATA'
						BrsarPath = GamePath+'/files/sound/MusicStatic/rp_Music_sound.brsar'
						MessagePath = GamePath+'/files/US/Message/message.carc'
						SaveSetting('Paths','GamePath',GamePath)
				elif(Selection == 2):
					if(input('\nUse Game Path as Disk Directory? [y/n] ') != 'y'):
						while True:
							DiskPath= input("\nDrag Decompressed Wii Music Directory: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
							if(os.path.isdir(DiskPath+'/DATA')):
								break
							else:
								print("\nERROR: Unable to Locate Valid Wii Music Directory")
					else:
						DiskPath = GamePath[0:len(GamePath)-5:1]
					
					DiskName = ''
					DiskNum = 0
					while(os.path.isfile(DiskPath+DiskName+'.wbfs')):
						DiskNum = DiskNum+1
						DiskName = '('+str(DiskNum)+')'
					subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/wit.exe\" cp \"'+DiskPath+'\" \"'+DiskPath+DiskName+'.wbfs\" --wbfs')
				print('')
			elif(Selection == 3): #////////////////////////////////////////Patch Main.dol
				FindGameFolder()
				FindDolphinSave()
				if(input('\nAre you sure you want to patch Main.dol? [y/n] ') == 'y'):
					print('\nCreating Gct...')
					CreateGct()
					print('\nPatching Main.dol...')
					subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/wstrt.exe\" patch \"'+GamePath+'/sys/main.dol\" --add-section R64E01.gct',capture_output=True)
					os.remove('R64E01.gct')
					print('\nPatch Successful!')
			elif(Selection == 4): #////////////////////////////////////////Riivolution Patch
				PrintSectionTitle('Riivolution Patch')
				FindGameFolder()
				FindDolphinSave()
				ModPath = GamePath[0:len(GamePath)-5:1]
				ModPath = ModPath[0:len(ModPath)-len(os.path.basename(ModPath)):1]
				ModName = input('\nPlease Input Mod Name: ')
				while (os.path.isdir(ModPath+ModName)):
					ModName = input('\nDirectory Already Exists! Please Enter a Diffrent Name: ')
				ModPath = ModPath+ModName
				os.mkdir(ModPath)
				os.mkdir(ModPath+'/Riivolution')
				os.mkdir(ModPath+'/Riivolution/codes')
				os.mkdir(ModPath+'/files')
				print('\nMaking Gct...')
				CreateGct()
				print('\nCopying Files...')
				copyfile(GamePath+'/files/Sound/MusicStatic/rp_Music_sound.brsar',ModPath+'/files/rp_Music_sound.brsar')
				copyfile(GamePath+'/files/US/Message/message.carc',ModPath+'/files/message.carc')
				copyfile(ProgramPath+'/Helper/GctFiles/codehandler.bin',ModPath+'/Riivolution/codehandler.bin')
				os.rename(ProgramPath+'/R64E01.gct',ModPath+'/Riivolution/codes/R64E01.gct')
				print('\nCreating XML file...')
				linestowrite = [
				'<wiidisc version="1" root="">',
				'  <id game="R64" />',
				'  <options>',
				'    <section name="'+ModName+'">',
				'      <option name="Load Mod">',
				'        <choice name="Yes">',
				'          <patch id="TheMod" />',
				'        </choice>',
				'      </option>',
				'    </section>',
				'  </options>',
				'  <patch id="TheMod">',
				'    <file disc="/Sound/MusicStatic/rp_Music_sound.brsar" external="/files/rp_Music_sound.brsar" offset="" />',
				'    <file disc="/US/Message/message.carc" external="/files/message.carc" offset="" />',
				'    <memory valuefile="codehandler.bin" offset="0x80001800" />',
				'    <memory value="8000" offset="0x00001CDE" />',
				'    <memory value="28B8" offset="0x00001CE2" />',
				'    <memory value="8000" offset="0x00001F5A" />',
				'    <memory value="28B8" offset="0x00001F5E" />',
				'    <memory valuefile="/codes/R64E01.gct" offset="0x800028B8" />',
				'  </patch>',
				'</wiidisc>']
				xml = open(ModPath+'/Riivolution/'+ModName+'.xml','w')
				xml.writelines(linestowrite)
				xml.close()
				print('\nPatch Creation Successful!\nExported to: '+ModPath)

			else: break
	elif(Selection == 5): #////////////////////////////////////////Run Game
		FindGameFolder()
		FindDolphin()
		PrintSectionTitle("Running Dolphin")
		if(os.path.isfile(GamePath)):
			subprocess.Popen('\"'+DolphinPath+'\" -b -e \"'+GamePath+'\"')
		else:
			subprocess.Popen('\"'+DolphinPath+'\" -b -e \"'+GamePath+'/sys/main.dol\"')
		time.sleep(1)
		print("")
	elif(Selection == 6): #////////////////////////////////////////100% Save File
		FindDolphinSave()
		if(input("\nAre You Sure You Want To Overwrite Your Save Data? [y/n] ") == 'y'):
			subprocess.run('robocopy \"'+ProgramPath+'/Helper/WiiMusicSave\" \"'+SaveDataPath+'\" /MIR /E',capture_output=True)
			print("\nOverwrite Successfull\n")
		else:
			print("\nAborted...\n")
	elif(Selection == 7): #////////////////////////////////////////Download Pre-Made Custom Songs
		print('\nDownloading...')
		try:
			response = requests.get('https://github.com/BenjaminHalko/Pre-Made-Songs-for-Wii-Music/archive/refs/heads/main.zip', stream=True)
			total_size_in_bytes= int(response.headers.get('content-length', 0))
			block_size = 1024
			progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
			with open('CustomSongs.zip', 'wb') as file:
				for data in response.iter_content(block_size):
					progress_bar.update(len(data))
					file.write(data)
			progress_bar.close()
			if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
				print("\nERROR, something went wrong\n")
			print('\nExtracting...\n')
			if(os.path.isdir('PreMade Custom Songs')): rmtree('PreMade Custom Songs')
			subprocess.run('tar -xf CustomSongs.zip')
			os.rename('Pre-Made-Songs-for-Wii-Music-main', 'PreMade Custom Songs')
			os.remove('CustomSongs.zip')
			print('Saved To: \"'+ProgramPath+'/PreMade Custom Songs\"\n')
		except (requests.ConnectionError, requests.Timeout) as exception:
			print('\nFailed to Download File...\n')
	elif(Selection == 8): #////////////////////////////////////////Help
		PrintSectionTitle('Help')
		print("(#0) Back to Main Menu")
		print("(#1) Open the Manual")
		print("(#2) Open Video Guide")
		
		Selection = MakeSelection(['What type of help do you want',0,2])

		if(Selection == 1):
			print('\nOpening Manual...')
			time.sleep(0.5)
			webbrowser.open('https://github.com/BenjaminHalko/WiiMusicEditor#manual')
		elif(Selection == 2):
			print('\nOpening Video Guide...')
			time.sleep(0.5)
			webbrowser.open('thereisnovideoguideyetbecauseihaventrecordedthevideoyet.com')
		print('')
		time.sleep(0.5)
	elif(Selection == 9): #////////////////////////////////////////Settings
		while True:
			PrintSectionTitle("Settings")
			print("(#0) Back To Main Menu")
			print("(#1) Change File Paths")
			print("(#2) Change Default Answers")
			print("(#3) Reset Replaced Song Database")
			print("(#4) Updates")
			if(unsafeMode):
				print("(#5) Switch to Safe Mode")
			else:
				print("(#5) Switch to Unsafe Mode")

			Selection = MakeSelection(['Which Setting Do You Want to Change',0,5])

			if(Selection == 1):
				while True:
					PrintSectionTitle('Path Editor')
					print("(#0) Back To Settings")
					print("(#1) Game Path (Current Path: "+GamePath+')')
					print("(#2) Dolphin Path (Current Path: "+DolphinPath+')')
					print("(#3) Dolphin Save Path (Current Path: "+DolphinSaveData+')')
					Selection = MakeSelection(['Which Path Do You Want to Change',0,3])
					if(Selection == 1):
						GamePath = ''
						FindGameFolder()
						print("")
					elif(Selection == 2):
						DolphinPath = ''
						FindDolphin()
						print("")
					elif(Selection == 3):
						DolphinSaveData = ''
						FindDolphinSave()
						print("")
					else: break
			elif(Selection == 2):
				while True:
					PrintSectionTitle('Default Answers')
					print("(#0) Back To Settings")
					print("(#1) Always Ask \"Are You Sure You Want To Replace Song\": "+DefaultWantToReplaceSong)
					print("(#2) Warm User When Replacing Already Replaced Song: "+DefaultReplacingReplacedSong)
					print("(#3) Use Auto Found Length and Tempo: "+DefaultUseAutoLengthTempo)
					print("(#4) Replace Song Names After Adding Custom Song: "+DefaultReplaceSongNames)

					Selection = MakeSelection(['Choose an Option',0,4])
					if(Selection == 1):
						DefaultWantToReplaceSong = ChangeDefaultAnswer(['Yes','No'],['Want To Replace Song',DefaultWantToReplaceSong])
					elif(Selection == 2):
						DefaultReplacingReplacedSong = ChangeDefaultAnswer(['Yes','No'],['Replacing Replaced Song',DefaultReplacingReplacedSong])
					elif(Selection == 3):
						DefaultUseAutoLengthTempo = ChangeDefaultAnswer(['Ask','Yes','No'],['Use Auto Length and Tempo'])
					elif(Selection == 4):
						DefaultReplaceSongNames = ChangeDefaultAnswer(['Ask','Yes','No'],['Replace Song Names'])
					else: break
			elif(Selection == 3):
				FindGameFolder()
				if(input("\nAre You Sure You Want to Reset the Replaced Song Database? [y/n] ") == 'y'):
					SaveSetting('Applied Custom Songs', WiiDiskFolder, '')
					print('\nReset Successful!\n')
				else:
					print('')
			elif(Selection == 4):
				while True:
					PrintSectionTitle('Updates')
					print("(#0) Back To Settings")
					print("(#1) Check For Updates")
					if(AutoUpdate):
						print("(#2) Turn Off Auto Updates")
					else:
						print("(#2) Turn On Auto Updates")
					if(not bool(beta)):
						print("(#3) Switch to Beta Branch")
					else:
						print("(#3) Switch to Main Branch")

					Selection = MakeSelection(['Pick an Option',0,3])
					if(Selection == 1):
						print('')
						CheckForUpdates(True)
						print('')
					elif(Selection == 2):
						AutoUpdate = not AutoUpdate
						SaveSetting('Updates', 'AutoUpdate', str(int(AutoUpdate)))
					elif(Selection == 3):
						beta = int(not bool(beta))
						SaveSetting('Updates', 'Branch', str(beta))
						if(DownloadUpdate()):
							beta = int(not bool(beta))
							SaveSetting('Updates', 'Branch', str(beta))
					else: break
			elif(Selection == 5):
				if((not unsafeMode) and (input('\nAre You Sure You Want to Turn on Unsafe Mode? [y/n] ') == 'y')) or (unsafeMode):
					unsafeMode = not unsafeMode
					SaveSetting('Unsafe Mode','Unsafe Mode',str(int(unsafeMode)))
				print('')
			else: break
	elif(Selection == 10): #////////////////////////////////////////Credits
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
