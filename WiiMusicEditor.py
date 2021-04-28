import os
import sys
import getpass
import time

#Default Paths
RootDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
BrsarPath = os.path.join(RootDir,'DATA/files/Sound/MusicStatic/rp_Music_sound.brsar')
codePath = "C:/Users/"+getpass.getuser()+"/Documents/Dolphin Emulator/GameSettings/R64E01.ini"

#Functions
def AddPatch(PatchName,PatchInfo):
	global codePath
	if(os.path.exists(codePath)):
		codes = open(codePath,'r')
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
		
		codes = open(codePath,'w')
		codes.writelines(lineText)
		codes.close()
	else:
		codes = open(codePath,'w')
		codes.write('[Gecko]\n')
		codes.write('$'+PatchName+' [WiiMusicEditor]\n')
		codes.write(PatchInfo)
		codes.write('[Gecko_Enabled]\n')
		codes.write('$'+PatchName+'\n')
		codes.close()

def FindBrsar():
	global RootDir
	global BrsarPath
	if(not os.path.isfile(BrsarPath)):
		if(RootDir != '2'):
			print("\nERROR: Unable to Locate rp_Music_sound.brsar")
		while True:
			BrsarPath = input("\nPlease Type In Location Of rp_Music_sound.brsar: ")
			if(os.path.isfile(BrsarPath)):
				break
			elif (os.path.isfile(os.path.join(BrsarPath,'rp_Music_sound.brsar'))):
				BrsarPath = os.path.join(BrsarPath,'rp_Music_sound.brsar')
				break
			else:
				print("\nERROR: Unable to Locate rp_Music_sound.brsar")

#Song Names
SongNames = [
'A Little Night Music',
'American Patrol',
'Animal Crossing',
'Animal Crossing K.K. Blues',
'Bridal Chrous',
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
'Ive Never Been To Me',
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
'Please Mr.Postman',
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
'Yankee Doodle']

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
'61F620']

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
'620F60']

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
'1940']

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
'1880']

LengthMemoryOffsets = [
'025a08ae',
'025a0c5a',
'025a2786',
'025a175e',
'025a0502',
'025a067a',
'025a1dfa',
'025a1c82',
'025a0ae2',
'025a1d3e',
'025a2842',
'025a146e',
'025a181a',
'025a1006',
'', #happybirthday
'', #illbethere
'025a2496',
'025a231e',
'025a10c2',
'025a1992',
'025a16a2',
'025a123a',
'025a202e',
'025a096a',
'025a0f4a',
'025a15e6',
'', #odetojoy
'025a0e8e',
'', #overthewaves
'025a1f72',
'', #sakurasakura
'', #scarbouroghfair
'025a1eb6',
'025a1bc6',
'', #supermariobros
'025a13b2',
'025a05be',
'025a07f2',
'025a0b9e',
'025a152a',
'025a260e',
'025a20ea',
'025a18d6',
'', #turkeystraw
'025a12f6',
'025a23da',
'025a0736',
'025a26ca',
'',
'025a0dd2']

TempoMemoryOffsets = [
'025a08b3',
'025a0c5e',
'025a278a',
'025a1763',
'025a0506',
'025a067e',
'025a1dfe',
'025a1c86',
'025a0ae6',
'025a1d42',
'025a2846',
'025a1472',
'025a181e',
'025a100a',
'',
'',
'025a249a',
'025a2322',
'025a10c6',
'025a1996',
'025a16a6',
'025a123e',
'025a2032',
'025a096e',
'025a0f4e',
'025a15ea',
'',
'025a0e92',
'',
'025a1f76',
'',
'',
'025a1eba',
'025a1bca',
'',
'025a13b6',
'025a05c2',
'025a07f6',
'025a0ba2',
'025a152e',
'025a2612',
'025a20ee',
'025a18da',
'',
'025a12fa',
'025a23de',
'025a073a',
'025a26ce',
'',
'025a0dd6']

TimeSignatureMemoryOffsets = [
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
'',
'',
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
'',
'025a1f6c',
'',
'',
'025a1eb0',
'025a1bc0',
'',
'025a13ac',
'025a05b8',
'025a07ec',
'025a0b98',
'025a1524',
'025a2608',
'025a20e4',
'025a18d0',
'',
'025a12f0',
'025a23d4',
'025a0730',
'025a26c4',
'',
'025a0dcc']

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
'Reggae']

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
'0659A7A3']

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

