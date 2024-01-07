import customtkinter
from customtkinter import *
from PIL import Image
import pyAesCrypt
import random
import string
from datetime import datetime
import threading
import configparser
import os
import webbrowser


#customtkinter.set_appearance_mode("System")
assets_path = os.path.join(sys._MEIPASS, 'Assets') if getattr(sys, 'frozen', False) else 'Assets'
customtkinter.set_default_color_theme(f'{assets_path}/green.json')


app = customtkinter.CTk()
app.title('OpenFileEncryptor')
app.iconbitmap(f'{assets_path}/Icon.ico')
app.geometry("400x500")
app.resizable(width=False, height=False)



icon_image = CTkImage(Image.open(f'{assets_path}/Exit.png'), size=(30, 30))

def create_new_settings_file():
    config = configparser.ConfigParser()
    config['Settings'] = {'Language': 'English', 'Logs': 'off'}
    file = open('Settings.cfg', 'w', encoding="utf-8")
    config.write(file)
    file.close()


if not os.path.exists('Settings.cfg'):
    create_new_settings_file()

def error_read():
    global Language
    global Logs
    Language='English'
    Logs='off'

def read_settings():
    global Language
    global Language_restore
    global Logs
    config = configparser.ConfigParser()
    try:
        config.read('Settings.cfg', encoding='utf-8')
        Language = config.get('Settings', 'Language')
        Logs = config.get('Settings', 'Logs')
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
    except configparser.Error:
        create_new_settings_file()
        Language='English'
        Logs='off'
read_settings()




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
    global Language_save
    global Logs_save
    Language_save = language_menu.get()
    Logs_save = check_box_log.get()
    config = configparser.ConfigParser()
    if 'Language_save' not in globals():
        config['Settings'] = {'Language': Language, 'Logs': Logs_save}
    else:
        config['Settings'] = {'Language': Language_save, 'Logs': Logs_save}
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

def switch_language():
    global select_dir_button_enc_lan
    global path_entry_enc_lan
    global pin_entry_enc_lan
    global encryption_button_lan
    global check_box_lan
    global check_box_log_lan
    global select_dir_button_dec_lan
    global path_entry_dec_lan
    global pin_entry_dec_lan
    global decryption_button_lan
    global seg_button_lan_1
    global seg_button_lan_2
    global seg_button_lan_3
    global save_settings_lan
    global save_key_button_lan
    global upload_from_file_entry_enc_lan
    global text_enc
    if Language == 'English':
        select_dir_button_enc_lan = 'Select Directory'
        path_entry_enc_lan = 'Path to Directory'
        pin_entry_enc_lan = 'Enter the encryption key'
        encryption_button_lan = 'Encryption'
        check_box_lan = 'Generate a key?'
        check_box_log_lan = 'Save Logs?'
        select_dir_button_dec_lan = 'Select Directory'
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

def switch_language_enc(file):
    global text_enc
    if Language == 'English':
        text_enc = '[File ' + str(os.path.splitext(file)[0]) + "' is encrypted]" + f'\n' + f'\n'
    elif Language == 'Русский':
        text_enc = '[Файл ' + str(os.path.splitext(file)[0]) + "' зашифрован]" + f'\n' + f'\n'

def switch_language_dec(decrypted_file):
    global text_dec
    global text_dec_error
    if Language == 'English':
        text_dec = "[File '" + decrypted_file + "' is decrypted]" + f'\n' + f'\n'
        text_dec_error = f"[Decryption error! The key to decrypt the file: {decrypted_file} is incorrect]" + f'\n' + f'\n'
    elif Language == 'Русский':
        text_dec = "[Файл '" + decrypted_file + "' дешифрован]" + f'\n' + f'\n'
        text_dec_error = f"[Ошибка дешифровки! Ключ для дешифровки файла: {decrypted_file} неверен]" + f'\n' + f'\n'


def copyright_callback_1(event):
    webbrowser.open_new(r'https://github.com/CherretGit')

def copyright_callback_2(event):
    webbrowser.open_new(r'https://github.com/dreamcat69GIT')


def settings():
    global save
    global close
    global language_menu
    global check_box_log
    global check_box_log_var
    global copyright_label_1
    global copyright_label_2
    save = customtkinter.CTkButton(app, text=f'{save_settings_lan}', height=35, width=140, command=save_settings)
    save.place(x=130,y=180)
    language_menu = customtkinter.CTkOptionMenu(app, values=['English', 'Русский'])
    language_menu.set(f'{Language}')
    language_menu.place(x=130, y=70)
    check_box_log_var = customtkinter.StringVar(value='off')
    check_box_log = customtkinter.CTkCheckBox(app, text=f'{check_box_log_lan}', variable=check_box_var, onvalue="on", offvalue="off")
    check_box_log.place(x=130, y=130)
    copyright_label_1 = customtkinter.CTkLabel(app, text='CherretGit_(GUI) ', fg_color='#2fa572')
    copyright_label_1.place(x=0, y=230)
    copyright_label_1.bind("<Button-1>", copyright_callback_1)
    copyright_label_2 = customtkinter.CTkLabel(app, text='dreamcat69GIT_(PROGRAM) ', fg_color='#2fa572')
    copyright_label_2.place(x=0, y=260)
    copyright_label_2.bind("<Button-1>", copyright_callback_2)
    if Logs == 'on':
        check_box_log.select()
    elif Logs == 'off':
        check_box_log.deselect()



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
                    a= True
    
                except Exception as ex:
                    print(ex)
                    a= False
            
            else:
                walking_by_dirs(path, password)
                a= True
                
                    
    except Exception as e:
        print(e)
        a= False
    return a



def walking_by_dirs2(dir, password):
    try:
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                try:
                    encryption(path, password)
                except Exception as ex:
                    print(ex)
            else:
                walking_by_dirs2(path, password)
    except Exception as e:
        print(e)



def generate_key():
    length = 256
    characters = string.ascii_letters + string.digits
    random_string = random.choice(string.ascii_letters)

    for _ in range(length - 1):
        new_char = random.choice(characters.replace(random_string[-1], ''))
        random_string += new_char

    return random_string

def console_write(index, text):
    textbox.insert(index, text)

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
    global save_key_manual_button
    global exit_mini_button_manual
    save_key_manual_button = customtkinter.CTkButton(app, text=f'{save_key_button_lan}', height=35, width=130,command=save_key_to_file_manual)
    save_key_manual_button.place(x=10,y=285)

def rem_save_key_button_manual():
    save_key_manual_button.destroy()

def rem_save_key_button():
    save_key_button.destroy()

def save_key_button():
    global save_key_button
    global exit_mini_button
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
    global select_dir_button_enc
    global path_entry_enc
    global encryption_button
    global pin_entry_enc
    global check_box
    global check_box_var
    global upload_from_file_enc
    global path_upload_entry_enc
    global upload_from_file_enc
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
    global select_dir_button_dec
    global path_entry_dec
    global decryption_button
    global pin_entry_dec
    global upload_from_file_dec
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
    global textbox
    global exit_button
    try:
        exit_console()
    except:
        pass
    textbox = customtkinter.CTkTextbox(app, fg_color='black', text_color='#2fa572',width=400, height=170)
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
    copyright_label_1.destroy()
    copyright_label_2.destroy()

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
app.mainloop()