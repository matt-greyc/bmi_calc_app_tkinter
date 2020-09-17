#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import datetime
import os
import csv

metric_frame_is_active = True # metric frame is the top frame,
# if metric_frame_is_active == False it means we've switched to imperial units


#  function starts app window in the center of the screen ---------------------
def center_screen(window_width, window_height): # starts app window in the center of the screen
    import ctypes
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return (window_width, window_height, (screen_width - window_width) / 2, (screen_height - window_height) / 2)
# -----------------------------------------------------------------------------


#  function used for validating user intput (height/weight) accepts only numeric values
# ---------------------------------------------------------------------------
def validate_data(S, s, d):

    # %S = the text string being inserted or deleted, if any
    # %s = value of entry prior to editing
    # %d = Type of action (1=insert, 0=delete, -1 for others)

    # allowed_values_numeric = '0123456789'
    # allowed_values_all = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'

    user_input = S
    entry_content_before_input = s
    full_entry_content = s + S

    # print('user_input:', user_input)
    # print('entry_content_before_input:', entry_content_before_input)
    # print('full_entry_content:', full_entry_content)

    # ------------------------------------------------------------------
    def validate_length(length_of_entry_field=20):

        if len(full_entry_content) < length_of_entry_field + 1:
            return True

        if len(full_entry_content) >= length_of_entry_field + 1 and d == '0':
            return True

        return False
    #-------------------------------------------------------------------

    # ------------------------------------------------------------------
    def validate_is_numeric():

        try:
            full_entry_content_float = float(full_entry_content)
            full_entry_content_int = int(full_entry_content)
            if full_entry_content_float == full_entry_content_int:
                return True
        except:
            return False

        # return False
    #-------------------------------------------------------------------



    stuff_to_validate = [
                         validate_length(3),
                         validate_is_numeric()
                         ]

    return all(stuff_to_validate)

# ---------------------------------------------------------------------------


# ----------- function used for validating user intput (name length)
def validate_name(S, d):

    name = name_entry.get()

    allowed_values_all = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._- '

        # print(S, type(S), d, type(d))
    # print(name, 'len', len(name))

    if name == default_text:
        return True

    for letter in S:
        if letter not in allowed_values_all:
            return False

    if len(name) > 9 and d == '0':
        return True

    if len(name)+ len(S) > 10 and d == '1':
        return False

    if len(name) <= 9:
        return True

    return False
# -----------------------------------------------------------------------------


# command function for metric radiobutton used for switching frames between
# metric and imperial --------------------------------------------------------
def f_metric_rb(): # executed when metric radiobutton is selected
    # self.entry.delete(0, 'end')
    global metric_frame_is_active
    metric_frame.tkraise()  # makes metric frame the top frame
    metric_rb.focus()

    # when metric frame is active metric entries are activated and imperial entries are deactivated
    kilograms_entry.config(takefocus=True)
    height_entry_cm.config(takefocus=True)
    height_entry_feet.config(takefocus=False)
    height_entry_inches.config(takefocus=False)
    stones_entry.config(takefocus=False)
    pounds_entry.config(takefocus=False)

    height_entry_feet.delete(0, 'end')  # clears 'feet' entry
    height_entry_inches.delete(0, 'end')  # clears 'inches' entry
    stones_entry.delete(0, 'end')  # clears 'stones' entry
    pounds_entry.delete(0, 'end')  # clears 'pounds' entry
    metric_frame_is_active = True  # variable used to determine the top frame

    calculate_button.config(takefocus=False)
    
# -----------------------------------------------------------------------------


# command function for imperial radiobutton used for switching frames between
# metric and imperial --------------------------------------------------------
def f_imperial_rb():  # executed when imperial radiobutton is selected
    global metric_frame_is_active
    imperial_frame.tkraise()  # makes imperial frame the top frame
    imperial_rb.focus()

    # when imperial frame is active imperial entries are activated and metric entries are deactivated
    height_entry_feet.config(takefocus=True)
    height_entry_inches.config(takefocus=True)
    stones_entry.config(takefocus=True)
    pounds_entry.config(takefocus=True)
    kilograms_entry.config(takefocus=False)
    height_entry_cm.config(takefocus=False)

    height_entry_cm.delete(0, 'end')
    kilograms_entry.delete(0, 'end')
    metric_frame_is_active = False  # variable used to determine the top frame

    calculate_button.config(takefocus=False)

