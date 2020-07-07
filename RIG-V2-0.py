"""RIG V2.0
Download x amount of images from a subreddit
For Windows and Linux.

By Steve Shambles July 2020.
stevepython.wordpress.com

pip3 install praw
"""
import os
from random import randrange
import shutil
import sys
from time import sleep
from tkinter import Button, E, END, filedialog
from tkinter import Label, LabelFrame, Menu, messagebox, PhotoImage
from tkinter import simpledialog, Tk, W
from tkinter.ttk import Combobox
import urllib.request as web
import webbrowser

import praw


root = Tk()


class Glo():
    """A few globals."""
    dest_fold = 'Reddit-Images'
    pusc = ''
    secret_code = ''
    subreddit_combo = ''


# Check if Glo.dest_fold exists.
chk_fldr = os.path.isdir(Glo.dest_fold)
# If it doesn't create it in cwd, now default download folder.
if not chk_fldr:
    os.makedirs(Glo.dest_fold)


def get_images():
    """Connect to Reddit API and attemp to download images."""
    # Error checks that user has filled out all boxes.
    EC_1 = Glo.subreddit_combo.get()
    EC_1 = EC_1.rstrip()
    if EC_1 == 'Subreddit' or EC_1 == '':
        messagebox.showerror('Error',
                             'Please Choose a Subreddit\n'
                             'See "HOW TO USE RIG" in the first menu')
        return

    EC_1 = grab_imgs_combo.get()
    if EC_1 == 'Images to grab':
        messagebox.showerror('Error',
                             'Please select how many Images '
                             'to grab\nSee "HOW TO USE RIG" in the first menu')
        return

    EC_1 = category_combo.get()
    if EC_1 == 'Category':
        messagebox.showerror('Error',
                             'Please Choose a Category\n'
                             'See "HOW TO USE RIG" in the first menu')
        return

    EC_1 = pause_combo.get()
    if EC_1 == 'Pauses':
        messagebox.showerror('Error',
                             'Please Choose length of pause\n'
                             'See "HOW TO USE RIG" in the first menu')
        return

    if not Glo.pusc:
        messagebox.showerror('Error',
                             'Please set personal use script code\n'
                             'from the settings menu first.\n\n'
                             'See "How to use RIG" in the first menu\n'
                             'for more information.')
        return

    if not Glo.secret_code:
        messagebox.showerror('Error',
                             'Please set secret code\n'
                             'from the settings menu first.\n\n'
                             'See "How to use RIG" in the first menu\n'
                             'for more information.')
        return

    if not Glo.dest_fold:
        messagebox.showerror('Error',
                             'Please choose a\n'
                             'folder to download to,\n'
                             'from the "Folder" menu first.\n\n'
                             'See "How to use RIG" in the first menu\n'
                             'for more information.')
        return

    selected_subred = Glo.subreddit_combo.get()
    selected_subred = selected_subred.rstrip()
    images_tograb = grab_imgs_combo.get()
    pause_length = pause_combo.get()
    get_cat = category_combo.get()

    # Call Reddit API with login details and what we want to dl.
    REDDIT = praw.Reddit(client_id=str(Glo.pusc),
                         client_secret=str(Glo.secret_code),
                         user_agent='RIG V2.0')

    # Basically because we cant change the praw category .method
    # with a variable, had to resort to pre-creating each outcome
    if get_cat == 'hot':
        sub_reddit = REDDIT.subreddit(str(selected_subred)).hot \
        (limit=int(images_tograb))
    elif get_cat == 'top':
        sub_reddit = REDDIT.subreddit(str(selected_subred)).top \
        ('all', limit=int(images_tograb))
    elif get_cat == 'rising':
        sub_reddit = REDDIT.subreddit(str(selected_subred)).rising \
        (limit=int(images_tograb))
    elif get_cat == 'gilded':
        sub_reddit = REDDIT.subreddit(str(selected_subred)).gilded \
        (limit=int(images_tograb))
    else:
        sub_reddit = REDDIT.subreddit(str(selected_subred)).new \
        (limit=int(images_tograb))

    # Open in sytem file viewer to view dls live as they come in.
    webbrowser.open(Glo.dest_fold)

    # The actual downloading bit.
    try:
        for submissions in sub_reddit:
            # Ignore stickies.
            if not submissions.stickied:
                fullfilename = os.path.join(Glo.dest_fold, '{}.jpg'.format(submissions))
                request = web.Request(submissions.url)

                with web.urlopen(request) as response, open(fullfilename, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                    dir_count = len(os.listdir(Glo.dest_fold))
                    print("Downloaded. {} file(s) saved in '{}'.".format(dir_count, Glo.dest_fold))

                    # Prob good idea if u dont want to get banned.
                    if pause_length == 'random 1-5 secs':
                        pause_length = (randrange(5))

                    sleep(int(pause_length))
    except:
        root.attributes('-topmost', 1)
        messagebox.showerror('Error', 'Sorry, Unknown download error')
        return

    root.attributes('-topmost', 1)
    messagebox.showinfo('Reddit Image Grabber', 'Downloads completed')


def about_menu():
    """Display About message box."""
    messagebox.showinfo('About', 'RIG V2.0. Freeware.\n'
                                 'Steve Shambles July 2020\n'
                                 '\nRIG helps you to download \n'
                                 'images in bulk from \n'
                                 'Reddit.com\n')


def visit_blog():
    """Visit my blog, you know it makes sense."""
    webbrowser.open('https://stevepython.wordpress.com/python-posts-quick-index')


def input_pusc():
    """Pop up input box to enter personal user script code."""
    get_pusc = simpledialog.askstring(title="Personal use script code",
                                      prompt="Cancel to leave unchanged")
    if get_pusc == '':
        return

    if get_pusc is not None:
        Glo.pusc = get_pusc
        messagebox.showinfo('Tip', 'If you wish to keep this code\n'
                                   'click save settings in settings menu.')


def input_secret():
    """Pop up input box to enter Reddit secret code with ctrl v."""
    get_secret = simpledialog.askstring(title="Secret code",
                                        prompt="Cancel to leave unchanged")
    if get_secret == '':
        return

    if get_secret is not None:
        Glo.secret_code = get_secret
        messagebox.showinfo('Tip', 'If you wish to keep this code\n'
                                   'click save settings in settings menu.')


def choose_dwnld_fldr():
    """Get user selected dir to save images."""
    get_df = filedialog.askdirectory()

    if get_df == '':
        return

    if get_df is not None:
        Glo.dest_fold = get_df
        messagebox.showinfo('Tip', 'If you wish to keep this setting\n'
                                   'click save settings in settings menu.')


def open_dwnld_fldr():
    """Display contents of current download folder in system file viewer."""
    webbrowser.open(Glo.dest_fold)


def del_dwnld_fldr():
    """Delete current download folder and its contents."""
    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to\n'
                                 'delete your RIG download\n'
                                 'folder and all of its contents?\n\n'
                                 'This action cannot be undone.\n')
    if ask_yn is False:
        return
    shutil.rmtree(Glo.dest_fold)
    Glo.dest_fold = ''

    messagebox.showinfo('Tip', 'Download folder deleted.\n'
                               'You will need to set up\n'
                               'a new download folder\n.'
                               'from the Folder menu.')


