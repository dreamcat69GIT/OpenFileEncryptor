import customtkinter
from customtkinter import *
from PIL import Image
from Assets import ofe_lib as pyAesCrypt
import random
import string
from datetime import datetime
import threading
import configparser
import os
import requests
import time


assets_path = os.path.join(sys._MEIPASS, 'Assets') if getattr(sys, 'frozen', False) else 'Assets'
customtkinter.set_default_color_theme(f'{assets_path}/stock_theme.json')


app = customtkinter.CTk()
app.title('OpenFileEncryptor')
app.iconbitmap(f'{assets_path}/Icon.ico')
app.geometry("400x500")
app.resizable(width=False, height=False)



icon_image = CTkImage(Image.open(f'{assets_path}/Exit.png'), size=(30, 30))

version = '1.1.0'

def check_for_updates(version):
    try:
        global download_url, updater_app, start_update_gui, button_update, update_gui
        json_url = 'https://raw.githubusercontent.com/dreamcat69GIT/OpenFileEncryptor/main/update.json'
        response = requests.get(json_url)
        data = response.json()
        if data["current_version"] > version:
            updater_app = customtkinter.CTkToplevel(app)
            updater_app.title('OpenFileEncryptor – Updater')
            updater_app.iconbitmap(f'{assets_path}/Icon.ico')
            updater_app.geometry("400x200")
            updater_app.resizable(width=False, height=False)
            new_update_label = customtkinter.CTkLabel(updater_app, text=f'{new_update_label_lan}', fg_color="transparent")
            new_update_label.pack()
            download_url = data["download_url"]
            button_update = customtkinter.CTkButton(updater_app, text=f'{button_update_lan}', height=35, width=140, command=pre_update)
            button_update.place(x=250, y=150)
            button_close = customtkinter.CTkButton(updater_app, text=f'{button_close_lan}', height=35, width=140, command=close_window)
            button_close.place(x=10, y=150)
            def update_gui():
                updating_label = customtkinter.CTkLabel(updater_app, text=f'{updating_label_lan}', fg_color="transparent")
                updating_label.pack()
                button_start_after_update = customtkinter.CTkButton(updater_app, text=f'{button_start_after_update_lan}', height=35, width=140, command=start_new_version)
                button_start_after_update.place(x=250, y=150)
                timer = threading.Timer(5, stop_program)
                timer.start()
    except:
        pass

def stop_program():
    os.abort()


def pre_update():
    thread = threading.Thread(target=update)
    thread.start()
    button_update.destroy()
    while thread.is_alive():
        time.sleep(1)
    update_gui()

def close_window():
    updater_app.destroy()


def update():
    global filename
    filename = os.path.basename(download_url)
    download_file(download_url, filename)


def download_file(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)

def start_new_version():
    program_path = os.getcwd()
    full_path = os.path.join(program_path, filename)
    os.execl(full_path, *sys.argv)

def create_new_settings_file():
    config = configparser.ConfigParser()
    try:
        Language = config.get('Settings', 'Language')
        if Language == 'English':
            theme_lan = 'Standard theme'
        elif Language == 'Русский':
            theme_lan = 'Стандартная тема'
        config['Settings'] = {'Language': 'English', 'Logs': 'off','CustomThemeName': thememenu, 'CustomThemePath': 'None', 'AutoUpdate': 'on'}
    except:
        config['Settings'] = {'Language': 'English', 'Logs': 'off',  'CustomThemeName': 'Standard theme', 'CustomThemePath': 'None', 'AutoUpdate': 'on'}
    file = open('Settings.cfg', 'w', encoding="utf-8")
    config.write(file)
    file.close()


if not os.path.exists('Settings.cfg'):
    create_new_settings_file()

def error_read():
    global Language, Logs
    Language='English'
    Logs='off'

