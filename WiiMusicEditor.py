import os
import sys
import getpass
import time
import subprocess
import configparser
import pathlib
import tempfile
from shutil import copyfile, rmtree, copytree
from math import floor, ceil
from typing import ByteString
import webbrowser
import hashlib
import zipfile

#Special Imports
while True:
	try:
		import requests
		import mido
		from colorama import Fore, Style, init
		from tqdm import tqdm
		from tabulate import tabulate 
		break
	except ImportError:
		subprocess.run('python -m pip install --upgrade pip')
		subprocess.run('pip install mido requests colorama tqdm tabulate')

init(convert=True)

time.sleep(0.05)

class SongClass:
	def __init__(self,SongType,Name,MemOffset,SongId,ScoreId,MemOrder):
		self.SongType = SongType
		self.Name = Name
		self.MemOffset = MemOffset
		self.SongId = SongId
		self.ScoreId = ScoreId
		self.MemOrder = MemOrder

class StyleClass:
	def __init__(self,StyleType,Name,MemOffset):
		self.StyleType = StyleType
		self.Name = Name
		self.MemOffset = MemOffset

class InstrumentClass:
	def __init__(self,Name,Number,InMenu):
		self.Name = Name
		self.Number = Number
		self.InMenu = InMenu

class SongTypeValue:
	Regular = 0
	Menu = 1
	JamMastery = 2

class StyleTypeValue:
	Global = 0
	SongSpecific = 1
	QuickJam = 2
	Menu = 3

NumberOfStyleTypes = 5

Songs = [
SongClass(SongTypeValue.Regular,'A Little Night Music','025a08a8','0161','0162',6),
SongClass(SongTypeValue.Regular,'American Patrol','025a0c54','016B','016C',11),
SongClass(SongTypeValue.Regular,'Animal Crossing','025a2780','01B5','01B6',48),
SongClass(SongTypeValue.Regular,'Animal Crossing K.K. Blues','025a1758','0189','018A',26),
SongClass(SongTypeValue.Regular,'Bridal Chorus','025a04fc','0157','0158',1),
SongClass(SongTypeValue.Regular,'Carmen','025a0674','015B','015C',3),
SongClass(SongTypeValue.Regular,'Chariots of Fire','025a1df4','019B','019C',35),
SongClass(SongTypeValue.Regular,'Daydream Believer','025a1c7c','0197','0198',33),
SongClass(SongTypeValue.Regular,'Do-Re-Mi','025a0adc','0167','0168',9),
SongClass(SongTypeValue.Regular,'Every Breath You Take','025a1d38','0199','019A',34),
SongClass(SongTypeValue.Regular,'F-Zero','025a283c','01B7','01B8',49),
SongClass(SongTypeValue.Regular,'Frere Jacques','025a1468','0181','0182',22),
SongClass(SongTypeValue.Regular,'From Santurtzi to Bilbao','025a1814','018B','018C',27),
SongClass(SongTypeValue.Regular,'From the New World','025a1000','0175','0176',16),
SongClass(SongTypeValue.Regular,'Happy Birthday to You','025a0a20','0165','0166',8),
SongClass(SongTypeValue.Regular,'Ill Be There','025a21a0','01A5','01A6',40),
SongClass(SongTypeValue.Regular,'Ive Never Been to Me','025a2490','01AD','01AE',44),
SongClass(SongTypeValue.Regular,'Jingle Bell Rock','025a2318','01A7','01A8',41),
SongClass(SongTypeValue.Regular,'La Bamba','025a10bc','0177','0178',17),
SongClass(SongTypeValue.Regular,'La Cucaracha','025a198c','018F','0190',29),
SongClass(SongTypeValue.Regular,'Little Hans','025a169c','0187','0188',25),
SongClass(SongTypeValue.Regular,'Long Long Ago','025a1234','017B','017C',19),
SongClass(SongTypeValue.Regular,'Material Girl','025a2028','01A1','01A2',38),
SongClass(SongTypeValue.Regular,'Minuet in G Major','025a0964','0163','0164',7),
SongClass(SongTypeValue.Regular,'My Grandfathers Clock','025a0f44','0173','0174',15),
SongClass(SongTypeValue.Regular,'O-Christmas Tree','025a15e0','0185','0186',24),
SongClass(SongTypeValue.Regular,'Ode To Joy','025a0440','0155','0156',0),
SongClass(SongTypeValue.Regular,'Oh My Darling Clementine','025a0e88','0171','0172',14),
SongClass(SongTypeValue.Regular,'Over the Waves','025a1a48','0191','0192',30),
SongClass(SongTypeValue.Regular,'Please Mr. Postman','025a1f6c','019F','01A0',37),
SongClass(SongTypeValue.Regular,'Sakura Sakura','025a1b04','0193','0194',31),
SongClass(SongTypeValue.Regular,'Scarborough Fair','025a1178','0179','017A',18),
SongClass(SongTypeValue.Regular,'September','025a1eb0','019D','019E',36),
SongClass(SongTypeValue.Regular,'Sukiyaki','025a1bc0','0195','0196',32),
SongClass(SongTypeValue.Regular,'Super Mario Bros','025a254c','01AF','01B0',45),
SongClass(SongTypeValue.Regular,'Sur le Pont d Avignon','025a13ac','017F','0180',21),
SongClass(SongTypeValue.Regular,'Swan Lake','025a05b8','0159','015A',2),
SongClass(SongTypeValue.Regular,'The Blue Danube','025a07ec','015F','0160',5),
SongClass(SongTypeValue.Regular,'The Entertainer','025a0b98','0169','016A',10),
SongClass(SongTypeValue.Regular,'The Flea Waltz','025a1524','0183','0184',23),
SongClass(SongTypeValue.Regular,'The Legend of Zelda','025a2608','01B1','01B2',46),
SongClass(SongTypeValue.Regular,'The Loco Motion','025a20e4','01A3','01A4',39),
SongClass(SongTypeValue.Regular,'Troika','025a18d0','018D','018E',28),
SongClass(SongTypeValue.Regular,'Turkey in the Straw','025a0d10','016D','016E',12),
SongClass(SongTypeValue.Regular,'Twinkle Twinkle Little Star','025a12f0','017D','017E',20),
SongClass(SongTypeValue.Regular,'Wake Me Up Before You Go-Go','025a23d4','01A9','01AA',42),
SongClass(SongTypeValue.Regular,'Wii Music','025a0730','015D','015E',4),
SongClass(SongTypeValue.Regular,'Wii Sports','025a26c4','01B3','01B4',47),
SongClass(SongTypeValue.Regular,'Woman','025a23d4','01AB','01AC',43),
SongClass(SongTypeValue.Regular,'Yankee Doodle','025a0dcc','016F','0170',13),
SongClass(SongTypeValue.Menu,'Menu Song (It is still a work in progress though)',['0259ACB0','0259ACD4','0259ACF8','0259AD1C','0259AD40'],-1,-1,-1)]
#'19AF7A0',['19ABD00','19B1A00','19B4360','19B69A0','19B9360','19BBF20'],'2260',['3AA0','2960','2640','29C0','2BC0','29A0']
Styles = [
StyleClass(StyleTypeValue.Global,'Jazz','0659A65C'),
StyleClass(StyleTypeValue.Global,'Rock','0659A680'),
StyleClass(StyleTypeValue.Global,'Latin','0659A6A4'),
StyleClass(StyleTypeValue.Global,'March','0659A6C8'),
StyleClass(StyleTypeValue.Global,'Electronic','0659A6EC'),
StyleClass(StyleTypeValue.Global,'Pop','0659A710'),
StyleClass(StyleTypeValue.Global,'Japanese','0659A724'),
StyleClass(StyleTypeValue.Global,'Tango','0659A758'),
StyleClass(StyleTypeValue.Global,'Classical','0659A77C'),
StyleClass(StyleTypeValue.Global,'Hawaiian','0659A7A0'),
StyleClass(StyleTypeValue.Global,'Reggae','0659A7C4'),
StyleClass(StyleTypeValue.SongSpecific,'A Little Night Music','0659AB00'),
StyleClass(StyleTypeValue.SongSpecific,'Animal Crossing','0659AA28'),
StyleClass(StyleTypeValue.SongSpecific,'Animal Crossing K.K. Blues','0659AB48'),
StyleClass(StyleTypeValue.SongSpecific,'Carmen','0659A878'),
StyleClass(StyleTypeValue.SongSpecific,'Chariots of Fire','0659A908'),
StyleClass(StyleTypeValue.SongSpecific,'Every Breath You Take','0659A8E4'),
StyleClass(StyleTypeValue.SongSpecific,'From Santurtzi to Bilbao','0659AADC'),
StyleClass(StyleTypeValue.SongSpecific,'Happy Birthday to You','0659AA94'),
StyleClass(StyleTypeValue.SongSpecific,'I\'ll Be There','0659A974'),
StyleClass(StyleTypeValue.SongSpecific,'I\'ve Never Been to Me','0659A9BC'),
StyleClass(StyleTypeValue.SongSpecific,'La Cucaracha','0659AAB8'),
StyleClass(StyleTypeValue.SongSpecific,'Material Girl','0659A950'),
StyleClass(StyleTypeValue.SongSpecific,'Minuet in G Major','0659AA4C'),
StyleClass(StyleTypeValue.SongSpecific,'O-Christmas Tree','0659A89C'),
StyleClass(StyleTypeValue.SongSpecific,'Oh My Darling Clementine','0659A830'),
StyleClass(StyleTypeValue.SongSpecific,'Over The Waves','0659A8C0'),
StyleClass(StyleTypeValue.SongSpecific,'Scarborough Fair','0659A854'),
StyleClass(StyleTypeValue.SongSpecific,'September','0659A92C'),
StyleClass(StyleTypeValue.SongSpecific,'Super Mario Bros','0659AC8C'),
StyleClass(StyleTypeValue.SongSpecific,'The Blue Danube','0659AB24'),
StyleClass(StyleTypeValue.SongSpecific,'The Entertainer','0659AA70'),
StyleClass(StyleTypeValue.SongSpecific,'The Legend of Zelda','0659A9E0'),
StyleClass(StyleTypeValue.SongSpecific,'Twinkle Twinkle Little Star','0659A7E8'),
StyleClass(StyleTypeValue.SongSpecific,'Wii Sports','0659AA04'),
StyleClass(StyleTypeValue.SongSpecific,'Wii Music','0659AB6C'),
StyleClass(StyleTypeValue.SongSpecific,'Woman','0659A998'),
StyleClass(StyleTypeValue.SongSpecific,'Yankee Doodle','0659A80C'),
StyleClass(StyleTypeValue.QuickJam,'A Capella','0659AC20'),
StyleClass(StyleTypeValue.QuickJam,'Acoustic','0659AB93'),
StyleClass(StyleTypeValue.QuickJam,'African Electronic','0659AB93'),
StyleClass(StyleTypeValue.QuickJam,'Animals!','0659AC68'),
StyleClass(StyleTypeValue.QuickJam,'Calypso','0659AC44'),
StyleClass(StyleTypeValue.QuickJam,'Exotic','0659ABFC'),
StyleClass(StyleTypeValue.QuickJam,'Flamenco','0659AB90'),
StyleClass(StyleTypeValue.QuickJam,'Galactic','0659ADD0'),
StyleClass(StyleTypeValue.QuickJam,'Handbell','0659AB93'),
StyleClass(StyleTypeValue.QuickJam,'Karate','0659ABB4'),
StyleClass(StyleTypeValue.QuickJam,'Orchestral','0659AD64'),
StyleClass(StyleTypeValue.QuickJam,'Parade','0659ABD8'),
StyleClass(StyleTypeValue.QuickJam,'Rapper','0659ADF4'),
StyleClass(StyleTypeValue.QuickJam,'Samba','0659AE18'),
StyleClass(StyleTypeValue.Menu,'Menu Style Main','0659ACB0'),
StyleClass(StyleTypeValue.Menu,'Menu Style Electronic','0659ACD4'),
StyleClass(StyleTypeValue.Menu,'Menu Style Japanese','0659ACF8'),
StyleClass(StyleTypeValue.Menu,'Menu Style March','0659AD1C'),
StyleClass(StyleTypeValue.Menu,'Menu Style A Capella','0659AD40')]