def del_dwnlded_imgs():
    """Delete all images in current download folder."""
    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to\n'
                                 'delete your RIG\n'
                                 'downloaded images?\n\n'
                                 'This action cannot be undone.\n')
    if ask_yn is False:
        return
    try:
        shutil.rmtree(Glo.dest_fold)
        os.makedirs(Glo.dest_fold)
    except:
        messagebox.showerror('Error', 'There was a problem\n'
                                      'maybe the file or\n'
                                      'folder is in use?')
        return

    messagebox.showinfo('Tip', 'Your RIG download folder.\n'
                               'is now empty, but still\n'
                               'valid, so you can start\n'
                               'downloading images into\n'
                               'it right away.')


def donate_me():
    """In the vain hope someone generous likes this program enough to
       reward my work."""
    webbrowser.open("https:\\paypal.me/photocolourizer")


def exit_rig():
    """Yes-no requestor to exit program."""
    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to exit RIG?')
    if ask_yn is False:
        return
    root.destroy()
    sys.exit()


def save_ids():
    """Save all the current settings to text files."""
    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to\n'
                                 'overwrite the old settings\n'
                                 'and save current settings?')
    if ask_yn is False:
        return

    # Save spi settings.
    with open('cid.txt', 'w') as contents:
        contents.write(Glo.pusc)

    with open('cls.txt', 'w') as contents:
        contents.write(Glo.secret_code)

    with open('dest.txt', 'w') as contents:
        contents.write(Glo.dest_fold)

    # Now do the left download settings.

    c_1 = Glo.subreddit_combo.get()
    c_1 = c_1.rstrip()
    c_2 = grab_imgs_combo.get()
    c_3 = category_combo.get()
    c_4 = pause_combo.get()
    allcs = str(c_1)+'\n'+str(c_2)+'\n'+str(c_3)+'\n'+str(c_4)

    with open('rig.txt', 'w') as contents:
        contents.write(allcs)

    messagebox.showinfo('RIG message', 'Settings have been saved')


