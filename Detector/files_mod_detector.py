import datetime
import time
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from tkinter import messagebox
from killer import kill_and_delete

ransomware_dictionary = [".encrypt", ".cry", ".crypto", ".darkness", ".enc" , ".exx", ".kb15", ".kraken", ".locked", ".nochance", ".___xratteamLucked", ".__AiraCropEncrypted!",
  "._AiraCropEncrypted", "._read_thi$_file" , ".02", ".0x0", ".725", ".1btc", ".1999", ".1cbu1", ".1txt", ".2ed2", ".31392E30362E32303136_[ID-KEY]_LSBJ1", ".73i87A",
  ".726", ".777", ".7h9r", ".7z.encrypted", ".7zipper", ".8c7f", ".8lock8", ".911", ".a19", ".a5zfn", ".aaa" , ".abc" , ".adk", ".adr", ".adair", ".AES", ".aes128ctr",
  ".AES256" , ".aes_ni", ".aes_ni_gov", ".aes_ni_0day" , ".AESIR", ".AFD", ".aga", ".alcatraz", ".Aleta", ".amba", ".amnesia", ".angelamerkel", ".AngleWare", ".antihacker2017",
  ".animus", ".ap19", ".atlas", ".aurora", ".axx", ".B6E1", ".BarRax", ".barracuda", ".bart", ".bart.zip", ".better_call_saul", ".bip", ".birbb", ".bitstak", ".bitkangoroo", 
  ".boom", ".black007", ".bleep", ".bleepYourFiles" , ".bloc", ".blocatto", ".block", ".braincrypt", ".breaking_bad", ".bript", ".brrr", ".btc", ".btcbtcbtc", ".btc-help-you", 
  ".cancer", ".canihelpyou", ".cbf", ".ccc", ".CCCRRRPPP", ".cerber", ".cerber2", ".cerber3", ".checkdiskenced", ".chifrator@qq_com", ".CHIP" , ".cifgksaffsfyghd", ".clf",
  ".clop", ".cnc", ".cobain", ".code", ".coded", ".comrade", ".coverton", ".crashed", ".crime", ".crinf", ".criptiko" , ".crypton", ".criptokod" , ".cripttt" , ".crjoker", 
  ".crptrgr", ".CRRRT" , ".cry", ".cry_", ".cryp1" , ".crypt", ".crypt38", ".crypted", ".cryptes", ".crypted_file", ".crypto", ".cryptolocker", ".CRYPTOSHIEL", ".CRYPTOSHIELD", 
  ".CryptoTorLocker2015!", ".cryptowall", ".cryptowin", ".crypz", ".CrySiS", ".css", ".ctb2", ".ctbl", ".CTBL", ".czvxce", ".d4nk", ".da_vinci_code", ".dale", ".damage",
  ".darkness" , ".darkcry", ".dCrypt", ".decrypt2017", ".ded", ".deria", ".desu", ".dharma", ".disappeared", ".diablo6", ".divine", ".dll", ".doubleoffset", ".domino", 
  ".doomed", ".dxxd", ".dyatel@qq_com", ".ecc", ".edgel", ".enc", ".encedRSA", ".EnCiPhErEd", ".encmywork", ".encoderpass", ".ENCR", ".encrypted", ".EnCrYpTeD", ".encryptedAES", 
  ".encryptedRSA", ".encryptedyourfiles", ".enigma", ".epic", ".evillock", ".exotic", ".exte", ".exx", ".ezz", ".fantom", ".fear", ".FenixIloveyou!!", ".file0locked", 
  ".filegofprencrp", ".fileiscryptedhard", ".filock", ".firecrypt", ".flyper", ".frtrss", ".fs0ciety", ".fuck", ".Fuck_You", ".fucked", ".FuckYourData" , ".fun", 
  ".flamingo", ".gamma", ".gefickt", ".gembok", ".globe", ".glutton", ".goforhelp", ".good", ".gruzin@qq_com" , ".gryphon", ".grinch", ".GSupport" , ".GWS", ".HA3", 
  ".hairullah@inbox.lv", ".hakunamatata", ".hannah", ".haters", ".happyday" ," .happydayzz", ".happydayzzz", ".hb15", ".helpdecrypt@ukr .net", ".helpmeencedfiles", 
  ".herbst", ".hendrix", ".hermes", ".help", ".hnumkhotep", ".hitler", ".howcanihelpusir", ".html", ".homer", ".hush", ".hydracrypt" , ".iaufkakfhsaraf", ".ifuckedyou", 
  ".iloveworld", ".infected", ".info", ".invaded", ".isis" , ".ipYgh", ".iwanthelpuuu", ".jaff", ".java", ".JUST", ".justbtcwillhelpyou", ".JLQUF", ".jnec", ".karma", 
  ".kb15", ".kencf", ".keepcalm", ".kernel_complete", ".kernel_pid", ".kernel_time", ".keybtc@inbox_com", ".KEYH0LES", ".KEYZ" , "keemail.me", ".killedXXX", ".kirked", 
  ".kimcilware", ".KKK" , ".kk", ".korrektor", ".kostya", ".kr3", ".krab", ".kraken", ".kratos", ".kyra", ".L0CKED", ".L0cked", ".lambda_l0cked", ".LeChiffre", ".legion",
  ".lesli", ".letmetrydecfiles", ".letmetrydecfiles", ".like", ".lock", ".lock93", ".locked", ".Locked-by-Mafia", ".locked-mafiaware", ".locklock", ".locky", ".LOL!", ".loprt", 
  ".lovewindows", ".lukitus", ".madebyadam", ".magic", ".maktub", ".malki", ".maya", ".merry", ".micro", ".MRCR1", ".muuq", ".MTXLOCK", ".nalog@qq_com", ".nemo-hacks.at.sigaint.org", 
  ".nobad", ".no_more_ransom", ".nochance" , ".nolvalid", ".noproblemwedecfiles", ".notfoundrans", ".NotStonks", ".nuclear55", "nuclear", ".obleep", ".odcodc", ".odin", ".oled",
  ".OMG!", ".only-we_can-help_you", ".onion.to._", ".oops", ".openforyou@india.com", ".oplata@qq.com" , ".oshit", ".osiris", ".otherinformation", ".oxr", ".p5tkjw", ".pablukcrypt", 
  ".padcrypt", ".paybtcs", ".paym", ".paymrss", ".payms", ".paymst", ".payransom", ".payrms", ".payrmts", ".pays", ".paytounlock", ".pdcr", ".PEGS1", ".perl", ".pizda@qq_com", 
  ".PoAr2w", ".porno", ".potato", ".powerfulldecrypt", ".powned"," .pr0tect", ".purge", ".pzdc", ".R.i.P", ".r16m" , ".R16M01D05", ".r3store", ".R4A" , ".R5A", ".r5a", ".RAD" , 
  ".RADAMANT", ".raid10",".ransomware", ".RARE1", ".rastakhiz", ".razy", ".RDM", ".rdmk", ".realfs0ciety@sigaint.org.fs0ciety", ".recry1", ".rekt", ".relock@qq_com", ".reyptson", 
  ".remind", ".rip", ".RMCM1", ".rmd", ".rnsmwr", ".rokku", ".rrk", ".RSNSlocked" , ".RSplited", ".sage", ".salsa222", ".sanction", ".scl", ".SecureCrypted", ".serpent", ".sexy", 
  ".shino", ".shit", ".sifreli", ".Silent", ".sport", ".stn", ".supercrypt", ".surprise", ".szf", ".t5019", ".tedcrypt", ".TheTrumpLockerf", ".thda", ".TheTrumpLockerfp", 
  ".theworldisyours", ".thor", ".toxcrypt", ".troyancoder@qq_com", ".trun", ".trmt", ".ttt", ".tzu", ".uk-dealer@sigaint.org", ".unavailable", ".vault", ".vbransom", ".vekanhelpu", 
  ".velikasrbija", ".venusf", ".Venusp", ".versiegelt", ".VforVendetta", ".vindows", ".viki", ".visioncrypt", ".vvv", ".vxLock", ".wallet", ".wcry", ".weareyourfriends", ".weencedufiles", 
  ".wflx", ".wlu", ".Where_my_files.txt", ".Whereisyourfiles", ".windows10", ".wnx", ".WNCRY", ".wncryt", ".wnry", ".wowreadfordecryp", ".wowwhereismyfiles", ".wuciwug", ".www", ".xiaoba", 
  ".xcri", ".xdata", ".xort", ".xrnt", ".xrtn", ".xtbl", ".xyz", ".ya.ru", ".yourransom", ".Z81928819", ".zc3791", ".zcrypt", ".zendr4", ".zepto", ".zorro", ".zXz", ".zyklon", ".zzz" , 
  ".zzzzz"]