def read_settings():
    global Language, Language_restore, Logs, thememenu_lan, autoupdate, CustomThemeName, CustomThemePath
    config = configparser.ConfigParser()
    try:
        config.read('Settings.cfg', encoding='utf-8')
        Language = config.get('Settings', 'Language')
        if Language == 'English':
            thememenu_lan = 'Standard theme'
        elif Language == 'Русский':
            thememenu_lan = 'Стандартная тема'
        Logs = config.get('Settings', 'Logs')
        CustomThemeName = config.get('Settings', 'CustomThemeName')
        CustomThemePath = config.get('Settings', 'CustomThemePath')
        autoupdate = config.get('Settings', 'autoupdate')
        if CustomThemeName == 'Standard theme' or CustomThemeName == 'Стандартная тема':
            customtkinter.set_default_color_theme(f'{assets_path}/stock_theme.json')
        else:
            try:
                customtkinter.set_default_color_theme(f'{CustomThemePath}')
            except:
                create_new_settings_file()
                error_read()
                customtkinter.set_default_color_theme(f'{assets_path}/stock_theme.json')
        if Language == 'English' or Language == 'Русский':
            pass
        else:
            create_new_settings_file()
            error_read()
        if Logs == 'on' or Logs == 'off':
            pass
        else:
            create_new_settings_file()
            error_read()
        if autoupdate == 'on' or autoupdate == 'off':
            pass
        else:
            create_new_settings_file()
            error_read()
    except configparser.Error:
        create_new_settings_file()
        Language='English'
        Logs='off'
        autoupdate = 'on'
read_settings()


def switch_language():
    global select_dir_button_enc_lan, path_entry_enc_lan, pin_entry_enc_lan, encryption_button_lan, check_box_lan, check_box_log_lan, select_dir_button_dec_lan, new_update_label_lan, button_update_lan, button_close_lan, updating_label_lan, button_start_after_update_lan, check_box_autoupdate_lan, path_entry_dec_lan, pin_entry_dec_lan, decryption_button_lan, seg_button_lan_1, seg_button_lan_2, seg_button_lan_3, save_settings_lan, save_key_button_lan, upload_from_file_entry_enc_lan, text_enc
    if Language == 'English':
        select_dir_button_enc_lan = 'Select Directory'
        path_entry_enc_lan = 'Path to Directory'
        pin_entry_enc_lan = 'Enter the encryption key'
        encryption_button_lan = 'Encryption'
        check_box_lan = 'Generate a key?'
        check_box_log_lan = 'Save Logs?'
        select_dir_button_dec_lan = 'Select Directory'
        new_update_label_lan = 'New update available'
        button_update_lan = 'Update'
        button_close_lan = 'Cancel'
        updating_label_lan = 'The update has been downloaded! The program will close in 5 seconds'
        button_start_after_update_lan = 'Launch'
        check_box_autoupdate_lan = 'Auto Update'
        path_entry_dec_lan = 'Path to Directory'
        pin_entry_dec_lan = 'Enter the decryption key'
        decryption_button_lan = 'Decryption'
        save_settings_lan = 'Save'
        save_key_button_lan = 'Save the key to a file'
        upload_from_file_entry_enc_lan = 'Select key'
        seg_button_lan_1 = 'Encryption'
        seg_button_lan_2 = 'Decryption'
        seg_button_lan_3 = 'Settings'
    elif Language == 'Русский':
        select_dir_button_enc_lan = 'Выбор директории'
        path_entry_enc_lan = 'Путь до директории'
        pin_entry_enc_lan = 'Введите ключ шифрования'
        encryption_button_lan = 'Шифрование'
        check_box_lan = 'Генерировать ключ?'
        check_box_log_lan = 'Сохранять логи?'
        select_dir_button_dec_lan = 'Выбор директории'
        new_update_label_lan = 'Доступно новое обновление'
        button_update_lan = 'Обновить'
        button_close_lan = 'Отмена'
        updating_label_lan = 'Обновление загружено! Программа закроется через 5 секунд'
        button_start_after_update_lan = 'Запустить'
        check_box_autoupdate_lan = 'Автообновление'
        path_entry_dec_lan = 'Путь до директории'
        pin_entry_dec_lan = 'Введите ключ дешифрования'
        decryption_button_lan = 'Дешифрование'
        save_settings_lan = 'Сохранить'
        save_key_button_lan = 'Сохранить ключ в файл'
        upload_from_file_entry_enc_lan = 'Выбрать ключ'
        seg_button_lan_1 = 'Шифрование'
        seg_button_lan_2 = 'Дешифрование'
        seg_button_lan_3 = 'Настройки'