def default_settings():
    """Reset all user settings to default."""

    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to\n'
                                 'reset all of RIGs settings?\n\n'
                                 'This action cannot be undone.')
    if ask_yn is False:
        return

    with open('rig.txt', 'w') as contents:
        contents.write('Subreddit\nImages to grab\nCategory\nPauses')

    with open('rig.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in open('rig.txt')]
        lines = f.read().splitlines()
        Glo.subreddit_combo.delete(0, END)
        Glo.subreddit_combo.insert(0, lines[0])
        grab_imgs_combo.delete(0, END)
        grab_imgs_combo.insert(1, lines[1])
        category_combo.delete(0, END)
        category_combo.insert(2, lines[2])
        pause_combo.delete(0, END)
        pause_combo.insert(3, lines[3])

    with open('cid.txt', 'w') as contents:
        Glo.pusc = ''

    with open('cls.txt', 'w') as contents:
        Glo.secret_code = ''

    with open('dest.txt', 'w') as contents:
        Glo.dest_fold = ''

    messagebox.showinfo('RIG message', 'All settings have been reset.')


def rig_help():
    """Visit RIG help page on my blog."""
    webbrowser.open('https://wp.me/Pa5TU8-2PQ')


def view_settings():
    """Display value of main three settings in pop up."""
    messagebox.showinfo('RIG Settings',
                        'Personal user script code: ' + Glo.pusc
                        + '\n\nReddit secret code: ' + Glo.secret_code
                        + '\n\nDownload folder: ' + Glo.dest_fold)


def edit_ids():
    """Open settings text files for editing or viewing."""
    webbrowser.open('cid.txt')
    webbrowser.open('dest.txt')
    webbrowser.open('cls.txt')


def edit_subs():
    """Open default subreddits text file for editing or viewing."""
    webbrowser.open('subreddits.txt')


def edit_nsfw():
    """Open nsfw subreddits text file for editing or viewing."""
    if sys.platform.startswith('win'):
        webbrowser.open(r'nsfw\subreddits.txt')
    else:
        webbrowser.open(r'nsfw/subreddits.txtsubreddits.txt')


def nsfw_subs():
    """Load in NSFW subreddits text file, after askyn warning."""
    ask_yn = messagebox.askyesno('SERIOUS WARNING',
                                 'Are you sure you want to\n'
                                 'load in the NSFW list?\n\n'
                                 'NSFW contains extremely\n'
                                 'ADULT content that is not\n'
                                 'suitable for anyone under\n'
                                 'the age of 18?')
    if ask_yn is False:
        return

    Glo.subreddit_combo.destroy()
    subred_list = []

    with open('nsfw/subreddits.txt') as file_in:
        for line in file_in:
            subred_list.append(line)

    Glo.subreddit_combo = Combobox(sub_red_frame)
    Glo.subreddit_combo['values'] = (subred_list)

    Glo.subreddit_combo.current(0)  # Set the selected item.
    Glo.subreddit_combo.grid(padx=5, pady=5)


def sfw_subs():
    """Load in default subreddits text file when requsted from menu."""
    Glo.subreddit_combo.destroy()
    subred_list = []

    with open('subreddits.txt') as file_in:
        for line in file_in:
            subred_list.append(line)

    Glo.subreddit_combo = Combobox(sub_red_frame)
    Glo.subreddit_combo['values'] = (subred_list)

    Glo.subreddit_combo.current(0)  # Set the selected item.
    Glo.subreddit_combo.grid(padx=5, pady=5)


# Check for praw.ini in current dir, if no,t goto dl page, then quit.
CHECK_INI = os.path.isfile('praw.ini')
if not CHECK_INI:
    messagebox.showinfo('Error',
                        'Praw.ini file is missing from current dir.\n'
                        'Click OK to go to a link to download it\n'
                        ' Copy praw.ini to same place as Rig executable and try again.')

    webbrowser.open('https://www.mediafire.com/file/776fdzz95cku6ee/praw.ini/file')
    root.destroy()
    root.quit()
    sys.exit

# Create window.
root.title('RIG V2.0')
root.resizable(False, False)

# Drop down menu.
MENU_BAR = Menu(root)
FILE_MENU = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='Menu', menu=FILE_MENU)
FILE_MENU.add_command(label='How to use RIG', command=rig_help)
FILE_MENU.add_command(label='Visit Blog', command=visit_blog)
FILE_MENU.add_separator()
FILE_MENU.add_command(label='About', command=about_menu)
FILE_MENU.add_command(label='Make a small donation via PayPal', command=donate_me)
FILE_MENU.add_command(label='Exit', command=exit_rig)
root.config(menu=MENU_BAR)