#Check For Wii Music Directory
if(not(os.path.isdir(RootDir+'/DATA'))):
	print("ERROR: Can't Find Root of Wii Music Disk!\nThis Program's Folder Should Be In The Root Directory of the Wii Music Disk\n(The Directory with DATA and UPDATE)]")
	while True:
		print("\n//////////////////// What Would You Like To Do?")
		print("0: Quit & Move the Program Folder to the Root Directory")
		print("1: Manually Locate Wii Music Directory")
		print("2: Locate Individual Wii Music Files")	
		RootDir = input("\nType Your Selection: ")
		if(RootDir == '0'):
			quit()
			break
		elif (RootDir == '1'):
			RootDir = input("\nPlease Type In Path To Wii Music Directory: ")
			if((os.path.isdir(os.path.join(RootDir,'DATA')))):
				break
			else:
				print("\nERROR: Invalid Directory!\nPlease Point To The Directory With DATA & UPDATE!")
		elif (RootDir == '2'):
			break
		else:
			print("\nERROR: Unavalible Option")

while True:
	#Options
	print("//////////////////////////////")
	print("//                          //")
	print("//        Welcome To        //")
	print("//         The Wii          //")
	print("//       Music Editor       //")
	print("//                          //")
	print("//////////////////////////////\n")
	print("//////////////////// Options")
	print("(#1) Add Custom Song To Wii Music")
	print("(#2) Change Song Name (Coming Soon)")
	print("(#3) Change Style\n")
	while True:
		mode = input("Please Select An Option: ")
		if(mode == '1') or (mode == '2') or (mode == '3'):
			break
		else:
			print("ERROR: Not a Valid Option!\n")

	if(mode == '1'):
		#Check For Brsar
		FindBrsar()

		#Load Brseq
		if(len(sys.argv) < 2):
			BrseqPath = ''
		else: BrseqPath = sys.argv[1]
		if(not BrseqPath[len(BrseqPath)-6:len(BrseqPath):1].lower() == '.brseq'):
			while True:
				BrseqPath = input("\nPlease Enter Path To .Brseq (Or Drag It On The .Bat File): ")
				if(os.path.isfile(BrseqPath)) and (BrseqPath[len(BrseqPath)-6:len(BrseqPath):1] == '.brseq'):
					break
				else:
					print("\nERROR: Not A Valid File!")
			
		Brseq = open(BrseqPath,"rb")
		Brseq.seek(0)
		BrseqInfo = Brseq.read()
		Brseq.close()
		BrseqLength = format(os.stat(BrseqPath).st_size,'x').upper()

		#Song Selection
		print("\n//////////////////// Song List:")
		for num in range(len(SongNames)):
			SongMinLength = min(int(SongFileLengths[num],16),int(ScoreFileLengths[num],16))
			if(int(BrseqLength,16) > SongMinLength):
				print('~UNAVALIBLE~ '+str(SongNames[num])+' ('+format(SongMinLength,'x').upper()+')')
			else:
				print('(#'+str(num)+') '+str(SongNames[num])+' ('+format(SongMinLength,'x').upper()+')')
			time.sleep(0.005)

		#Brseq Info
		print("\n//////////////////// File Info:\nBrseq File Size: "+BrseqLength)

		#Song Selection
		while True:
			SongSelected = input("\n//////////////////// Song Selection:\nEnter The Song Number You Want To Replace: ")
			if(SongSelected.isnumeric()) and (int(SongSelected) < len(SongNames)):
				SongSelected = int(SongSelected)
				if(int(BrseqLength,16) <= min(int(SongFileLengths[SongSelected],16),int(ScoreFileLengths[SongSelected],16))):
					break
				else:
					print("ERROR: Brseq Filesize is over the maximum filesize for this song!")
			else:
				print("\nERROR: Not a Valid Number")

		#Brsar Writing
		brsar = open(BrsarPath, "r+b")
		brsar.seek(int(SongOffsets[SongSelected],16))
		brsar.write(bytes(int(SongFileLengths[SongSelected],16)))
		brsar.seek(int(ScoreOffsets[SongSelected],16))
		brsar.write(bytes(int(ScoreFileLengths[SongSelected],16)))
		brsar.seek(int(SongOffsets[SongSelected],16))
		brsar.write(BrseqInfo)
		brsar.seek(int(ScoreOffsets[SongSelected],16))
		brsar.write(BrseqInfo)
		brsar.close()

		#Length, Tempo, Time Signature Patch
		print("\n//////////////////// Length, Tempo, Time Signature Patch")
		while True:
			Length = input("How Many Measures Does Your Song Have: ")
			if(Length.isnumeric()): 
				break
			else:
				print("\nERROR: Not a Valid Number\n")

		while True:
			Tempo = input("\nWhat is the Tempo of Your Song: ")
			if(Tempo.isnumeric()):
				Tempo = format(int(Tempo),'x').upper()
				break
			else:
				print("\nERROR: Not a Valid Number")

		while True:
			TimeSignature = input("\nWhat Time Signature is Your Song? (4 = 4/4, 3 = 3/4): ")
			if(TimeSignature == '3') or (TimeSignature == '4'):
				Length = format(int(Length) * int(TimeSignature),'x').upper()
				break
			else:
				print("\nERROR: Please Press Ether 4 or 3")


		LengthCode = LengthMemoryOffsets[SongSelected]+' '+'0'*(8-len(Length))+Length+'\n'
		TempoCode = TempoMemoryOffsets[SongSelected]+' '+'0'*(8-len(Tempo))+Tempo+'\n'
		TimeCode = TimeSignatureMemoryOffsets[SongSelected]+' 00000'+TimeSignature+'00\n'

		if(input('\nAre You Sure You Want to Override '+SongNames[SongSelected]+'?\nYou Will NOT Be Able to Restore the Song Unless You Have Made a Backup! [y/n] ') == 'y'):
			AddPatch(SongNames[SongSelected]+' Song Patch',LengthCode+TempoCode+TimeCode)
			print("\nPatch Complete")
			time.sleep(0.5)
			print("")
		else:
			print("Aborted...")
	elif(mode == '3'):
		print("\n//////////////////// Style List:")
		for num in range(len(StyleNames)):
			print('(#'+str(num)+') '+str(StyleNames[num]))
			time.sleep(0.005)
		while True:
			StyleSelected = input("\n//////////////////// Style Selection:\nEnter The Style Number You Want To Replace: ")
			if(StyleSelected.isnumeric()) and (int(StyleSelected) < len(StyleNames)):
				StyleSelected = int(StyleSelected)
				break
			else:
				print("\nERROR: Not a Valid Number")
		print("\n//////////////////// Instrument List:")
		for num in range(40):
			print('(#'+str(num)+') '+str(InstrumentNames[num]))
			time.sleep(0.005)
		print("\n//////////////////// Style Selection:")
		while True:
			Melody = input("Enter The Instrament Number You Want For Melody: ")
			if(Melody.isnumeric()) and (int(Melody) < 40):
				Melody = format(int(Melody),'x').upper()
				Melody = '0'*(2-len(Melody))+Melody
				break
			else:
				print("\nERROR: Not a Valid Number\n")
		while True:
			Harmony = input("\nEnter The Instrament Number You Want For Harmony: ")
			if(Harmony.isnumeric()) and (int(Harmony) < 40):
				Harmony = format(int(Harmony),'x').upper()
				Harmony = '0'*(2-len(Harmony))+Harmony
				break
			else:
				print("\nERROR: Not a Valid Number")
		while True:
			Chord = input("\nEnter The Instrament Number You Want For Chord: ")
			if(Chord.isnumeric()) and (int(Chord) < 40):
				Chord = format(int(Chord),'x').upper()
				Chord = '0'*(2-len(Chord))+Chord
				break
			else:
				print("\nERROR: Not a Valid Number")
		while True:
			Bass = input("\nEnter The Instrament Number You Want For Bass: ")
			if(Bass.isnumeric()) and (int(Bass) < 40):
				Bass = format(int(Bass),'x').upper()
				Bass = '0'*(2-len(Bass))+Bass
				break
			else:
				print("\nERROR: Not a Valid Number")
		print("\n//////////////////// Instrument List:")
		for num in range(40,len(InstrumentNames)):
			print('(#'+str(num-40)+') '+str(InstrumentNames[num]))
			time.sleep(0.005)
		while True:
			Perc1 = input("\nEnter The Instrament Number You Want For Percussion 1: ")
			if(Perc1.isnumeric()) and (int(Perc1) < len(InstrumentNames)-40):
				Perc1 = format(int(Perc1)+40,'x').upper()
				Perc1 = '0'*(2-len(Perc1))+Perc1
				break
			else:
				print("\nERROR: Not a Valid Number")
		while True:
			Perc2 = input("\nEnter The Instrament Number You Want For Percussion 2: ")
			if(Perc2.isnumeric()) and (int(Perc2) < len(InstrumentNames)-40):
				Perc2 = format(int(Perc2)+40,'x').upper()
				Perc2 = '0'*(2-len(Perc2))+Perc2
				break
			else:
				print("\nERROR: Not a Valid Number")

		AddPatch(StyleNames[StyleSelected]+' Style Patch',StyleMemoryOffsets[StyleSelected]+' 00000018\n'+Melody+'000000 '+Harmony+'000000\n'+Chord+'000000 '+Bass+'000000\n'+Perc1+'000000 '+Perc2+'000000\n')
		print("\nPatch Complete")
		time.sleep(0.5)
		print("")