switch_language()


def check_files_with_text(directory, target_text):
    files_with_text = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                for line in file:
                    if target_text in line:
                        files_with_text.append(filename)
                        break
    return files_with_text

target_text = 'CTk'
directory_path = os.getcwd()

files_with_text = check_files_with_text(directory_path, target_text)


def select_dir_enc():
    path = filedialog.askdirectory()
    global dir_path
    path_entry_enc.delete(0, END)
    path_entry_enc.insert(0, f'{path}')

def select_dir_dec():
    path = filedialog.askdirectory()
    global dir_path
    path_entry_dec.delete(0, END)
    path_entry_dec.insert(0, f'{path}')

def select_key_enc():
    path = filedialog.askopenfilename()
    file = open(path, 'r', encoding="utf-8")
    key = file.read()
    pin_entry_enc.delete(0, END)
    pin_entry_enc.insert(0, key)

def select_key_dec():
    path = filedialog.askopenfilename()
    file = open(path, 'r', encoding="utf-8")
    key = file.read()
    pin_entry_dec.delete(0, END)
    pin_entry_dec.insert(0, key)


def save_settings():
    with open('Settings.cfg', 'wb'):
        pass
    global Language_save, Logs_save, autoupdate_save
    Language_save = language_menu.get()
    Logs_save = check_box_log.get()
    autoupdate_save = check_box_autoupdate.get()
    full_path = os.path.join(directory_path, thememenu.get())
    config = configparser.ConfigParser()
    if 'Language_save' not in globals():
        config['Settings'] = {'Language': Language, 'Logs': Logs_save}
        if thememenu.get() == thememenu_lan:
            config['Settings'] = {'Language': Language, 'Logs': Logs_save, 'CustomThemeName': thememenu_lan, 'CustomThemePath': 'None', 'autoupdate': autoupdate_save}
        else:
            config['Settings'] = {'Language': Language, 'Logs': Logs_save, 'CustomThemeName': thememenu.get(), 'CustomThemePath': full_path, 'autoupdate': autoupdate_save}
    else:
        config['Settings'] = {'Language': Language_save, 'Logs': Logs_save}
        if thememenu.get() == thememenu_lan:
            config['Settings'] = {'Language': Language_save, 'Logs': Logs_save, 'CustomThemeName': thememenu_lan, 'CustomThemePath': 'None', 'autoupdate': autoupdate_save}
        else:
            config['Settings'] = {'Language': Language_save, 'Logs': Logs_save, 'CustomThemeName': thememenu.get(), 'CustomThemePath': full_path, 'autoupdate': autoupdate_save}
    file = open('Settings.cfg', 'a+', encoding="utf-8")
    config.write(file)
    file.close()
    if Logs == 'on':
        text = 'Settings Saved' + f'\n' + f'\n'
        write_log(text)
    restart_program()

def write_log(text):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file = open('log.log', 'a+', encoding="utf-8")
    file.write(f'[{time_now}] {text}')
    file.close

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def switch_language_enc(file):
    global text_enc
    if Language == 'English':
        text_enc = '[File ' + str(os.path.splitext(file)[0]) + "' is encrypted]" + f'\n' + f'\n'
    elif Language == 'Русский':
        text_enc = '[Файл ' + str(os.path.splitext(file)[0]) + "' зашифрован]" + f'\n' + f'\n'