# folder drop down menu
file_menu = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='Folder', menu=file_menu)
file_menu.add_command(label='Choose Download folder', command=choose_dwnld_fldr)
file_menu.add_command(label='Open Download folder', command=open_dwnld_fldr)
file_menu.add_separator()
file_menu.add_command(label='Delete Download folder', command=del_dwnld_fldr)
file_menu.add_command(label='Delete all images in Download folder', command=del_dwnlded_imgs)
root.config(menu=MENU_BAR)

# api drop down menu
api_menu = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='Settings', menu=api_menu)
api_menu.add_command(label='Enter personal use script code - ctrl v to paste', command=input_pusc)
api_menu.add_command(label='Enter Reddit secret code - ctrl v to paste', command=input_secret)
api_menu.add_separator()
api_menu.add_command(label='View settings', command=view_settings)
api_menu.add_command(label='Save settings', command=save_ids)
api_menu.add_separator()
api_menu.add_command(label='Edit settings manually', command=edit_ids)
api_menu.add_command(label='Reset settings', command=default_settings)
api_menu.add_separator()
api_menu.add_command(label='View or edit SFW subreddits list', command=edit_subs)
api_menu.add_command(label='View or edit NSFW subreddits list', command=edit_nsfw)

api_menu.add_separator()
api_menu.add_command(label='Load NSFW ADULT subreddits list', command=nsfw_subs)
api_menu.add_command(label='Load SFW subreddits list', command=sfw_subs)

root.config(menu=MENU_BAR)

# Load in and display rig logo.
riglogo_lbl = Label(root)
PHOTO = PhotoImage(file='rig-logo-strip.png')
riglogo_lbl.config(image=PHOTO)
riglogo_lbl.grid(padx=2, pady=2)
riglogo_lbl.photo = PHOTO