# -----------------------------------------------------------------------------


# command function for 'calculate BMI' button --------------------------------
def calculate_bmi(*args, **kwargs):  # executed when calculate BMI button is clicked

    bmi = None
    global metric_frame_is_active

    if metric_frame_is_active == True:  # calculates bmi for metric units

        cm = height_entry_cm.get()  # pulls data from 'centimeters' entry
        kg = kilograms_entry.get()  # pulls data from 'kilograms' entry

        title = 'Missing data'  # messages used for blank entry fields and zero values
        error_message = f'''Missing values detected.
Please ensure you have entered
valid height and weight.'''

        if cm == '' or kg == '':  # checks if entries are blank
            messagebox.showinfo(title, error_message)  # displayed if entries are blank
        elif float(cm) == 0 or float(kg) == 0:  # checks if values are zero
            messagebox.showinfo(title, error_message)  # displayed if values are zero
        else:
            cm = int(cm)
            kg = int(kg)
            bmi = round(kg/(cm/100)**2, 1) # BMI = (Weight in Kilograms / (Height in Meters x Height in Meters))

            result_dict = dict(cm=cm, kg=kg, feet=0, inches=0, stones=0, pounds=0, BMI=bmi)

            display_results(**result_dict)  # displays bmi + info messages

    elif metric_frame_is_active == False:  # calculates bmi for imperial units

        feet = height_entry_feet.get()  # pulls data from 'feet' entry
        inches = height_entry_inches.get()  # pulls data from 'inches' entry
        stones = stones_entry.get()  # pulls data from 'stones' entry
        pounds = pounds_entry.get()  # pulls data from 'pounds' entry

        feet_to_inches = (0 if feet == '' else float(feet) * 12)
        total_inches = feet_to_inches + (0 if inches == '' else float(inches))  # total imperial height

        stones_to_pounds = (0 if stones == '' else float(stones) * 14)
        total_pounds = stones_to_pounds + (0 if pounds == '' else float(pounds))  # total imperial weight

        title = 'Missing data'  # messages used for blank entry fields and zero values
        error_message = f'''Missing values detected.
Please ensure you have entered
valid height and weight.'''
 #
        if feet == '' and inches == '' or stones == '' and pounds == '': # checks if entries are blank
            messagebox.showinfo(title, error_message)  # displayed if entries are blank
        elif total_inches == 0 or total_pounds == 0:  # checks if values are zero
            messagebox.showinfo(title, error_message)  # displayed if values are zero
        else:
            feet = (0 if feet == '' else int(feet))
            inches = (0 if inches == '' else int(inches))
            stones = (0 if stones == '' else int(stones))
            pounds = (0 if pounds == '' else int(pounds))
            bmi = round((total_pounds/(total_inches)**2) * 703, 1) # BMI = (Weight in Pounds / (Height in inches x Height in inches)) x 703

            result_dict = dict(cm=0, kg=0, feet=feet, inches=inches, stones=stones, pounds=pounds, BMI=bmi)

            display_results(**result_dict)  # displays bmi + info messages

            
# ----------------   end of 'calculate BMI' function block  ------------------