def switch_language_dec(decrypted_file):
    global text_dec, text_dec_error
    if Language == 'English':
        text_dec = "[File '" + decrypted_file + "' is decrypted]" + f'\n' + f'\n'
        text_dec_error = f"[Decryption error! The key to decrypt the file: {decrypted_file} is incorrect]" + f'\n' + f'\n'
    elif Language == 'Русский':
        text_dec = "[Файл '" + decrypted_file + "' дешифрован]" + f'\n' + f'\n'
        text_dec_error = f"[Ошибка дешифровки! Ключ для дешифровки файла: {decrypted_file} неверен]" + f'\n' + f'\n'


def settings():
    global save, close, language_menu, check_box_log, check_box_log_var, check_box_autoupdate, check_box_autoupdate_var, thememenu, copyright_label_1, copyright_label_2
    save = customtkinter.CTkButton(app, text=f'{save_settings_lan}', height=35, width=140, command=save_settings)
    save.place(x=130,y=460)
    language_menu = customtkinter.CTkOptionMenu(app, values=['English', 'Русский'])
    language_menu.set(f'{Language}')
    language_menu.place(x=130, y=70)
    check_box_log_var = customtkinter.StringVar(value='off')
    check_box_log = customtkinter.CTkCheckBox(app, text=f'{check_box_log_lan}', variable=check_box_log_var, onvalue="on", offvalue="off")
    check_box_log.place(x=130, y=130)
    check_box_autoupdate_var = customtkinter.StringVar(value='off')
    check_box_autoupdate = customtkinter.CTkCheckBox(app, text=f'{check_box_autoupdate_lan}', variable=check_box_autoupdate_var, onvalue="on", offvalue="off")
    check_box_autoupdate.place(x=130, y=190)
    thememenu = customtkinter.CTkOptionMenu(app, values=[thememenu_lan])
    thememenu_lan_text = [f'{thememenu_lan}']
    values = thememenu_lan_text + files_with_text
    thememenu.configure(values= values)
    thememenu.set(f'{CustomThemeName}')
    thememenu.place(x=125, y=240)
    if Logs == 'on':
        check_box_log.select()
    elif Logs == 'off':
        check_box_log.deselect()
    if autoupdate == 'on':
        check_box_autoupdate.select()
    elif autoupdate == 'off':
        check_box_autoupdate.deselect()



def decryption(file, password):
    buffer_size = 512 * 1024
    decrypted_file = str(os.path.splitext(file)[0])
    switch_language_dec(decrypted_file)
    index = '0.0'
    text = text_dec
    text_error = text_dec_error
    try:
        pyAesCrypt.decryptFile(str(file), decrypted_file, password, buffer_size)
        console_write(index, text)
        if Logs == 'on':
            write_log(text)
    except ValueError as e:
        console_write(index, text_error)
        if Logs == 'on':
            write_log(text_error)
    if os.path.exists(decrypted_file):
        os.remove(file)
        return True
    

def walking_by_dirs(dir, password):
    try:
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                try:
                    decryption(path, password)
    
                except Exception as ex:
                    pass
            
            else:
                walking_by_dirs(path, password)
                
    except Exception as e:
        pass



def walking_by_dirs2(dir, password):
    try:
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                try:
                    encryption(path, password)
                except Exception as ex:
                    pass
            else:
                walking_by_dirs2(path, password)
    except Exception as e:
        pass


def generate_key():
    length = 256
    characters = string.ascii_letters + string.digits
    random_string = random.choice(string.ascii_letters)

    for _ in range(length - 1):
        new_char = random.choice(characters.replace(random_string[-1], ''))
        random_string += new_char

    return random_string

def console_write(index, text):
    textbox.configure(state = NORMAL)
    textbox.insert(index, text)
    textbox.configure(state=DISABLED)