Instruments = [
InstrumentClass('Piano',0,True),
InstrumentClass('Marimba',1,False),
InstrumentClass('Vibraphone',2,True),
InstrumentClass('Steel Drum',3,False),
InstrumentClass('Dulcimer',4,False),
InstrumentClass('Handbell',5,False),
InstrumentClass('Harpsichord',6,False),
InstrumentClass('Timpani',7,False),
InstrumentClass('Galactic Piano',8,False),
InstrumentClass('Toy Piano',9,False),
InstrumentClass('Dog',10,False),
InstrumentClass('Cat',11,False),
InstrumentClass('Rapper',12,False),
InstrumentClass('Guitar',13,False),
InstrumentClass('Electric Guitar',14,False),
InstrumentClass('Electric Bass',15,False),
InstrumentClass('Double Bass',16,False),
InstrumentClass('Ukulele',17,False),
InstrumentClass('Banjo',18,False),
InstrumentClass('Sitar',19,False),
InstrumentClass('Shamisen',20,True),
InstrumentClass('Harp',21,False),
InstrumentClass('Galactic Guitar',22,True),
InstrumentClass('Galactic Bass',23,True),
InstrumentClass('Jaw Harp',24,False),
InstrumentClass('Violin',25,True),
InstrumentClass('Cello',26,False),
InstrumentClass('Trumpet',27,False),
InstrumentClass('Saxophone',28,True),
InstrumentClass('Flute',29,True),
InstrumentClass('Clairenet',30,True),
InstrumentClass('Tuba',31,True),
InstrumentClass('Accordion',32,False),
InstrumentClass('Harmonica',33,False),
InstrumentClass('Bagpipe',34,False),
InstrumentClass('Recorder',35,False),
InstrumentClass('Galactic horn',36,False),
InstrumentClass('Nes',37,False),
InstrumentClass('Singer',38,True),
InstrumentClass('Another Singer',39,True),
InstrumentClass('Basic Drums',40,True),
InstrumentClass('Rock Drums',41,True),
InstrumentClass('Jazz Drums',42,False),
InstrumentClass('Latin Drums',43,True),
InstrumentClass('Ballad Drums',44,False),
InstrumentClass('Congas',45,False),
InstrumentClass('Maracas',46,False),
InstrumentClass('Tambourine',47,False),
InstrumentClass('Cuica',48,False),
InstrumentClass('Cowbell',49,False),
InstrumentClass('Clap',50,False),
InstrumentClass('Bells',51,False),
InstrumentClass('Castanets',52,False),
InstrumentClass('Guiro',53,False),
InstrumentClass('Timpales',54,False),
InstrumentClass('Djembe',55,False),
InstrumentClass('Taiko Drum',56,True),
InstrumentClass('Cheerleader',57,False),
InstrumentClass('Snare Drum',58,True),
InstrumentClass('Bass Drum',59,False),
InstrumentClass('Galactic Drums',60,True),
InstrumentClass('Galactic Congas',61,False),
InstrumentClass('DJ Turntables',62,True),
InstrumentClass('Kung Fu Person',63,False),
InstrumentClass('Reggae Drums',64,False),
InstrumentClass('Whistle',65,False),
InstrumentClass('Beatbox',66,True),
InstrumentClass('None',-1,False)]

MainDolOffset = '59C56E'

GctValues = ['00D0C0DE00D0C0DE','F000000000000000']

#Functions
def AddPatch(PatchName,PatchInfo):
	global GamePath
	global CodePath
	global DefaultStyleMethod
	global ProgramPath
	codePathInGamePath = GamePath+'/GeckoCodes.ini'
	if(type(PatchName) == str):
		PatchName = [PatchName]
		PatchInfo = [PatchInfo]
	
	for patchNum in range(len(PatchName)):
		if(os.path.exists(codePathInGamePath)):
			codes = open(codePathInGamePath,'r')
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
			
			codes = open(codePathInGamePath,'w')
			codes.writelines(lineText)
			codes.close()
		else:
			codes = open(codePathInGamePath,'w')
			codes.write('[Gecko]\n')
			codes.write('$'+PatchName[patchNum]+' [WiiMusicEditor]\n')
			codes.write(PatchInfo[patchNum])
			codes.write('[Gecko_Enabled]\n')
			codes.write('$'+PatchName[patchNum]+'\n')
			codes.close()
		if(os.path.isfile(CodePath)): os.remove(CodePath)
		copyfile(codePathInGamePath,CodePath)