#  displays bmi result and info messages --------------------------------------
def display_results(*args, **kwargs):

    global default_text

    #  saves results as csv file if user clicks 'save' button -----------------
    def save_file(*args, **kwargs):
        nonlocal username

        f_date = datetime.datetime.now().strftime("%Y-%m-%d")  # date string: 2020-01-28
        user = (username + '_' if username else '')  # eg
        default_filename = user + 'bmi_result_' + f_date + '.csv'  # default filename: 'matt_bmi_result_2020-01-30.csv'
        current_folder = os.getcwd()  # gets filepath using os module

        filename = filedialog.asksaveasfile(filetypes = [("csv file","*.csv")],
        initialdir = current_folder, initialfile=default_filename,
        defaultextension='.csv')  # opens tkinter 'save as' dialog

        column_names = ['Date', 'BMI', 'centimeters', 'feet', 'inches',
                        'kilograms', 'stones', 'pounds']  # column names passed to csv writer
        # result_dict = dict(cm=0, kg=0, feet=feet, inches=inches, stones=stones, pounds=pounds, BMI=bmi)
        data = [f_date, kwargs['BMI'], kwargs['cm'], kwargs['feet'], kwargs['inches'],
                kwargs['kg'], kwargs['stones'], kwargs['pounds']]  # data passed to csv writer

        csv_object = csv.writer(filename, lineterminator='\n')
        csv_object.writerow(column_names)  # writes column names to csv file
        csv_object.writerow(data)  # writes results to csv file
    #  ----------------    end of save_file function block    -----------------


    #  clears entries and closes results display window   ---------------------
    def close_and_clear(*args, **kwargs):

        height_entry_cm.delete(0, 'end')
        kilograms_entry.delete(0, 'end')
        height_entry_feet.delete(0, 'end')
        height_entry_inches.delete(0, 'end')
        stones_entry.delete(0, 'end')
        pounds_entry.delete(0, 'end')

        results_frame.destroy()
        root.bind("<KeyPress-Return>", calculate_bmi)
    #  ------------------------------------------------------------------------

    bmi_result = kwargs['BMI']  # kwargs -> bmi result dict
    username = False if name_entry.get() in [default_text, ''] else name_entry.get() # name entered by the user

    if bmi_result < 18.5:  # messages displayed for bmi < 18.5
        message1 = 'UNDERWEIGHT'
        message2 = '''When your body mass index is less than 18.5,
it could indicate that you do not have
enough body fat to sustain good health.'''
    elif bmi_result >= 18.5 and bmi_result < 25:  # messages displayed for bmi 18.5 - 25
        message1 = 'HEALTHY'
        message2 = '''Congratulations, you appear to have
an optimal amount of body fat.'''
    elif bmi_result >= 25 and bmi_result < 30:  # messages displayed for bmi 25 - 30
        message1 = 'OVERWEIGHT'
        message2 = '''When your body mass index number is
25 or higher, it may indicate that you have
too much weight in relation to your height.'''
    elif bmi_result >= 30:  # messages displayed for bmi > 30
        message1 = 'OBESE'
        message2 = '''Based upon your BMI score, you are possibly
obese. You are at a much higher risk of developing
chronic diseases and shortening your lifespan.'''


    # ---------------------         results frame         ---------------------
    # -------------------------------------------------------------------------

    results_frame = tk.Frame(root, bg=app_color, height=root_height, width=root_width)

    result = ''


    if username:  # if user entered name: 'Matt, your BMI is {bmi_result}'
        display_label_name_message = f'{username}, your BMI is {bmi_result}:'
    else:  # if user didn't enter name: 'Your BMI is {bmi_result}'
        display_label_name_message = f'Your BMI is {bmi_result}:'

    display_label_bmi_message = '<<<  ' + message1 + '  >>>'  #  ''<<<  UNDERWEIGHT  >>>''

    # label 1 -> name + bmi --------------------------------------------------
    display_label_name = tk.Label(results_frame, text=display_label_name_message,
    font=('Segoe UI', 20, 'bold'), bg=app_color)
    display_label_name.place(relx=0, rely=0.05, relwidth=1, relheight=0.175)
    # label 2 -> result: normal/overweight etc  -------------------------------
    display_label_bmi = tk.Label(results_frame, text=display_label_bmi_message,
                                 font=('Segoe UI', 18, 'bold'), bg=app_color)
    display_label_bmi.place(relx=0, rely=0.25, relwidth=1, relheight=0.15)
    # label 3 -> info  -------------------------------------------------------
    display_label_message = tk.Label(results_frame, text=message2,
    font=('Calibri', 14, 'bold'), anchor="center", bg=app_color, bd=0, relief='groove')
    display_label_message.place(relx=0, rely=0.4, relwidth=1, relheight=0.35)

    # -------------------------        buttons          ----------------------
    display_buttons_style = ttk.Style()  # style for display frame buttons
    display_buttons_style.configure('DBS.TButton', font=('Segoe UI', 12, 'bold'))

    # button save result  -----------------------------------------------------
    save_button = ttk.Button(results_frame, text='Save Result', command=save_file,
    style='DBS.TButton')
    save_button.place(relx=0.15, rely=0.8, relwidth=0.25, relheight=0.16)
    # button close display window  --------------------------------------------
    quit_button = ttk.Button(results_frame, text='Close Window', command=close_and_clear,
    style='DBS.TButton')
    quit_button.place(relx=0.6, rely=0.8, relwidth=0.25, relheight=0.15)

    results_frame.focus()
    results_frame.grid(row=0, column=0, sticky='nswe')

    root.unbind("<KeyPress-Return>", funcid=None) #calculate_bmi)

    # ---------------         end of results frame block         --------------