def encryption(file, password):
    switch_language_enc(file)
    index = '0.0'
    text = text_enc
    buffer_size = 512 * 1024
    pyAesCrypt.encryptFile(
        str(file),
        str(file) + ".crp",
        password,
        buffer_size
    )
    console_write(index, text)
    if Logs == 'on':
        write_log(text)
    os.remove(file)


def save_key_to_file():
    filename = filedialog.asksaveasfilename()
    if not filename.endswith('.txt'):
        filename += '.txt'
    with open(filename, 'w') as file:
        file.write(key)


def save_key_to_file_manual():
    filename = filedialog.asksaveasfilename()
    key = pin_entry_enc.get()
    if not filename.endswith('.txt'):
        filename += '.txt'
    with open(filename, 'w') as file:
        file.write(key)

def save_key_button_manual():
    global save_key_manual_button, exit_mini_button_manual
    save_key_manual_button = customtkinter.CTkButton(app, text=f'{save_key_button_lan}', height=35, width=130,command=save_key_to_file_manual)
    save_key_manual_button.place(x=10,y=285)

def rem_save_key_button_manual():
    save_key_manual_button.destroy()

def rem_save_key_button():
    save_key_button.destroy()

def save_key_button():
    global save_key_button, exit_mini_button
    save_key_button = customtkinter.CTkButton(app, text=f'{save_key_button_lan}', height=35, width=130,command=save_key_to_file)
    save_key_button.place(x=10,y=285)



def start_encryption():
    try:
        rem_save_key_button_manual()
    except:
        pass
    try:
        rem_save_key_button()
    except:
        pass
    console_enc()
    global key
    if check_box_var.get() == 'off':
        f = path_entry_enc.get()
        password = str(pin_entry_enc.get())
        threading.Thread(target=walking_by_dirs2, args=(f, password)).start()
        save_key_button_manual()
    elif check_box_var.get() == 'on':
        f = path_entry_enc.get()
        key = generate_key()
        password = str(key)
        threading.Thread(target=walking_by_dirs2, args=(f, password)).start()
        save_key_button()


def start_decryption():
    console_enc()
    f = path_entry_dec.get()
    password = str(pin_entry_dec.get())
    threading.Thread(target=walking_by_dirs, args=(f, password)).start()

def check_box_disable():
    if check_box_var.get() == 'off':
        pin_entry_enc.configure(state='normal')
    elif check_box_var.get() == 'on':
        pin_entry_enc.configure(state='disabled')


def enc_window():
    global select_dir_button_enc, path_entry_enc, encryption_button, pin_entry_enc, check_box, check_box_var, upload_from_file_enc, path_upload_entry_enc, upload_from_file_enc
    select_dir_button_enc = customtkinter.CTkButton(app, text=f'{select_dir_button_enc_lan}', height=35, width=130,command=select_dir_enc)
    select_dir_button_enc.place(x = 10, y=100)
    path_entry_enc = customtkinter.CTkEntry(app, placeholder_text=f'{path_entry_enc_lan}', width=200, height=35)
    path_entry_enc.place(x = 170, y=100)
    pin_entry_enc = customtkinter.CTkEntry(app, placeholder_text=f'{pin_entry_enc_lan}', width=200, height=35)
    pin_entry_enc.place(x = 170, y=170)
    encryption_button = customtkinter.CTkButton(app, text=f'{encryption_button_lan}', height=35, width=130,command=start_encryption)
    encryption_button.place(x = 10, y=230)
    check_box_var = customtkinter.StringVar(value="off")
    check_box = customtkinter.CTkCheckBox(app, text=f'{check_box_lan}', command=check_box_disable, variable=check_box_var, onvalue="on", offvalue="off")
    check_box.place(x=10,y=60)
    upload_from_file_enc = customtkinter.CTkButton(app, text=f'{upload_from_file_entry_enc_lan}', height=35, width=130,command=select_key_enc)
    upload_from_file_enc.place(x = 10, y=170)