def FindGameFolder():
	global GamePath
	global BrsarPath
	global MessagePath
	global WiiDiskFolder
	if(not os.path.isdir(GamePath+'/files')):
		ExceptedFileExtensions = ['.iso','.wbfs']
		while True:
			GamePath = input("\nDrag Wii Music Filesystem or ROM to Window: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
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
				subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/wit.exe\" cp --fst \"'+GamePath+'\" \"'+os.path.dirname(GamePath)+"/"+os.path.splitext(os.path.basename(GamePath))[0]+'\"')
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
			DolphinSaveData = input("\nDrag Dolphin Config Directory to Window: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
			if(os.path.isdir(DolphinSaveData+'/Wii')):
				DolphinSaveData = DolphinSaveData.replace('\\','/')
				CodePath = DolphinSaveData+"/GameSettings/R64E01.ini"
				SaveDataPath = DolphinSaveData+"/Wii/title/00010000/52363445/data"
				SaveSetting('Paths','DolphinSaveData',DolphinSaveData)
				break
			else:
				print("\nERROR: Unable to Locate Valid Dolphin Save Directory")

def ChangeName(SongToChange,newText):
	global ProgramPath
	TextOffset = ['c8','190','12c']
	subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/decode.bat\" '+MessageFolder(),capture_output=True)
	for typeNum in range(3):
		message = open(MessageFolder().replace('\"','')+'/message.d/new_music_message.txt','rb')
		textlines = message.readlines()
		message.close()
		offset = format(int(TextOffset[typeNum],16)+Songs[SongToChange].MemOrder,'x').lower()
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
	return '\"'+(os.path.dirname(MessagePath))+'\"'

def LoadSetting(section,key,default):
	global ProgramPath
	ini = configparser.ConfigParser()
	ini.read(ProgramPath+'/settings.ini')
	if(ini.has_option(section, key)):
		return ini[section][key]
	else:
		return default

def SaveSetting(section,key,value):
	global ProgramPath
	ini = configparser.ConfigParser()
	ini.read(ProgramPath+'/settings.ini')
	if(not ini.has_section(section)):
		ini.add_section(section)
	ini.set(section,key,value)
	print(str(ini))
	with open(ProgramPath+'/settings.ini', 'w') as inifile:
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
			subprocess.run(ProgramPath+'/WiiMusicEditorNew/Helper/Update/Update.bat')
			quit()
			return False
	except (requests.ConnectionError, requests.Timeout) as exception:
		print('\nFailed to Download File...\n')
		return True

def SelectStyleInstrument(PartString,IsPercussion):
	global Styles
	global Selection
	global normalInstrumentNumber
	global unsafeMode
	global Instruments
	global NormalStyleSelected
	print('')
	while True:
		PartType = input("What\'s the Instrument Number you want for the "+PartString+": ")
		if(PartType.isnumeric()):
			if(IsPercussion) and (not unsafeMode): PartType = int(PartType) + normalInstrumentNumber
			PartType = Instruments[int(PartType)].Number
			if(unsafeMode):
				if(PartType == len(Instruments)-1):
					PartType = 'ffffffff'
					break
				elif (PartType < len(Instruments)):
					PartType = format(PartType,'x').upper()
					PartType = '0'*(8-len(PartType))+PartType
					break
				else:
					print("\nERROR: Not a Valid Number\n")
			elif((PartType == normalInstrumentNumber and not IsPercussion) or (PartType == len(Instruments)-1 and IsPercussion)) and (NormalStyleSelected):
				PartType = 'ffffffff'
				break
			elif((PartType < normalInstrumentNumber) != IsPercussion) and (PartType < len(Instruments)) and ((NormalStyleSelected) or (Instruments[PartType].InMenu)):
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
	global GamePath
	global ProgramPath
	patches = open(GamePath+'/GeckoCodes.ini')
	textlines = patches.readlines()
	patches.close()
	codes = GctValues[0]
	for text in textlines:
		if(text[0].isalpha() or text[0].isnumeric()):
			codes = codes + text.replace(' ','').strip()
	codes = codes+GctValues[1]
	patch = open(ProgramPath+'/R64E01.gct','wb')
	patch.write(bytes.fromhex(codes))
	patch.close()

def LoadNormalFiles():
	global ProgramPath
	global GamePath
	ExceptedFileExtensions = ['.iso','.wbfs']
	TempPath = GamePath
	while True:
		if(TempPath == ""):
			TempPath = input("\nDrag an UNALTERED Wii Music Directory or a Wii Music Disk on to the Window: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
		if(os.path.isdir(TempPath+'/DATA/files')) or (os.path.isdir(TempPath+'/files')):
			if(os.path.isdir(TempPath+'/DATA')):
				TempPath = os.path.dirname(TempPath+'/DATA/files').replace('\\','/')
			else:
				TempPath = os.path.dirname(TempPath+'/files').replace('\\','/')
			if(CheckFiles(TempPath)):
				CopyUnalteredFiles(TempPath)
				break
			else:
				if(TempPath != GamePath): print("Not an Unaltered Wii Music Directory")
				
		elif(os.path.isfile(TempPath)) and (pathlib.Path(TempPath).suffix in ExceptedFileExtensions):
			if(os.path.isdir(ProgramPath+"/Disk")): rmtree(ProgramPath+"/Disk")
			subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/wit.exe\" cp --fst \"'+TempPath+'\" \"'+ProgramPath+'/Disk/\"')
			TempPath = ProgramPath+'/Disk/DATA'
			if(CheckFiles(TempPath)):
				CopyUnalteredFiles(TempPath)
				allowBreak = True
			else:
				if(TempPath != GamePath):
					print("Not an Unaltered Wii Music Directory")
				allowBreak = False
			rmtree(ProgramPath+"/Disk")
			if(allowBreak): break
		else:
			if(TempPath != GamePath): print("\nERROR: Unable to Locate Valid Wii Music Directory")
		TempPath = ""

def CheckFiles(directory):
	global brsarChecksum
	global messageChecksum
	global mainDolChecksum
	md5_hash = hashlib.md5()
	a_file = open(directory+'/files/Sound/MusicStatic/rp_Music_sound.brsar', "rb")
	content = a_file.read()
	a_file.close()
	md5_hash.update(content)
	currentBrsarChecksum = md5_hash.hexdigest()
	md5_hash = hashlib.md5()
	a_file = open(directory+'/files/US/Message/message.carc', "rb")
	content = a_file.read()
	a_file.close()
	md5_hash.update(content)
	currentMessageChecksum = md5_hash.hexdigest()
	md5_hash = hashlib.md5()
	a_file = open(directory+'/sys/main.dol', "rb")
	content = a_file.read()
	a_file.close()
	md5_hash.update(content)
	currentMainDolChecksum = md5_hash.hexdigest()
	return (currentBrsarChecksum == brsarChecksum) and (currentMessageChecksum == messageChecksum) and (currentMainDolChecksum == mainDolChecksum)

def CopyUnalteredFiles(dir):
	global ProgramPath
	if(not os.path.isdir(ProgramPath+'/Helper/Backup')): os.mkdir(ProgramPath+'/Helper/Backup')
	if(not os.path.isfile(ProgramPath+'/Helper/Backup/rp_Music_sound.brsar')):
		copyfile(dir+'/files/Sound/MusicStatic/rp_Music_sound.brsar',ProgramPath+'/Helper/Backup/rp_Music_sound.brsar')
	if(not os.path.isfile(ProgramPath+'/Helper/Backup/message.carc')):
		copyfile(dir+'/files/US/Message/message.carc',ProgramPath+'/Helper/Backup/message.carc')
	if(not os.path.isfile(ProgramPath+'/Helper/Backup/main.dol')):
		copyfile(dir+'/sys/main.dol',ProgramPath+'/Helper/Backup/main.dol')

def CopyFileSafe(copyFrom,copyTo):
	if(os.path.isfile(copyTo)): os.remove(copyTo)
	copyfile(copyFrom,copyTo)

def LoadNewFile(dir):
	global GctValues
	global GamePath
	geckoCodeFile = ""
	if(os.path.isfile(dir)):
		files = [dir]
	else:
		files = os.listdir(dir)
	
	for currentFile in files:
		file = dir+'/'+currentFile
		if(file.endswith('.brsar')):
			CopyFileSafe(file,GamePath+'/files/Sound/MusicStatic/rp_Music_sound.brsar')
			print('\nImported .brsar')
		elif(file.endswith('.carc')):
			CopyFileSafe(file,GamePath+'/files/US/Message/message.carc')
			print('\nImported .carc')
		elif(file.endswith('.dol')):
			CopyFileSafe(file,GamePath+'/sys/main.dol')
			print('\nImported .dol')
		elif(file.endswith('.gct')):
			if(geckoCodeFile == ""): geckoCodeFile = file
		elif(file.endswith('.ini')):
			geckoCodeFile = file

	if(geckoCodeFile != ""):
		if(geckoCodeFile.endswith('.gct')):
			if(os.path.isfile(GamePath+'/GeckoCodes.ini')): os.remove(GamePath+'/GeckoCodes.ini')
			codes = open(file,'rb')
			codes.seek(8)
			values = codes.read(os.stat(file).st_size-16).hex()
			codes.close()
			codes = open(GamePath+'/GeckoCodes.ini','w')
			codes.write('[Gecko]\n$Imported Geckocodes [WiiMusicEditor]\n'+values+'\n[Gecko_Enabled]\n$Imported Geckocodes\n')
			codes.close()
			print('\nImported .gct')
		else:
			CopyFileSafe(geckoCodeFile,GamePath+'/GeckoCodes.ini')
			print('\nImported .ini')

def EditBrsarOffset(offset):
	global sizeDifference
	global brsar
	brsar.seek(offset)
	size = brsar.read(4)
	brsar.seek(offset)
	brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
	brsar.seek(offset+(int.from_bytes(size,"big")+sizeDifference))
	
#Default Paths
ProgramPath = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
GamePath = LoadSetting('Paths','GamePath','None')
BrsarPath = GamePath+'/files/sound/MusicStatic/rp_Music_sound.brsar'
MessagePath = GamePath+'/files/US/Message/message.carc'
DolphinSaveData = LoadSetting('Paths','DolphinSaveData',"C:/Users/"+getpass.getuser()+"/Documents/Dolphin Emulator")
CodePath = DolphinSaveData+"/GameSettings/R64E01.ini"
SaveDataPath = DolphinSaveData+"/Wii/title/00010000/52363445/data"
DolphinPath = LoadSetting('Paths','DolphinPath','None')
WiiDiskFolder = ''
FindWiiDiskFolder()

#Checksums
brsarChecksum = "e1f24f2363ed9accddc5c21d6a4b8149"
messageChecksum = "dcb17927eaa761648d4a8639973cc13a"
mainDolChecksum = "b72505b4877a4d55435a597fa2544a77"

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
DefaultLoadSongScore = LoadSetting('Default Answers', 'Load Song And Score', 'No')

#Unsafe Mode
unsafeMode = bool(int(LoadSetting('Unsafe Mode','Unsafe Mode','0')))

#Main Loop
while True:
	#Find Branch
	if(not os.path.exists('settings.ini')):
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

	if(AutoUpdate) and (not uptodate):
		uptodate = True
		CheckForUpdates(False)

	#First Run
	if(GamePath == 'None'):
		print('\nThanks for Downloading the Wii Music Editor!')
		print('\nLet\'s Setup Some File Paths for You!')
		FindGameFolder()
		if(not os.path.isfile(ProgramPath+'/Helper/Backup/rp_Music_sound.brsar')) or (not os.path.isfile(ProgramPath+'/Helper/Backup/message.carc')) or (not os.path.isfile(ProgramPath+'/Helper/Backup/main.dol')):
			LoadNormalFiles()
		if(input('\nWould You Like to Specify a Dolphin Directory? [y/n] ') == 'y'):
			FindDolphin()
	elif(not os.path.isfile(ProgramPath+'/Helper/Backup/rp_Music_sound.brsar')) or (not os.path.isfile(ProgramPath+'/Helper/Backup/message.carc')) or (not os.path.isfile(ProgramPath+'/Helper/Backup/main.dol')):
		LoadNormalFiles()

	#Options
	PrintSectionTitle('Options')
	print("(#1) Add Custom Song To Wii Music")
	print("(#2) Change Song Names")
	print("(#3) Edit Styles")
	print("(#4) Advanced Tools")
	print("(#5) Load Wii Music")
	print("(#6) Revert Changes")
	print("(#7) Overwrite Save File With 100% Save")
	print("(#8) Download Pre-Made Custom Songs")
	print("(#9) Help")
	print("(#10) Settings")
	print("(#11) Credits")

	Selection = MakeSelection(['Please Select an Option',1,11])

	if(Selection == 1): #////////////////////////////////////////Add Custom Song
		#Load Files
		FindGameFolder()
		FindDolphinSave()

		#Load Brseq
		ExceptedSongExtensions = ['.midi','.mid','.brseq','.rseq']
		BrseqInfo = []
		BrseqLength = []
		for num in range(2):
			while True:
				extraString = ''
				if(DefaultLoadSongScore == 'Yes'):
					extraString = ' [SONG]'
					if(num == 1): extraString = ' [SCORE]'
				BrseqPath = input("\nDrag File to Batch (MIDIs, BRSEQ, & RSEQ Files only)"+extraString+": ").replace('&', '').replace('\'', '').replace('\"', '').strip()
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
					if(num == 0): subprocess.run('\"'+ProgramPath+'/Helper/SequenceCmd/GotaSequenceCmd.exe\" to_midi \"'+directory+'/z.brseq\"')
				else:
					subprocess.run('\"'+ProgramPath+'/Helper/SequenceCmd/GotaSequenceCmd.exe\" from_midi \"'+directory+'/z.midi\"')
				if(num == 0) :
					Tempo = 'Could Not Locate'
					Length = 'Could Not Locate'
					if(os.path.isfile(directory+"/z.midi")):
						mid = mido.MidiFile(directory+"/z.midi")
						
						for msg in mid.tracks[0]:
							if(msg.type == 'set_tempo'):
								Tempo = floor(mido.tempo2bpm(msg.tempo))
						Length = str(ceil(mid.length*Tempo/60))
						Tempo = str(Tempo)
				Brseq = open(directory+"/z.brseq","rb")
				Brseq.seek(0)
				BrseqInfo.append(Brseq.read())
				Brseq.close()
				BrseqLength.append(format(os.stat(directory+"/z.brseq").st_size,'x').upper())
			if(num == 0) and (DefaultLoadSongScore != 'Yes'):
				BrseqInfo.append(BrseqInfo[0])
				BrseqLength.append(BrseqLength[0])
				print('cheese')
				break

		#Applied Custom Songs
		appliedCustomSongs = []
		if(os.path.isfile(GamePath+'/GeckoCodes.ini')):
			codes = open(GamePath+'/GeckoCodes.ini')
			textlines = codes.readlines()
			codes.close()
			for text in textlines:
				if('[WiiMusicEditor]' in text) and ('Style' not in text):
					appliedCustomSongs.append(text[1:len(text)-29:1])

		#Song List
		LowestSong = -1
		PrintSectionTitle('Song List')

		for num in range(len(Songs)):
			if(Songs[num].Name in appliedCustomSongs):
				print(Fore.YELLOW+'(#'+str(num)+') '+str(Songs[num].Name)+' ~[Already Replaced]~'+Style.RESET_ALL)
			else:
				print('(#'+str(num)+') '+str(Songs[num].Name))
			time.sleep(0.005)

		#Brseq Info
		PrintSectionTitle("File Info")
		print("Number of Beats: "+Length)
		print("Tempo: "+Tempo)

		#Song Selection
		PrintSectionTitle('Song Selection')
		while True:
			SongSelected = input("Enter the Song Number you want to Replace: ")
			if(SongSelected.isnumeric()) and (int(SongSelected) < len(Songs)):
				SongSelected = int(SongSelected)
				if(Songs[SongSelected].Name not in appliedCustomSongs) or (DefaultReplacingReplacedSong == 'No') or (input('\nWARNING: You Have Already Replaced this Song Before! Are You Sure You Want to Replace this Song [y/n] ') == 'y'):
					break
				else:
					print('Aborted...\n')
			else:
				print("\nERROR: Not a Valid Number\n")

		#Length, Tempo, Time Signature Patch
		if(SongSelected != 50):
			PrintSectionTitle("Length, Tempo, Time Signature Patch")
			AutoFill = 'n'
			if((Tempo != 'Could Not Locate') or ((Length != '0') and (Length != 'Could Not Locate'))) and (DefaultUseAutoLengthTempo != 'No'):
				MetaDataFound = ''
				if(Length != 'Could Not Locate') and (Length != '0'): MetaDataFound = 'Length'
				if(Tempo != 'Could Not Locate'):
					if(MetaDataFound == ''): MetaDataFound = 'Tempo'
					else: MetaDataFound = MetaDataFound+', Tempo'
				print('Metadata Found: '+MetaDataFound)
				if(DefaultUseAutoLengthTempo == 'Yes'):
					AutoFill = 'y'
				else:
					AutoFill = input("\nI've found some Metadata for you! Would you like to Autofill? [y/n] ")
			
			if(AutoFill != 'y') or (Length == '0'):
				Length = MakeSelection(['\nHow Many Measures in Your Song'])
			else:
				Length = format(int(Length),'x').upper()

			if(AutoFill != 'y') or (not Tempo.isnumeric()):
				Tempo = MakeSelection(['What is the Tempo of Your Song'])

			Tempo = format(int(Tempo),'x').upper()

			while True:
				TimeSignature = input("\nWhat's the Time Signature of your Song? (4 = 4/4, 3 = 3/4): ")
				if(TimeSignature == '3') or (TimeSignature == '4'):
					break
				else:
					print("\nERROR: Please Press Ether 4 or 3")

			if(AutoFill != 'y') or (Length == 0):
				Length = format(int(Length) * int(TimeSignature),'x').upper()
			
			#Final Writting
			LengthCode = '0'+format(int(Songs[SongSelected].MemOffset,16)+6,'x').lower()+' '+'0'*(8-len(Length))+Length+'\n'
			TempoCode = '0'+format(int(Songs[SongSelected].MemOffset,16)+10,'x').lower()+' '+'0'*(8-len(Tempo))+Tempo+'\n'
			TimeCode = Songs[SongSelected].MemOffset+' 00000'+TimeSignature+'00\n'

		if(DefaultWantToReplaceSong != 'No') or (input('\nAre You Sure You Want to Override '+Songs[SongSelected].Name+'?\nYou CANNOT restore the song if you don\'t have a backup! [y/n] ') == 'y'):
			#Brsar Writing
			brsar = open(BrsarPath, "rb")
			if(Songs[SongSelected].SongType == SongTypeValue.Regular):
				brsar.seek(int('33A84',16)+24*Songs[SongSelected].MemOrder*2)
				offset1 = brsar.read(4)
				offset2 = brsar.read(4)
				brsar.seek(int('33A84',16)+24*(Songs[SongSelected].MemOrder*2+1))
				offset3 = brsar.read(4)
				offset4 = brsar.read(4)
				brsar.seek(0)
				data1 = brsar.read(int('5F6620',16)+int.from_bytes(offset1,'big'))
				brsar.seek(int('5F6620',16)+int.from_bytes(offset1,'big')+int.from_bytes(offset2,'big'))
				data2 = brsar.read(int.from_bytes(offset3,'big')-int.from_bytes(offset1,'big')-int.from_bytes(offset2,'big'))
				brsar.seek(int('5F6620',16)+int.from_bytes(offset3,'big')+int.from_bytes(offset4,'big'))
				data3 = brsar.read()
				brsar.close()
				brsar = open(BrsarPath, "wb")
				brsar.write(data1+BrseqInfo[0]+data2+BrseqInfo[1]+data3)
				brsar.close()
				brsar = open(BrsarPath, "r+b")
				brsar.seek(int('33A88',16)+24*Songs[SongSelected].MemOrder*2)
				sizeDifference = int(BrseqLength[0],16)-int.from_bytes(brsar.read(4),"big")
				brsar.seek(int('33A88',16)+24*Songs[SongSelected].MemOrder*2)
				brsar.write(int(BrseqLength[0],16).to_bytes(4, 'big'))
				EditBrsarOffset(int('33A84',16)+24*(Songs[SongSelected].MemOrder*2+1))
				brsar.seek(int('33A88',16)+24*(Songs[SongSelected].MemOrder*2+1))
				sizeDifference += int(BrseqLength[1],16)-int.from_bytes(brsar.read(4),"big")
				brsar.seek(int('33A88',16)+24*(Songs[SongSelected].MemOrder*2+1))
				brsar.write(int(BrseqLength[1],16).to_bytes(4, 'big'))
				#Resize All Song Offsets
				for num in range((Songs[SongSelected].MemOrder+1)*2,100):
					EditBrsarOffset(int('33A84',16)+24*num)

				for offset in ['8','33748','343F0','343F8','359FC','35A04','35A68','35A70','35AD4','35ADC','35B40','35B48','35BCC','35BD4',
				'35C38','35C40','35CA4','35CAC','35D30','35D38','35DBC','35DC4','35E28','35E30','35EB4','35EBC','35F20','35F28','35F8C','35F94',
				'36018','36020','36064','3606C','360D0','360D8','3705C','37064','370E8','370F0','371F4','371FC',
				'37340','37348','376CC','376D4','37738','37740','3374C',
				'37784','3778C','379D0','379D8','37ABC','37AC4','37B48','37B50','37BB4','37BBC','37C20','37C28','37C8C','37C94','37D18','37D20',
				'37D64','37D6C','37E70','37E78','37EBC','37EC4','37F48','37F50']:
					EditBrsarOffset(int(offset,16))
				brsar.close()
				AddPatch(Songs[SongSelected].Name+' Song Patch',LengthCode+TempoCode+TimeCode)
			elif(Songs[SongSelected].SongType == SongTypeValue.Menu):
				offset = [0]*14
				data = [0]*8
				for num in range(7):
					brsar.seek(int('37DBC',16)+24*num)
					offset[num*2] = brsar.read(4)
					offset[num*2+1] = brsar.read(4)
				brsar.seek(int('37D64',16))
				currentSpot = int.from_bytes(brsar.read(4),'big')
				brsar.seek(0)
				data[0] = brsar.read(currentSpot+int.from_bytes(offset[0],'big'))
				for num in range(6):
					brsar.seek(currentSpot+int.from_bytes(offset[num*2],'big')+int.from_bytes(offset[num*2+1],'big'))
					data[num+1] = brsar.read(int.from_bytes(offset[num*2+2],'big')-int.from_bytes(offset[num*2],'big')-int.from_bytes(offset[num*2+1],'big'))
				brsar.seek(currentSpot+int.from_bytes(offset[12],'big')+int.from_bytes(offset[13],'big'))
				data[7] = brsar.read()
				brsar.close()
				brsar = open(BrsarPath, "wb")
				brsar.write(data[0]+BrseqInfo[0]+data[1]+BrseqInfo[1]+data[2]+BrseqInfo[1]+data[3]+BrseqInfo[1]+data[4]+BrseqInfo[1]+data[5]+BrseqInfo[1]+data[6]+BrseqInfo[1]+data[7])
				brsar.close()
				brsar = open(BrsarPath, "r+b")
				brsar.seek(int('37DC0',16))
				sizeDifference = int(BrseqLength[0],16)-int.from_bytes(brsar.read(4),"big")
				brsar.seek(int('37DC0',16))
				brsar.write(int(BrseqLength[0],16).to_bytes(4, 'big'))
				for num in range(1,7):
					EditBrsarOffset(int('37DBC',16)+24*num)
					brsar.seek(int('37DC0',16)+24*num)
					sizeDifference += int(BrseqLength[1],16)-int.from_bytes(brsar.read(4),"big")
					brsar.seek(int('37DC0',16)+24*num)
					brsar.write(int(BrseqLength[1],16).to_bytes(4, 'big'))
				for offset in ['8','37D68','37D6C','37E70','37E78','37EBC','37EC4','37F48','37F50']:
					EditBrsarOffset(int(offset,16))
				brsar.close()
			AddPatch('Rapper Crash Fix','043B0BBB 881C0090\n043B0BBF 7C090000\n043B0BC3 4081FFBC\n043B0BC7 881C00D6\n')
			print("\nPatch Complete!")
			time.sleep(0.5)
			if(DefaultReplaceSongNames != 'No') and (SongSelected != 50) and ((DefaultReplaceSongNames == 'Yes') or (input('\nWould you like to change the Song Text? [y/n] ') == 'y')):
				ChangeName(SongSelected,[input('\nWhat\'s the title of your Song: '),input('\nWhat\'s the description of your Song (Use \\n for new lines): '),input('\nWhat\'s the genre of your Song: ')])
				print("\nEditing Successful!\n")
			else: print('')
		else:
			print("Aborted...")
	elif(Selection == 2): #////////////////////////////////////////Change Song Names
		#Load Files
		FindGameFolder()

		#Song List
		PrintSectionTitle("Song List")
		for num in range(len(Songs)):
			print('(#'+str(num)+') '+str(Songs[num].Name))
			time.sleep(0.005)

		#Song Selection
		PrintSectionTitle("Song Selection")
		Selection = MakeSelection(['\nWhich Song Do You Want To Change The Name Of',0,len(Songs)-1])
		
		ChangeName(Selection,[input('\nWhat\'s the title of your Song: '),input('\nWhat\'s the description of your Song (Use \\n for new lines): '),input('\nWhat\'s the genre of your Song: ')])
		print("\nEditing Successful!\n")
	elif(Selection == 3): #////////////////////////////////////////Change Style
		FindDolphinSave()
		MenuStyles = 5
		columnSplit = 4
		MaxStyles = []
		StyleTable = [[['Global Styles','Song Specific Styles','Quick Jam Styles','Menu Styles']],[['Replace All Styles']]]
		for num in range(ceil(NumberOfStyleTypes/columnSplit)):
			MaxStyles.append([0]*min(columnSplit,NumberOfStyleTypes-num*columnSplit))
		print('')
		for num in range(len(Styles)):
			number = Styles[num].StyleType
			array = 0
			while(number >= columnSplit):
				array += 1
				number -= columnSplit
			MaxStyles[array][number] += 1
			if(MaxStyles[array][number] >= len(StyleTable[array])):
				StyleTable[array].append(['']*min(columnSplit,NumberOfStyleTypes-array*columnSplit))
			StyleTable[array][MaxStyles[array][number]][number] = '(#'+str(num)+') '+Styles[num].Name
		while(len(StyleTable[floor(NumberOfStyleTypes/columnSplit)]) <= 2):
			StyleTable[floor(NumberOfStyleTypes/columnSplit)].append(['']*(NumberOfStyleTypes-floor(NumberOfStyleTypes/columnSplit)*columnSplit))
		StyleTable[floor(NumberOfStyleTypes/columnSplit)][1][NumberOfStyleTypes-floor(NumberOfStyleTypes/columnSplit)*columnSplit-1] = '(#'+str(len(Styles))+') Replace All Non-Menu Styles'
		StyleTable[floor(NumberOfStyleTypes/columnSplit)][2][NumberOfStyleTypes-floor(NumberOfStyleTypes/columnSplit)*columnSplit-1] = '(#'+str(len(Styles)+1)+') Replace All Menu Styles'
		for num in range(len(StyleTable)):
			print(tabulate(StyleTable[num], headers='firstrow'))
			print('')
		Selection = MakeSelection(['What\'s the Style Number you want to change',0,len(Styles)+2])
		NormalStyleSelected = (Selection < len(Styles)-MenuStyles) or (Selection == len(Styles))
		PrintSectionTitle("Instrument List")
		normalInstrumentNumber = 40
		
		if(not unsafeMode):
			for num in range(normalInstrumentNumber+1):
				realNum = num
				if(num == normalInstrumentNumber):
					num = len(Instruments)-1
				if (not Instruments[num].InMenu) and (not NormalStyleSelected):
					print(Fore.RED+'(UNAVALIBLE) '+str(Instruments[num].Name)+Style.RESET_ALL)
				else:
					print('(#'+str(realNum)+') '+str(Instruments[num].Name))
				time.sleep(0.005)
		else:
			for num in range(len(Instruments)):
				if ((Instruments[num].InMenu) and (not NormalStyleSelected) and (num < normalInstrumentNumber)) or (((num < normalInstrumentNumber) or (num == len(Instruments)-1)) and (NormalStyleSelected)):
					print(Style.RESET_ALL+'(#'+str(num)+') '+str(Instruments[num].Name))
				elif (unsafeMode):
					if((Instruments[num].InMenu) and (not NormalStyleSelected)) or (NormalStyleSelected):
						print(Fore.YELLOW+'(#'+str(num)+') '+str(Instruments[num].Name)+Style.RESET_ALL)
					else:
						print(Fore.RED+'(#'+str(num)+') '+str(Instruments[num].Name)+Style.RESET_ALL)
				time.sleep(0.005)
		PrintSectionTitle("Instrument Selection")
		Melody = SelectStyleInstrument('Melody',False)
		Harmony = SelectStyleInstrument('Harmony',False)
		Chord = SelectStyleInstrument('Chord',False)
		Bass = SelectStyleInstrument('Bass',False)
		PrintSectionTitle("Instrument List")
		if(not unsafeMode):
			for num in range(40,len(Instruments)):
				if (not Instruments[num].InMenu) and (not NormalStyleSelected):
					print(Fore.RED+'(UNAVALIBLE) '+Instruments[num].Name+Style.RESET_ALL)
				else:
					print('(#'+str(num-40)+') '+Instruments[num].Name)
				time.sleep(0.005)
		else:
			for num in range(len(Instruments)):
				if ((Instruments[num].InMenu) and (not NormalStyleSelected) and (num >= normalInstrumentNumber)) or (((num >= normalInstrumentNumber) or (num == len(Instruments)-1)) and (NormalStyleSelected)):
					print(Style.RESET_ALL+'(#'+str(num)+') '+Instruments[num].Name)
				elif (unsafeMode):
					if((Instruments[num].InMenu) and (not NormalStyleSelected)) or (NormalStyleSelected):
						print(Fore.YELLOW+'(#'+str(num)+') '+Instruments[num].Name+Style.RESET_ALL)
					else:
						print(Fore.RED+'(#'+str(num)+') '+Instruments[num].Name+Style.RESET_ALL)
				time.sleep(0.005)

		Perc1 = SelectStyleInstrument('Percussion 1',True)
		Perc2 = SelectStyleInstrument('Percussion 2',True)

		if(Selection == len(Styles)):
			PatchName = []
			PatchInfo = []
			for num in range(len(Styles)-MenuStyles):
				PatchName.append(Styles[num].Name+' Style Patch')
				PatchInfo.append(Styles[num].MemOffset+' 00000018\n'+Melody+' '+Harmony+'\n'+Chord+' '+Bass+'\n'+Perc1+' '+Perc2+'\n')
			AddPatch(PatchName,PatchInfo)
		elif(Selection >= len(Styles)-MenuStyles):
			PatchName = []
			PatchInfo = []
			for num in range(len(Styles)-MenuStyles,len(Styles)):
				PatchName.append(Styles[num].Name+' Style Patch')
				PatchInfo.append(Styles[num].MemOffset+' 00000018\n'+Melody+' '+Harmony+'\n'+Chord+' '+Bass+'\n'+Perc1+' '+Perc2+'\n')
			AddPatch(PatchName,PatchInfo)
		else:
			AddPatch(Styles[Selection].Name+' Style Patch',Styles[Selection].MemOffset+' 00000018\n'+Melody+' '+Harmony+'\n'+Chord+' '+Bass+'\n'+Perc1+' '+Perc2+'\n')

		print("\nPatch Complete!")
		time.sleep(0.5)
		print("")
	elif(Selection == 4): #////////////////////////////////////////Advanced Tools
		while True:
			PrintSectionTitle('Advanced Tools')
			print("(#0) Back to Main Menu")
			print("(#1) Change All Wii Music Text")
			print("(#2) Remove Song")
			print("(#3) Import/Export Files")
			print("(#4) Extract/Pack Wii Music ROM")
			print("(#5) Patch Main.dol With Gecko Codes")
			print("(#6) Create Riivolution Patch")

			Selection = MakeSelection(['Please Select an Option',0,6])

			if(Selection == 1): #////////////////////////////////////////Change Text
				#Load Files
				FindGameFolder()
				
				#Run Notepad
				subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/decode.bat\" '+MessageFolder(),capture_output=True)
				time.sleep(0.5)
				print("\nWaiting for Notepad to close...")
				subprocess.run('notepad \"'+MessageFolder().replace('\"','')+'/message.d/new_music_message.txt\"',capture_output=True)
				subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/encode.bat\" '+MessageFolder(),capture_output=True)
				print("\nEditing Successful!\n")
			elif(Selection == 2): #////////////////////////////////////////Remove Song
				FindGameFolder()
				FindDolphinSave()
				PrintSectionTitle('Remove Song')
				for num in range(len(Songs)-1):
					print('(#'+str(num)+') '+str(Songs[num].Name))
					time.sleep(0.005)
				print('(#'+str(len(Songs)-1)+') Remove All Non-Custom Songs')
				
				Selection = MakeSelection(['Please Select a Song to Remove',0,len(Songs)-1])

				if(Selection == len(Songs)-1):
					appliedCustomSongs = []
					if(os.path.isfile(GamePath+'/GeckoCodes.ini')):
						codes = open(GamePath+'/GeckoCodes.ini')
						textlines = codes.readlines()
						codes.close()
						for text in textlines:
							if('[WiiMusicEditor]' in text) and ('Style' not in text):
								appliedCustomSongs.append(text[1:len(text)-29:1])
				
				for number in range(len(Songs)-2):
					if(Selection != len(Songs)-1):
						number = Selection
					
					if((Selection != len(Songs)-1) or (Songs[number].Name not in appliedCustomSongs)):
						#Brsar Writing
						brsar = open(GamePath+'/sys/main.dol', "r+b")
						brsar.seek(int(MainDolOffset,16)+6+int("BC",16)*Songs[number].MemOrder)
						brsar.write(bytes.fromhex('ffffffffffff'))
						brsar.close()

					if(Selection != len(Songs)-1): break

				print('\nEradication Complete!')
			elif(Selection == 3): #////////////////////////////////////////Import/Export Files
				while True:
					PrintSectionTitle('Import/Export Files')
					print("(#0) Back To Main Menu")
					print("(#1) Import Files")
					print("(#2) Export Files to .zip")
					print("(#3) Export Files to Folder")

					Selection = MakeSelection(['Choose an Option',0,3])
					if(Selection == 1):
						while True:
							importDir = input("\nDrag Wii Music files you want to import [.brsar, .carc, .dol, .ini, .gct, .zip, folder]: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
							if(os.path.isdir(importDir)) or (pathlib.Path(importDir).suffix in ['.brsar','.carc','.dol','.ini','.gct','.zip']):
								if(pathlib.Path(importDir).suffix == '.zip'):
									with tempfile.TemporaryDirectory() as directory:
										with zipfile.ZipFile(importDir, 'r') as zip_ref:
											zip_ref.extractall(directory)
											LoadNewFile(directory)
								else:
									LoadNewFile(importDir)
								break
							else:
								print('\nERROR: Bad Filetype')
					
					elif(Selection == 0): break
					else:
						name = os.path.dirname(GamePath)+" Extracted Files"
						number = ""
						num = 0
						while(os.path.isdir(name+number) and Selection == 3) or (os.path.isfile(name+number+".zip") and Selection == 2):
							num = num+1
							number = " ("+str(num)+")"
						name = name+number
						if(Selection == 3) and (not os.path.isdir(name)): os.mkdir(name)
						if(Selection == 2): zipObj = zipfile.ZipFile(name+'.zip', 'w')
						md5_hash = hashlib.md5()
						a_file = open(GamePath+'/files/Sound/MusicStatic/rp_Music_sound.brsar', "rb")
						content = a_file.read()
						a_file.close()
						md5_hash.update(content)
						if(brsarChecksum != md5_hash.hexdigest()):
							if(Selection == 3):
								copyfile(GamePath+'/files/Sound/MusicStatic/rp_Music_sound.brsar',name+'/rp_Music_sound.brsar')
							else:
								zipObj.write(GamePath+'/files/Sound/MusicStatic/rp_Music_sound.brsar','rp_Music_sound.brsar')
						md5_hash = hashlib.md5()
						a_file = open(GamePath+'/files/US/Message/message.carc', "rb")
						content = a_file.read()
						a_file.close()
						md5_hash.update(content)
						if(messageChecksum != md5_hash.hexdigest()):
							if(Selection == 3):
								copyfile(GamePath+'/files/US/Message/message.carc',name+'/message.carc')
							else:
								zipObj.write(GamePath+'/files/US/Message/message.carc','message.carc')
						md5_hash = hashlib.md5()
						a_file = open(GamePath+'/sys/main.dol', "rb")
						content = a_file.read()
						a_file.close()
						md5_hash.update(content)
						if(mainDolChecksum != md5_hash.hexdigest()):
							if(Selection == 3):
								copyfile(GamePath+'/sys/main.dol',name+'/main.dol')
							else:
								zipObj.write(GamePath+'/sys/main.dol','main.dol')
						if(os.path.isfile(GamePath+'/GeckoCodes.ini')):
							if(Selection == 3):
								copyfile(GamePath+'/GeckoCodes.ini',name+'/GeckoCodes.ini')
							else:
								zipObj.write(GamePath+'/GeckoCodes.ini','GeckoCodes.ini')
							CreateGct()
							if(Selection == 3):
								os.rename(ProgramPath+'/R64E01.gct',name+'/R64E01.gct')
							else:
								zipObj.write(ProgramPath+'/R64E01.gct','R64E01.gct')
								os.remove(ProgramPath+'/R64E01.gct')
						if(Selection == 2):
							zipObj.close()
							name = name+'.zip'
						print('\nExport Complete!\nSaved to: '+name)
			elif(Selection == 4): #////////////////////////////////////////Extract/Pack Wii Music ROM
				while True:
					PrintSectionTitle('Extract/Pack Wii Music ROM')
					print("(#0) Back To Advanced Tools")
					print("(#1) Extract ROM Filesystem")
					print("(#2) Pack Filesystem to .wbfs")
					print("(#3) Pack Filesystem to .iso")

					Selection = MakeSelection(['Choose an Option',0,3])
					if(Selection == 1):
						ExceptedFileExtensions = ['.iso','.wbfs']
						while True:
							DiskPath = input("\nPlease Drag the Wii Music Disk: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
							if(os.path.isfile(DiskPath)) and (pathlib.Path(DiskPath).suffix in ExceptedFileExtensions):
								break
							else:
								print('ERROR: Not Supported File Type')
						subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/wit.exe\" cp --fst \"'+DiskPath+'\" \"'+os.path.dirname(DiskPath)+"/"+os.path.splitext(os.path.basename(DiskPath))[0]+'\"')
						if(input('\nWould You Like to Set This Path as the Current Game Path? [y/n] ') == 'y'):
							GamePath = os.path.dirname(DiskPath).replace('\\','/')+'/'+os.path.splitext(os.path.basename(DiskPath))[0]+'/DATA'
							BrsarPath = GamePath+'/files/sound/MusicStatic/rp_Music_sound.brsar'
							MessagePath = GamePath+'/files/US/Message/message.carc'
							SaveSetting('Paths','GamePath',GamePath)
					elif(Selection == 2) or (Selection == 3):
						if(input('\nUse Game Path as Disk Directory? [y/n] ') != 'y'):
							while True:
								DiskPath= input("\nDrag Decompressed Wii Music Directory: ").replace('&', '').replace('\'', '').replace('\"', '').strip()
								if(os.path.isdir(DiskPath+'/DATA')):
									break
								else:
									print("\nERROR: Unable to Locate Valid Wii Music Directory")
						else:
							FindGameFolder()
							if(GamePath[len(GamePath)-4:len(GamePath):1] == 'DATA'):
								DiskPath = GamePath[0:len(GamePath)-5:1]
							else:
								DiskPath = GamePath
						
						DiskName = ''
						DiskNum = 0
						if(Selection == 2):
							while(os.path.isfile(DiskPath+DiskName+'.wbfs')):
								DiskNum = DiskNum+1
								DiskName = '('+str(DiskNum)+')'
							subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/wit.exe\" cp \"'+DiskPath+'\" \"'+DiskPath+DiskName+'.wbfs\" --wbfs')
						else:
							while(os.path.isfile(DiskPath+DiskName+'.iso')):
								DiskNum = DiskNum+1
								DiskName = '('+str(DiskNum)+')'
							subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/wit.exe\" cp \"'+DiskPath+'\" \"'+DiskPath+DiskName+'.iso\" --iso')
					else: break
					print('')
			elif(Selection == 5): #////////////////////////////////////////Patch Main.dol
				FindGameFolder()
				FindDolphinSave()
				if(input('\nAre you sure you want to patch Main.dol? [y/n] ') == 'y'):
					if(os.path.isfile(GamePath+'/GeckoCodes.ini')):
						print('\nCreating Gct...')
						CreateGct()
						print('\nPatching Main.dol...')
						subprocess.run('\"'+ProgramPath+'/Helper/Wiimms/wstrt.exe\" patch \"'+GamePath+'/sys/main.dol\" --add-section \"'+ProgramPath+'/R64E01.gct --force\"',capture_output=True)
						os.remove(ProgramPath+'/R64E01.gct')
						print('\nPatch Successful!')
					else:
						print('\nNo Gecko Codes Found')
			elif(Selection == 6): #////////////////////////////////////////Riivolution Patch
				PrintSectionTitle('Riivolution Patch')
				FindGameFolder()
				FindDolphinSave()
				if(GamePath[len(GamePath)-4:len(GamePath):1] == 'DATA'):
					ModPath = GamePath[0:len(GamePath)-5:1]
					ModPath = ModPath[0:len(ModPath)-len(os.path.basename(ModPath)):1]
				else:
					ModPath = GamePath[0:len(GamePath)-len(os.path.basename(GamePath)):1]
				ModName = input('\nPlease Input Mod Name: ')
				while (os.path.isdir(ModPath+ModName)):
					ModName = input('\nDirectory Already Exists! Please Enter a Diffrent Name: ')
				ModPath = ModPath+ModName
				os.mkdir(ModPath)
				os.mkdir(ModPath+'/Riivolution')
				os.mkdir(ModPath+'/Riivolution/codes')
				os.mkdir(ModPath+'/'+ModName.replace(' ',''))
				print('\nMaking Gct...')
				CreateGct()
				print('\nCopying Files...')
				copyfile(GamePath+'/files/Sound/MusicStatic/rp_Music_sound.brsar',ModPath+'/'+ModName.replace(' ','')+'/rp_Music_sound.brsar')
				copyfile(GamePath+'/files/US/Message/message.carc',ModPath+'/'+ModName.replace(' ','')+'/message.carc')
				copyfile(ProgramPath+'/Helper/GctFiles/codehandler.bin',ModPath+'/Riivolution/codehandler.bin')
				os.rename(ProgramPath+'/R64E01.gct',ModPath+'/Riivolution/codes/R64E01.gct')
				print('\nCreating XML file...')
				linestowrite = [
				'<wiidisc version="1" root="">\n',
				'  <id game="R64" />\n',
				'  <options>\n',
				'    <section name="'+ModName+'">\n',
				'      <option name="Load Mod">\n',
				'        <choice name="Enabled">\n',
				'          <patch id="TheMod" />\n',
				'        </choice>\n',
				'      </option>\n',
				'    </section>\n',
				'  </options>\n',
				'  <patch id="TheMod">\n',
				'    <file disc="/Sound/MusicStatic/rp_Music_sound.brsar" external="/'+ModName.replace(' ','')+'/rp_Music_sound.brsar" offset="" />\n',
				'    <file disc="/US/Message/message.carc" external="/'+ModName.replace(' ','')+'/message.carc" offset="" />\n',
				'    <memory valuefile="codehandler.bin" offset="0x80001800" />\n',
				'    <memory value="8000" offset="0x00001CDE" />\n',
				'    <memory value="28B8" offset="0x00001CE2" />\n',
				'    <memory value="8000" offset="0x00001F5A" />\n',
				'    <memory value="28B8" offset="0x00001F5E" />\n',
				'    <memory valuefile="/codes/R64E01.gct" offset="0x800028B8" />\n',
				'  </patch>\n',
				'</wiidisc>\n']
				xml = open(ModPath+'/Riivolution/'+ModName.replace(' ','')+'.xml','w')
				xml.writelines(linestowrite)
				xml.close()
				print('\nPatch Creation Successful!\nExported to: '+ModPath)
				if(input('\nWould You Like to Copy the Patch on to an SD card? [y/n] ') == 'y'):
					letter = input('\nType the Drive Letter of the SD card: ')
					print('\nCopying...')
					copytree(ModPath+'/Riivolution',letter+':/Riivolution')
					copytree(ModPath+'/'+ModName.replace(' ',''),letter+':/'+ModName.replace(' ',''))
					print('\nSuccessfully Copied!')
			else: break
	elif(Selection == 5): #////////////////////////////////////////Run Game
		FindGameFolder()
		FindDolphin()
		PrintSectionTitle("Running Dolphin")
		if(os.path.isfile(GamePath+'/GeckoCodes.ini')):
			if(os.path.isfile(CodePath)): os.remove(CodePath)
			copyfile(GamePath+'/GeckoCodes.ini',CodePath)
		subprocess.Popen('\"'+DolphinPath+'\" -b -e \"'+GamePath+'/sys/main.dol\"')
		time.sleep(1)
		print("")
	elif(Selection == 6): #////////////////////////////////////////Revert Changes
		while True:
			PrintSectionTitle('Revert Changes')
			print("(#0) Back to Main Menu")
			print("(#1) Revert Songs")
			print("(#2) Revert Text")
			print("(#3) Revert Styles")
			print("(#4) Revert Main.dol")
			print("(#5) Revert All")

			Selection = MakeSelection(['Select An Option',0,5])

			if(Selection != 0):
				for num in range(1,5):
					if(Selection != 5):
						num = Selection

					if(num == 1):
						if(os.path.isfile(GamePath+'/GeckoCodes.ini')):
							codes = open(GamePath+'/GeckoCodes.ini')
							textlines = codes.readlines()
							codes.close()
							linenum = 0
							while linenum < len(textlines):
								if('Song' in textlines[linenum]):
									textlines.pop(linenum)
									while(len(textlines) > linenum) and (textlines[linenum][0].isnumeric() or textlines[linenum][0].isalpha()):
										textlines.pop(linenum)
								else:
									linenum = linenum+1					
							codes = open(GamePath+'/GeckoCodes.ini','w')
							codes.writelines(textlines)
							codes.close()
						if(os.path.isfile(ProgramPath+"/Helper/Backup/rp_Music_sound.brsar")):
							os.remove(BrsarPath)
							copyfile(ProgramPath+"/Helper/Backup/rp_Music_sound.brsar",BrsarPath)
							print('\nSongs Reverted')
						else:
							print('\nERROR: Backup not found')
					elif(num == 2):
						if(os.path.isfile(ProgramPath+"/Helper/Backup/message.carc")):
							os.remove(MessagePath)
							copyfile(ProgramPath+"/Helper/Backup/message.carc",MessagePath)
							print('\nText Reverted')
						else:
							print('\nERROR: Backup not found')
					elif(num == 3):
						if(os.path.isfile(GamePath+'/GeckoCodes.ini')):
							codes = open(GamePath+'/GeckoCodes.ini')
							textlines = codes.readlines()
							codes.close()
							for linenum in range(len(textlines)):
								if(linenum < len(textlines)):
									if('Style' in textlines[linenum]):
										textlines.pop(linenum)
										while(len(textlines) > linenum) and (textlines[linenum][0].isnumeric() or textlines[linenum][0].isalpha()):
											textlines.pop(linenum)
							codes = open(GamePath+'/GeckoCodes.ini','w')
							codes.writelines(textlines)
							codes.close()
						print('\nStyles Reverted')
					elif(num == 4):
						if(os.path.isfile(ProgramPath+"/Helper/Backup/main.dol")):
							os.remove(GamePath+'/sys/main.dol')
							copyfile(ProgramPath+"/Helper/Backup/main.dol",GamePath+'/sys/main.dol')
							print('\nMain.dol Reverted')
						else:
							print('\nERROR: Backup not found')

					if(Selection != 5): break
			else: break
	elif(Selection == 7): #////////////////////////////////////////100% Save File
		FindDolphinSave()
		if(input("\nAre You Sure You Want To Overwrite Your Save Data? [y/n] ") == 'y'):
			subprocess.run('robocopy \"'+ProgramPath+'/Helper/WiiMusicSave\" \"'+SaveDataPath+'\" /MIR /E',capture_output=True)
			print("\nOverwrite Successfull\n")
		else:
			print("\nAborted...\n")
	elif(Selection == 8): #////////////////////////////////////////Download Pre-Made Custom Songs
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
	elif(Selection == 9): #////////////////////////////////////////Help
		PrintSectionTitle('Help')
		print("(#0) Back to Main Menu")
		print("(#1) Open the Wiki")
		print("(#2) Open Video Guide")
		
		Selection = MakeSelection(['What type of help do you want',0,2])

		if(Selection == 1):
			print('\nOpening Wiki...')
			time.sleep(0.5)
			webbrowser.open('https://github.com/BenjaminHalko/WiiMusicEditor/wiki')
		elif(Selection == 2):
			print('\nOpening Video Guide...')
			time.sleep(0.5)
			webbrowser.open('https://youtu.be/EBz9VtBXqEo')
		print('')
		time.sleep(0.5)
	elif(Selection == 10): #////////////////////////////////////////Settings
		while True:
			PrintSectionTitle("Settings")
			print("(#0) Back To Main Menu")
			print("(#1) Change File Paths")
			print("(#2) Other Settings")
			print("(#3) Updates")
			if(unsafeMode):
				print("(#4) Switch to Safe Mode")
			else:
				print("(#4) Switch to Unsafe Mode")

			Selection = MakeSelection(['Which Setting Do You Want to Change',0,4])

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
					PrintSectionTitle('Specific Settings')
					print("(#0) Back To Settings")
					print("(#1) Replace Song and Score Files Seperatly: "+DefaultLoadSongScore)
					print("(#2) Replace Song Warnings: "+DefaultWantToReplaceSong)
					print("(#3) Warm User When Replacing Already Replaced Song: "+DefaultReplacingReplacedSong)
					print("(#4) Use Auto Found Length and Tempo: "+DefaultUseAutoLengthTempo)
					print("(#5) Replace Song Names After Adding Custom Song: "+DefaultReplaceSongNames)

					Selection = MakeSelection(['Choose an Option',0,5])
					if(Selection == 1):
						DefaultLoadSongScore = ChangeDefaultAnswer(['Yes','No'],['Load Song And Score',DefaultLoadSongScore])
					elif(Selection == 2):
						DefaultWantToReplaceSong = ChangeDefaultAnswer(['Yes','No'],['Want To Replace Song',DefaultWantToReplaceSong])
					elif(Selection == 3):
						DefaultReplacingReplacedSong = ChangeDefaultAnswer(['Yes','No'],['Replacing Replaced Song',DefaultReplacingReplacedSong])
					elif(Selection == 4):
						DefaultUseAutoLengthTempo = ChangeDefaultAnswer(['Ask','Yes','No'],['Use Auto Length and Tempo'])
					elif(Selection == 5):
						DefaultReplaceSongNames = ChangeDefaultAnswer(['Ask','Yes','No'],['Replace Song Names'])
					else: break
			elif(Selection == 3):
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
			elif(Selection == 4):
				if((not unsafeMode) and (input('\nAre You Sure You Want to Turn on Unsafe Mode? [y/n] ') == 'y')) or (unsafeMode):
					unsafeMode = not unsafeMode
					SaveSetting('Unsafe Mode','Unsafe Mode',str(int(unsafeMode)))
				print('')
			else: break
	elif(Selection == 11): #////////////////////////////////////////Credits
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