#  ------------------ end of display bmi result function block ----------------


#  --------------------------     main app window    --------------------------
root = tk.Tk()

# root dimensions
root_height, root_width = 250, 600

date = datetime.datetime.now().strftime("%d-%m-%Y")  # current date in sting format

# root.geometry(f'{root_width}x{root_height}')
root.geometry('%dx%d+%d+%d' %  center_screen(root_width, root_height))
root.title('BMI Calculator App  ' + date)
root.resizable(False, False)

#  -----------------------     widget parameters      ------------------------
widget_borderwidth = 0
widget_relief = 'groove'
entry_factor = 0.75
entry_height_factor = 0.6
unit_labels_font = ('Segoe UI', 10, 'bold')
small_font = ('Segoe UI', 11, 'bold')
large_font = ('Segoe UI', 20, 'bold')
medium_font = ('Segoe UI', 13, 'bold')
radiobutton_font = ('Segoe UI', 12, 'bold')
radiobutton_font_color = 'DarkOrchid4'
calculate_button_font = ('Segoe UI', 20, 'bold')
app_color = 'lightblue'#'seashell3'
entry_field_color = 'lightgreen'#'lightblue'
button_color = 'gray50'
label_text_color = 'gray12'
left_padding = 0.05

validation = root.register(validate_data)  # used for validating user input
validation_name = root.register(validate_name)  # used for validating user input


# -----   frame 1: top frame - labels + radio buttons (metric / imperial)  ----
# -----------------------------------------------------------------------------
top_frame = tk.Frame(root, height=root_height/5*1.5, width=root_width, bg=app_color)

# top frame geometry
tf_padding = 0.01
tf_widget_width = 0.2
tf_rows = 2
tf_widget_height = (1 - tf_padding * 2) / tf_rows

# top frame widgets
factor=0.8
# -----------------------------------------------------------------------------
bmi_label = tk.Label(top_frame, text='BMI Calculator', justify='center', bd=0, relief='groove',
                     font=large_font, bg=app_color, fg=label_text_color)
bmi_label.place(relx=tf_padding, rely=tf_padding,
                relwidth=1-tf_padding*2, relheight=tf_widget_height)
# -----------------------------------------------------------------------------
metric_rb = tk.Radiobutton(top_frame, text='Metric ', value=1, font=radiobutton_font,
                           command=lambda: f_metric_rb(), bg=app_color, fg=radiobutton_font_color,
                           borderwidth=widget_borderwidth, relief=widget_relief)
metric_rb.place(relx=tf_padding+left_padding, rely=tf_padding+tf_widget_height,
                  relwidth=tf_widget_width, relheight=tf_widget_height)
# -----------------------------------------------------------------------------
imperial_rb = tk.Radiobutton(top_frame, text='Imperial', value=2, font=radiobutton_font,
                             command=lambda: f_imperial_rb(), bg=app_color, fg=radiobutton_font_color,
                             borderwidth=widget_borderwidth, relief=widget_relief)
imperial_rb.place(relx=left_padding+tf_padding+tf_widget_width, rely=tf_padding+tf_widget_height,
                  relwidth=tf_widget_width, relheight=tf_widget_height)
metric_rb.select()  # selects metric radiobutton when app starts