sub_red_frame = LabelFrame(root, text="Subreddit")
sub_red_frame.grid(row=1, column=0, padx=5, pady=8)

imgs_2grab_frame = LabelFrame(root, text="Images to grab")
imgs_2grab_frame.grid(row=2, column=0, padx=5, pady=8)

category_frame = LabelFrame(root, text="Category")
category_frame.grid(row=3, column=0, padx=5, pady=8)

pauses_frame = LabelFrame(root, text="Pauses")
pauses_frame.grid(row=4, column=0, padx=5, pady=8)

subred_list = []
with open('subreddits.txt') as file_in:
    subred_list = []
    for line in file_in:
        subred_list.append(line)
Glo.subreddit_combo = Combobox(sub_red_frame)
Glo.subreddit_combo['values'] = (subred_list)

Glo.subreddit_combo.current(0)  # Set the selected item.
Glo.subreddit_combo.grid(padx=5, pady=5)
# Choose amount of images to download.
grab_imgs_combo = Combobox(imgs_2grab_frame)
grab_imgs_combo['values'] = ('Images to grab', 1, 5, 10, 25, 50, 100, 250, 500, 999)
grab_imgs_combo.current(0)
grab_imgs_combo.grid(padx=5, pady=5)

# Select category combobox.
category_combo = Combobox(category_frame)
category_combo['values'] = ('Category', 'new', 'hot', 'top', 'rising')
category_combo.current(0)
category_combo.grid(sticky=W+E, padx=5, pady=5)

# Select download pause combobox.
pause_combo = Combobox(pauses_frame)
pause_combo['values'] = ('Pauses', 1, 2, 3, 4, 5, 'random 1-5 secs')
pause_combo.current(0)
pause_combo.grid(sticky=W+E, padx=5, pady=5)

# Grab images button.
B = Button(root, text='Grab Images', bg="limegreen",
           command=get_images)
B.grid(sticky=W+E, padx=5, pady=5)

# Read txt files.
# If cid.txt exists insert the code into GUI for user.
if os.path.exists('cid.txt'):
    with open('cid.txt', 'r') as contents:
        Glo.pusc = contents.read()

# If not then create it.
if not os.path.exists('cid.txt'):
    # Default text otherwise.
    with open('cid.txt', 'w') as contents:
        contents.write('Personal use script code')

# If cls.txt exists insert the code into box for user.
if os.path.exists('cls.txt'):
    with open('cls.txt', 'r') as contents:
        Glo.secret_code = contents.read()

# If not then create it.
if not os.path.exists('cls.txt'):
    with open('cls.txt', 'w') as contents:
        contents.write('Secret Code')

# If dest.txt exists insert the code into box for user
if os.path.exists('dest.txt'):
    with open('dest.txt', 'r') as contents:
        Glo.dest_fold = contents.read()

# If not then create it.
if not os.path.exists('dest.txt'):
    with open('dest.txt', 'w') as contents:
        contents.write(Glo.dest_fold)

# If rig.txt exists insert settings into GUI for user.
if os.path.exists('rig.txt'):
    with open('rig.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in open('rig.txt')]
        lines = f.read().splitlines()
        Glo.subreddit_combo.delete(0, END)
        Glo.subreddit_combo.insert(0, lines[0])

        if Glo.subreddit_combo.get() == 'NSFW':
            nsfw_subs()

        grab_imgs_combo.delete(0, END)
        grab_imgs_combo.insert(1, lines[1])
        category_combo.delete(0, END)
        category_combo.insert(2, lines[2])
        pause_combo.delete(0, END)
        pause_combo.insert(3, lines[3])

# If rig.txt not found call default settings function.
if not os.path.exists('rig.txt'):
    default_settings()

root.eval('tk::PlaceWindow . Center')
root.protocol("WM_DELETE_WINDOW", exit_rig)

root.mainloop()