suspicious_files = []

batch = list()
measures = list()

speed_band = [70,325] # opened files/s
batch_size = 60

word_whitelist = [ "chrome", "svchost", "MsMpEng", "WhatsApp", "VS Code", "SearchIndexer", "Discord", "Spotify", "explorer", "WinRar", "taskhostw", "ARMOURY CRATE"]
word_blacklist = ["Downloads"]

if __name__ == "__main__":

  patterns = ["*"]
  ignore_patterns = None
  ignore_directories = False 
  case_sensitive = True

  #donwloadFilesHandler corresponde a un watchdog que comprueba nuevos .exe en la carpeta Downloads
  donwloadFilesHandler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

  #allFilesHandler corresponde a un watchdog que comprueba modificaciones de cualquier archivo en cualquier carpeta
  allFilesHandler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)



def measureTime(file):
  f_save = open("times.txt", "a")
  f_save.write((file["Time"]).strftime("%H:%M:%S.%f'") + "\n")
  f_save.close()

def measureSpeed(speed):
  f = open("speeds.txt", "a")
  f.write(str(speed) + "\n")
  f.close()

def get_exes(path, suspicious_files):
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			if os.path.splitext(name)[1] == ".exe":
				suspicious_files.append(name)

def check_mod_speed(time1, time2):

  delta_time = (time2 - time1).total_seconds()
  speed = (batch_size//2) / delta_time
  #measureSpeed(speed)
  print("Mods Speed:" + str(speed))
  if speed>speed_band[0] and speed<speed_band[1]:
    return True
  else:
    return False


def detectRW(batch):

  if len(batch) in {batch_size//2, (batch_size*3)//4, batch_size}:
    time2 = batch[len(batch)-1]["Time"]
    time1 = batch[len(batch)-(batch_size//2)]["Time"]
    return check_mod_speed(time1, time2)

def warning(paths_lists):
  
  warning_message = "Se ha detectado activitad maliciosa en su ordenador.\n"

  if len(paths_lists["deleted"]) !=0:
    warning_message = warning_message + "Los siguientes archivos maliciosos han sido eliminados:\n"
    for path in paths_lists["deleted"]:
      warning_message = warning_message + path + "\n"
    warning_message = warning_message + "\n"

  if len(paths_lists["to_delete"]) !=0:
    warning_message = warning_message + "Los siguientes archivos maliciosos deberían ser eliminados cuanto antes:\n"
    for path in paths_lists["to_delete"]:
      warning_message = warning_message + path + "\n"
    warning_message = warning_message + "\n"

  if len(paths_lists["to_check"]) !=0:
    warning_message = warning_message + "Los siguientes archivos podrían contener un ransomware:\n"
    for path in paths_lists["to_check"]:
      warning_message = warning_message + path + "\n"
    warning_message = warning_message + "\n"

  messagebox.showinfo(message= warning_message , title="Aviso de Ransomware")




def on_moved_Download(event):

  #Cuando se descarga un archivo hay un cambio de nombre de .tmp a .crdownload 
  #y luego a la extensión del archivo

  if os.path.splitext(event.src_path)[1] == ".crdownload":
    if os.path.splitext(event.dest_path)[1] == ".exe":
      suspicious_files.append(os.path.basename(event.dest_path))
      # allFilesObserver.start()


def on_moved_AllFiles(event):

  try:
    file_extension = os.path.splitext(event.dest_path)[1]

    if file_extension in ransomware_dictionary:  
      print("Extension detected: " + file_extension)
      paths_lists = kill_and_delete(word_whitelist, word_blacklist)

      if paths_lists !=False:
        warning(paths_lists)

  except:
    pass

def on_modified_AllFiles(event):

  try:
    file = {"Path": event.src_path, "Time": datetime.datetime.now()}  

    if not any(file['Path'] == event.src_path for file in batch):
      batch.append(file)
      #measureTime(file)

      if detectRW(batch) == True:

        paths_lists = kill_and_delete(word_whitelist, word_blacklist)
        if paths_lists !=False:
          warning(paths_lists)
        
      if len(batch)==batch_size: #vacía tres cuartos del batch
        for i in range((batch_size*3)//4):
          batch.pop(0)

  except:
    pass

get_exes(os.path.join(Path.home(), "Downloads"), suspicious_files)

#Configurando Oberserver de la carpeta Donwloads
donwloadFilesHandler.on_moved = on_moved_Download
downloadObserver = Observer()
downloadObserver.schedule(donwloadFilesHandler, os.path.join(Path.home(), "Downloads"), recursive=True)

#Configurando Oberserver de todas las carpetas
allFilesHandler.on_moved = on_moved_AllFiles
allFilesHandler.on_modified = on_modified_AllFiles
allFilesObserver = Observer()
allFilesObserver.schedule(allFilesHandler, r"C:\\" , recursive=True)

allFilesObserver.start()
downloadObserver.start()

try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  downloadObserver.stop()
  downloadObserver.join()
  allFilesObserver.stop()
  allFilesObserver.join()