# -----------------------------------------------------------------------------
name_label = tk.Label(top_frame, text='Name:', justify='right', bd=0, relief='groove',
                     font=radiobutton_font, bg=app_color, fg=radiobutton_font_color)
name_label.place(relx=tf_padding+0.5, rely=tf_padding+tf_widget_height,
                relwidth=0.11, relheight=tf_widget_height)
# -----------------------------------------------------------------------------
name_entry = tk.Entry(top_frame, justify='center', bg='thistle2')
default_text = 'Enter name'
name_entry.config(fg='grey40', font=small_font)
name_entry.insert(0, default_text)
name_entry.place(relx=tf_padding+0.62, rely=tf_padding+tf_widget_height+0.07,
                relwidth=0.31, relheight=tf_widget_height*0.8)
# name_entry.config(validate="key", validatecommand=(validation_name, '%S'))
# name_entry.config(validate="key", validatecommand=(validation_name, '%s'))
name_entry.config(validate="key", validatecommand=(validation_name, '%S', '%d'))


# -----------------------------------------------------------------------------
def name_entry_focus_out(*args, **kwargs):
    name_entry.config(fg='grey15', font=small_font)
    name = name_entry.get().strip()
    name_entry.delete(0, 'end')
    name_entry.insert(0, name)

    if name_entry.get().strip() == '':
        name_entry.config(fg='grey40', font=small_font)
        name_entry.delete(0, 'end')
        name_entry.insert(0, default_text)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def name_entry_focus_in(*args, **kwargs):
    if name_entry.get() == default_text:
        name_entry.delete(0, 'end')

    name_entry.config(fg='black', font=small_font)
# -----------------------------------------------------------------------------


name_entry.bind("<FocusIn>", name_entry_focus_in)
name_entry.bind("<FocusOut>", name_entry_focus_out)

top_frame.grid(row=0, column=1, sticky='we')
# -----------------------------------------------------------------------------
# ---------------            end of frame 1 block            ------------------



# ---------     frame 2: imperial units frame - labels + entries      ---------
# -----------------------------------------------------------------------------
imperial_frame = tk.Frame(root, bg=app_color, height=root_height/5*2, width=root_width)

# imperial frame geometry
if_padding = 0.01
if_widgets = 6
if_widget_width = (1 - tf_padding * 2) / if_widgets
if_rows = 2
if_widget_height = (1 - tf_padding * 2) / tf_rows

# imperial frame widgets
# row 1
# -----------------------------------------------------------------------------
height_label_imperial = tk.Label(imperial_frame, text=' Enter your height:', bg=app_color,
                                 anchor='w', justify='left', borderwidth=widget_borderwidth,
                                 relief=widget_relief, font=medium_font, fg=label_text_color)
height_label_imperial.place(relx=left_padding+if_padding, rely=if_padding,
                            relwidth=if_widget_width*2, relheight=if_widget_height)
# -----------------------------------------------------------------------------
height_entry_feet = tk.Entry(imperial_frame, justify='center', bg=entry_field_color,
                             font=small_font)
height_entry_feet.place(relx=left_padding+if_padding+if_widget_width*2, rely=if_padding+(1-entry_height_factor)*if_widget_height/2,
                        relwidth=if_widget_width*entry_factor,
                        relheight=if_widget_height*entry_height_factor)
height_entry_feet.config(validate="key", validatecommand=(validation, '%S', '%s', '%d'))
# -----------------------------------------------------------------------------
feet_label = tk.Label(imperial_frame, text='  feet', bg=app_color, anchor='w',
                      justify='left', borderwidth=widget_borderwidth,
                      font=unit_labels_font, relief=widget_relief)
feet_label.place(relx=left_padding+if_padding+if_widget_width*2+entry_factor*if_widget_width,
                 rely=if_padding, relwidth=if_widget_width, relheight=if_widget_height)
# -----------------------------------------------------------------------------
height_entry_inches = tk.Entry(imperial_frame, justify='center', bg=entry_field_color,
                               font=small_font)
height_entry_inches.place(relx=left_padding+if_padding+if_widget_width*3+entry_factor*if_widget_width,
                          rely=if_padding+(1-entry_height_factor)*if_widget_height/2,
                        relwidth=if_widget_width*entry_factor,
                        relheight=if_widget_height*entry_height_factor)