def dec_window():
    global select_dir_button_dec, path_entry_dec, decryption_button, pin_entry_dec, upload_from_file_dec
    select_dir_button_dec = customtkinter.CTkButton(app, text=f'{select_dir_button_dec_lan}', height=35, width=130,command=select_dir_dec)
    select_dir_button_dec.place(x = 10, y=100)
    path_entry_dec = customtkinter.CTkEntry(app, placeholder_text=f'{path_entry_dec_lan}', width=200, height=35)
    path_entry_dec.place(x = 170, y=100)
    pin_entry_dec = customtkinter.CTkEntry(app, placeholder_text=f'{pin_entry_dec_lan}', width=200, height=35)
    pin_entry_dec.place(x = 170, y=170)
    decryption_button = customtkinter.CTkButton(app, text=f'{decryption_button_lan}', height=35, width=130,command=start_decryption)
    decryption_button.place(x = 10, y=230)
    upload_from_file_dec = customtkinter.CTkButton(app, text=f'{upload_from_file_entry_enc_lan}', height=35, width=130,command=select_key_dec)
    upload_from_file_dec.place(x = 10, y=170)

def console_enc():
    global textbox, exit_button
    try:
        exit_console()
    except:
        pass
    textbox = customtkinter.CTkTextbox(app,state = DISABLED,width=400, height=170)
    textbox.place(x=0,y=330)
    exit_button = customtkinter.CTkButton(app, text = '', width=5, height=5, image=icon_image, fg_color = 'transparent',hover_color = '#f44336', command=exit_console)
    exit_button.place(x= 360, y= 290)


def exit_console():
    textbox.destroy()
    exit_button.destroy()

def rem_enc():
    select_dir_button_enc.destroy()
    path_entry_enc.destroy()
    pin_entry_enc.destroy()
    encryption_button.destroy()
    check_box.destroy()
    upload_from_file_enc.destroy()

def rem_dec():
    select_dir_button_dec.destroy()
    path_entry_dec.destroy()
    pin_entry_dec.destroy()
    decryption_button.destroy()
    upload_from_file_dec.destroy()

def rem_settings():
    save.destroy()
    language_menu.destroy()
    check_box_log.destroy()
    check_box_autoupdate.destroy()
    thememenu.destroy()

last_dir = 'Encryption'
def folders_values(value):
    global last_dir
    if value == f'{seg_button_lan_1}':
        if last_dir == 'Decryption':
            rem_dec()
            last_dir = 'Encryption'
            enc_window()
        elif last_dir == 'Settings':
            rem_settings()
            last_dir = 'Encryption'
            enc_window()
    elif value == f'{seg_button_lan_2}':
        if last_dir == 'Encryption':
            rem_enc()
            last_dir = 'Decryption'
            try:
                rem_save_key_button_manual()
            except:
                pass
            try:
                rem_save_key_button()
            except:
                pass
            dec_window()
        elif last_dir == 'Settings':
            rem_settings()
            last_dir = 'Decryption'
            dec_window()
    elif value == f'{seg_button_lan_3}':
        if last_dir == 'Encryption':
            rem_enc()
            try:
                rem_save_key_button_manual()
            except:
                pass
            try:
                rem_save_key_button()
            except:
                pass
            last_dir = 'Settings'
            settings()
        elif last_dir == 'Decryption':
            rem_dec()
            last_dir = 'Settings'
            settings()

folders = customtkinter.CTkSegmentedButton(app, values=[f'{seg_button_lan_1}', f'{seg_button_lan_2}',f'{seg_button_lan_3}'],height=40, command=folders_values)
folders.pack()
folders.set(f'{seg_button_lan_1}')

enc_window()
if autoupdate == 'on':
    check_for_updates(version)
app.mainloop()