height_entry_inches.config(validate="key", validatecommand=(validation, '%S', '%s', '%d'))
# -----------------------------------------------------------------------------
inches_label = tk.Label(imperial_frame, text='  inches', bg=app_color, anchor='w',
                        justify='left', borderwidth=widget_borderwidth,
                        font=unit_labels_font, relief=widget_relief)
inches_label.place(relx=left_padding+if_padding+if_widget_width*3+entry_factor*if_widget_width*2, rely=if_padding,
                        relwidth=if_widget_width, relheight=if_widget_height)
# row 2
# -----------------------------------------------------------------------------
weight_label_imperial = tk.Label(imperial_frame, text=' Enter your weight:',
                                 anchor='w', justify='left', bg=app_color,
                                 borderwidth=widget_borderwidth, fg=label_text_color,
                                 relief=widget_relief, font=medium_font)
weight_label_imperial.place(relx=left_padding+if_padding, rely=if_padding+if_widget_height,
                            relwidth=if_widget_width*2, relheight=if_widget_height)
# -----------------------------------------------------------------------------
stones_entry = tk.Entry(imperial_frame, justify='center', bg=entry_field_color,
                        font=small_font)
stones_entry.place(relx=left_padding+if_padding+if_widget_width*2, rely=if_padding+if_widget_height+(1-entry_height_factor)*if_widget_height/2,
                        relwidth=if_widget_width*entry_factor,
                        relheight=if_widget_height*entry_height_factor)
stones_entry.config(validate="key", validatecommand=(validation, '%S', '%s', '%d'))
# -----------------------------------------------------------------------------
stones_label = tk.Label(imperial_frame, text='  stones', bg=app_color, anchor='w',
                        justify='left', borderwidth=widget_borderwidth,
                        font=unit_labels_font, relief=widget_relief)
stones_label.place(relx=left_padding+if_padding+if_widget_width*2+entry_factor*if_widget_width, rely=if_padding+if_widget_height,
                        relwidth=if_widget_width, relheight=if_widget_height)
# -----------------------------------------------------------------------------
pounds_entry = tk.Entry(imperial_frame, justify='center', bg=entry_field_color,
                        font=small_font)
pounds_entry.place(relx=left_padding+if_padding+if_widget_width*3+entry_factor*if_widget_width, rely=if_padding+if_widget_height+(1-entry_height_factor)*if_widget_height/2,
                        relwidth=if_widget_width*entry_factor,
                        relheight=if_widget_height*entry_height_factor)
pounds_entry.config(validate="key", validatecommand=(validation, '%S', '%s', '%d'))
# -----------------------------------------------------------------------------
pounds_label = tk.Label(imperial_frame, text='  pounds', bg=app_color, anchor='w',
                        justify='left', borderwidth=widget_borderwidth,
                        font=unit_labels_font, relief=widget_relief)
pounds_label.place(relx=left_padding+if_padding+if_widget_width*3+entry_factor*if_widget_width*2,
                   rely=if_padding+if_widget_height, relwidth=if_widget_width,
                   relheight=if_widget_height)

imperial_frame.grid(row=1, column=1, sticky='we')
# ---------------            end of frame 2 block            ------------------


# ---------     frame 3: metric units frame - labels + entries      ---------
# -----------------------------------------------------------------------------
metric_frame = tk.Frame(root, bg=app_color, height=root_height/5*2, width=root_width)

# metric frame geometry
mf_padding = 0.01
mf_widgets = 6
mf_widget_width = (1 - mf_padding * 2) / mf_widgets
mf_rows = 2
mf_widget_height = (1 - mf_padding * 2) / tf_rows

# metric frame widgets
# row 1
# -----------------------------------------------------------------------------
height_label_metric = tk.Label(metric_frame, text=' Enter your height:',  anchor='w',
                               justify='left', borderwidth=widget_borderwidth, fg=label_text_color,
                               relief=widget_relief, font=medium_font, bg=app_color)
height_label_metric.place(relx=left_padding+mf_padding, rely=mf_padding, relwidth=mf_widget_width*2, relheight=mf_widget_height)
# # -----------------------------------------------------------------------------
height_entry_cm = tk.Entry(metric_frame, justify='center', bg=entry_field_color,
                           font=small_font)
height_entry_cm.place(relx=left_padding+mf_padding+mf_widget_width*2,
                      rely=mf_padding+(1-entry_height_factor)*mf_widget_height/2,
                      relwidth=mf_widget_width*entry_factor,
                      relheight=mf_widget_height*entry_height_factor)
height_entry_cm.config(validate="key", validatecommand=(validation, '%S', '%s', '%d'))
# -----------------------------------------------------------------------------
cm_label = tk.Label(metric_frame, text='  centimeters', bg=app_color, anchor='w',
                    justify='left', borderwidth=widget_borderwidth,
                    font=unit_labels_font, relief=widget_relief)
cm_label.place(relx=left_padding+mf_padding+mf_widget_width*2+entry_factor*mf_widget_width, rely=mf_padding,
                        relwidth=mf_widget_width, relheight=mf_widget_height)
# row 2
# -----------------------------------------------------------------------------
weight_label_metric = tk.Label(metric_frame, text=' Enter your weight:', anchor='w',
                               justify='left', borderwidth=widget_borderwidth, fg=label_text_color,
                               relief=widget_relief, font=medium_font, bg=app_color)
weight_label_metric.place(relx=left_padding+mf_padding, rely=mf_padding+mf_widget_height,
                          relwidth=mf_widget_width*2, relheight=mf_widget_height)
# -----------------------------------------------------------------------------
kilograms_entry = tk.Entry(metric_frame, justify='center', bg=entry_field_color,
                           font=small_font)
kilograms_entry.place(relx=left_padding+mf_padding+mf_widget_width*2,
                      rely=mf_padding+mf_widget_height+(1-entry_height_factor)*mf_widget_height/2,
                          relwidth=mf_widget_width*entry_factor,
                          relheight=mf_widget_height*entry_height_factor)
kilograms_entry.config(validate="key", validatecommand=(validation, '%S', '%s', '%d'))
# -----------------------------------------------------------------------------
kilograms_label = tk.Label(metric_frame, text='  kilograms', bg=app_color, anchor='w',
                           justify='left', borderwidth=widget_borderwidth,
                           font=unit_labels_font, relief=widget_relief)
kilograms_label.place(relx=left_padding+mf_padding+mf_widget_width*2+entry_factor*mf_widget_width,
                      rely=mf_padding+mf_widget_height,
                      relwidth=mf_widget_width, relheight=mf_widget_height)

metric_frame.grid(row=1, column=1, sticky='we')
# ---------------            end of frame 3 block            ------------------


# ---------          frame 4: bottom frame - calculate button         ---------
# -----------------------------------------------------------------------------
bottom_frame = tk.Frame(root, bg=app_color, height=root_height/5*1.5, width=root_width)

# bottom frame widgets
# -----------------------------------------------------------------------------
button_style = ttk.Style()
button_style.configure('W.TButton', justify='center', font=calculate_button_font,
                       bg=button_color, bd=10, fg='darkblue', relief="raised")
calculate_button = ttk.Button(bottom_frame, style='W.TButton', text='Calculate BMI',
                             command=lambda: calculate_bmi())
calculate_button.place(relx=0.275, rely=0.15, relwidth=0.45, relheight=0.7)

bottom_frame.grid(row=2, column=1, sticky='we')
# ---------------            end of frame 4 block            ------------------


# def push_enter(*args, **kwargs):
#     add_task(datafile, entry_task.get())

# root.bind("<KeyPress-Return>", push_enter)

# when app starts metric frame is active
kilograms_entry.config(takefocus=True)
height_entry_cm.config(takefocus=True)
height_entry_feet.config(takefocus=False)
height_entry_inches.config(takefocus=False)
stones_entry.config(takefocus=False)
pounds_entry.config(takefocus=False)

metric_rb.focus()

calculate_button.config(takefocus=False)

root.bind("<KeyPress-Return>", calculate_bmi)
# root.bind("<KeyPress-Escape>", lambda x: root.destroy())


root.mainloop()
