#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import PySimpleGUI as sg
import pandas as pd
import numpy as np
import pickle
from PIL import Image, ImageOps
import webbrowser
data_ecc = pd.read_excel('comb_data_ecc_USED.xlsx')[['shape', 'rohsv', 'fsv', 'fco', 'Vf', 'Ke', 'ecc']]
data_ecu = pd.read_excel('comb_data_ecu_USED.xlsx')[['shape', 'rohsv', 'fsv', 'fco', 'Vf', 'Ke', 'ecu']]
data_fcc = pd.read_excel('comb_data_fcc_USED.xlsx')[['shape', 'rohsv', 'fsv', 'fco', 'Vf', 'Ke', 'fcc']]
data_fcu = pd.read_excel('comb_data_fcu_USED.xlsx')[['shape', 'rohsv', 'fsv', 'fco', 'Vf', 'Ke', 'fcu']]
parameters = ['rohsv', 'fsv', 'fco', 'Vf', 'Ke']
ranges = {}
for param in parameters:
    min_values = [data_ecc[param].min(), data_ecu[param].min(), data_fcc[param].min(), data_fcu[param].min()]
    max_values = [data_ecc[param].max(), data_ecu[param].max(), data_fcc[param].max(), data_fcu[param].max()]
    
    ranges[param] = [round(max(min_values), 4), round(max(max_values),4)]
import PySimpleGUI as sg
shape_choices = ['Rectangular', 'Circular']
sg.theme('DefaultNoMoreNagging')
img = Image.open('stress_strain.png')
original_width, original_height = img.size
scl = 0.5
scaled_width = int(original_width * scl)
scaled_height = int(original_height * scl)
scaled_img = img.resize((scaled_width, scaled_height))
scaled_img_filename = 'scaled_stress_strain.png'
scaled_img.save(scaled_img_filename)

def check_value(value, range):
    try:
        float_value = float(value)
        if range[0] <= float_value <= range[1]:
            return True
    except ValueError:
        pass
    return False
def OpenLink(url):
    webbrowser.open_new(url)
def create_link_label(text, url):
    root = tk.Tk()
    root.withdraw()
    label = tk.Label(root, text=text, fg="blue", cursor="hand2")
    label.pack()
    label.bind("<Button-1>", lambda event: handle_link_click(url))
    return label
    
layout = [
    [sg.Text('Define the input parameters', text_color='blue', font=(''))],
    [
        sg.Column(layout=[
            [sg.Frame(layout=[
                [sg.Text('Shape', size=(38, 1)), sg.Combo(shape_choices, default_value='Rectangular', key='-shape-', size=(15, 1))],
                [sg.Text('Transverse reinforcement ratio, rohsv', size=(38, 1)), sg.Input(key='-rohsv-', size=(15, 1), enable_events=True)],
                [sg.Text('Yield strength of transverse reinforcement, fsv (MPa)', size=(38, 1)), sg.Input(key='-fsv-', size=(15, 1), enable_events=True)],
                [sg.Text('Compressive strength of unconfined UHPC, fco (MPa)', size=(38, 1)), sg.Input(key='-fco-', size=(15, 1), enable_events=True)],
                [sg.Text('Fiber volumetric ratio, Vf (%)', size=(38, 1)), sg.Input(key='-Vf-', size=(15, 1), enable_events=True)],
                [sg.Text('Effective confinement, Ke', size=(38, 1)), sg.Input(key='-Ke-', size=(15, 1), enable_events=True)]],
            title='Input parameters')], 
        ], justification='left'),

        sg.Column(layout=[
            [sg.Frame(layout=[
                [sg.Text('Shape: Rectangular or Circular')],
                [sg.Text(f'{ranges["rohsv"][0]} ≤ rohsv ≤ {ranges["rohsv"][1]}')],
                [sg.Text(f'{ranges["fsv"][0]} ≤ fsv ≤ {ranges["fsv"][1]}')],
                [sg.Text(f'{ranges["fco"][0]} ≤ fco ≤ {ranges["fco"][1]}')],
                [sg.Text(f'{ranges["Vf"][0]} ≤ Vf ≤ {ranges["Vf"][1]}')],
                [sg.Text(f'{ranges["Ke"][0]} ≤ Ke ≤ {ranges["Ke"][1]}')]],
            title='Range of applications of the model')],             
        ], justification='center')
    ],

    [
        sg.Button('Predict'), sg.Button('Cancel')
    ],
    [sg.Text('')],    
    
    [sg.Text('Predicted peak and ultimate stress-strain respones of confined UHPC', text_color='blue', font=(''))],
    [
        sg.Frame(layout=[
            [sg.Text(' ')],
            [sg.Text('Peak stress, fcc (MP)', size=(25, 1)), sg.InputText('', key='-fcc-', size=(15, 1))],
            [sg.Text('Peak strain, εcc', size=(25, 1)), sg.InputText('', key='-ecc-', size=(15, 1))],
            [sg.Text('Ultimate stress, fcu (MPa)', size=(25, 1)), sg.InputText('', key='-fcu-', size=(15, 1))],
            [sg.Text('Ultimate strain, εcu', size=(25, 1)), sg.InputText('', key='-ecu-', size=(15, 1))],
            [sg.Text('')],
        ],
        title='Output'),
        sg.Column(layout=[
            [sg.Image(filename=scaled_img_filename, key='-fig1-')],
            [sg.Text('Figure: Peak and ultimate stress-strain responses.')]
        ]
                 )
    ],
]
img2 = Image.open('image2.png')
img4 = Image.open('image4.png')
widths = [img2.width, img4.width]
heights = [img2.height,  img4.height]
min_width = min(widths)
min_height = min(heights)
img2 = ImageOps.fit(img2, (min_width, min_height))
img4 = ImageOps.fit(img4, (min_width, min_height))
scale_factor = 0.25
img2 = img2.resize((int(min_width * scale_factor), int(min_height * scale_factor)))
img4 = img4.resize((int(min_width * scale_factor), int(min_height * scale_factor)))
img2.save('image22.png')
img4.save('image44.png')
fig2 = sg.Image(filename='image22.png', key='-fig2-', size=(min_width * scale_factor, min_height * scale_factor))
fig4 = sg.Image(filename='image44.png', key='-fig4-', size=(min_width * scale_factor, min_height * scale_factor))
layout += [
    [sg.Text('')],
    [sg.Column([
    [sg.Text('Authors: Tadesse G. Wakjira and M. Shahria Alam'+ '\n'
             '             The University of British Columbia, Okanagan')],
    [
     sg.Button('www.tadessewakjira.com/Contact', key='WEBSITE', button_color=('white', 'gray')),
     sg.Button('https://alams.ok.ubc.ca', key='WEBSITE', button_color=('white', 'gray')),
    ]
    ],
    element_justification='left'
    ),
        sg.Column(
            [   [fig2,
                fig4,
                ],
            ],
            element_justification='center'
        ),
    ],

    [sg.Text("   If you utilize this software for your work, we kindly request that you cite the corresponding paper as a reference.", 
             size=(90, 1), 
             border_width=1, 
             relief=sg.RELIEF_SUNKEN, 
             background_color='white',
             text_color='black',
             font=('Helvetica', 8, 'bold'))],
]
window = sg.Window('ConUHPC-HybridOptML-CTGU', layout)
w2_fcc = 0.5120249797347537
w3_fcc = 0.09548557049699438
w4_fcc = 0.15311417312866968
w2_ecc = 0.666070021389532
w3_ecc = 0.032966395402373894
w4_ecc = 0.672580119475696
w2_ecu = 0.5324452696592009
w3_ecu = 0.11772675931709439
w4_ecu = 0.7260459180677157
w2_fcu = 0.017534791488202625
w3_fcu = 0.5713179955166596
w4_fcu = 0.7954487296808732
m1_ecc = pickle.load(open('model1_ecc.pkl', 'rb'))
m2_ecc = pickle.load(open('model2_ecc.pkl', 'rb'))
m3_ecc = pickle.load(open('model3_ecc.pkl', 'rb'))
m4_ecc = pickle.load(open('model4_ecc.pkl', 'rb'))
m1_fcc = pickle.load(open('model1_fcc.pkl', 'rb'))
m2_fcc = pickle.load(open('model2_fcc.pkl', 'rb'))
m3_fcc = pickle.load(open('model3_fcc.pkl', 'rb'))
m4_fcc = pickle.load(open('model4_fcc.pkl', 'rb'))
m1_fcu = pickle.load(open('model1_fcu.pkl', 'rb'))
m2_fcu = pickle.load(open('model2_fcu.pkl', 'rb'))
m3_fcu = pickle.load(open('model3_fcu.pkl', 'rb'))
m4_fcu = pickle.load(open('model4_fcu.pkl', 'rb'))
m1_ecu = pickle.load(open('model1_ecu.pkl', 'rb'))
m2_ecu = pickle.load(open('model2_ecu.pkl', 'rb'))
m3_ecu = pickle.load(open('model3_ecu.pkl', 'rb'))
m4_ecu = pickle.load(open('model4_ecu.pkl', 'rb'))
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event == 'Predict':
        try:
            shape = values['-shape-']
            rohsv = float(values['-rohsv-'])
            fsv = float(values['-fsv-'])
            fco = float(values['-fco-'])
            Vf = float(values['-Vf-'])
            Ke = float(values['-Ke-'])
            shape = 0 if shape == 'Circular' else 1 if shape == 'Rectangular' else shape
            df = pd.DataFrame([[shape, rohsv, fsv, fco, Vf, Ke]], columns=['shape', 'rohsv', 'fsv', 'fco', 'Vf', 'Ke'])
            dfn_ecc = (df - data_ecc.drop(columns='ecc').min()) / (data_ecc.drop(columns='ecc').max() - data_ecc.drop(columns='ecc').min())
            dfn_fcc = (df - data_fcc.drop(columns='fcc').min()) / (data_fcc.drop(columns='fcc').max() - data_fcc.drop(columns='fcc').min())
            dfn_fcu = (df - data_fcu.drop(columns='fcu').min()) / (data_fcu.drop(columns='fcu').max() - data_fcu.drop(columns='fcu').min())
            dfn_ecu = (df - data_ecu.drop(columns='ecu').min()) / (data_ecu.drop(columns='ecu').max() - data_ecu.drop(columns='ecu').min())
            m1_preds_ecc = m1_ecc.predict(dfn_ecc)
            m2_preds_ecc = m2_ecc.predict(dfn_ecc)
            m3_preds_ecc = m3_ecc.predict(dfn_ecc)
            m4_preds_ecc = m4_ecc.predict(dfn_ecc)
            predicted_ecc = m1_preds_ecc + w2_ecc*m2_preds_ecc + w3_ecc*m3_preds_ecc + w4_ecc*m4_preds_ecc
            predicted_ecc = predicted_ecc * (data_ecc['ecc'].max() - data_ecc['ecc'].min()) + data_ecc['ecc'].min()
            m1_preds_fcc = m1_fcc.predict(dfn_fcc)
            m2_preds_fcc = m2_fcc.predict(dfn_fcc)
            m3_preds_fcc = m3_fcc.predict(dfn_fcc)
            m4_preds_fcc = m4_fcc.predict(dfn_fcc)
            predicted_fcc = m1_preds_fcc + w2_fcc*m2_preds_fcc + w3_fcc*m3_preds_fcc + w4_fcc*m4_preds_fcc
            predicted_fcc = predicted_fcc * (data_fcc['fcc'].max() - data_fcc['fcc'].min()) + data_fcc['fcc'].min()
            m1_preds_fcu = m1_fcu.predict(dfn_fcu)
            m2_preds_fcu = m2_fcu.predict(dfn_fcu)
            m3_preds_fcu = m3_fcu.predict(dfn_fcu)
            m4_preds_fcu = m4_fcu.predict(dfn_fcu)
            predicted_fcu = m1_preds_fcu + w2_fcu*m2_preds_fcu + w3_fcu*m3_preds_fcu + w4_fcu*m4_preds_fcu
            predicted_fcu = predicted_fcu * (data_fcu['fcu'].max() - data_fcu['fcu'].min()) + data_fcu['fcu'].min()
            m1_preds_ecu = m1_ecu.predict(dfn_ecu)
            m2_preds_ecu = m2_ecu.predict(dfn_ecu)
            m3_preds_ecu = m3_ecu.predict(dfn_ecu)
            m4_preds_ecu = m4_ecu.predict(dfn_ecu)
            predicted_ecu = m1_preds_ecu + w2_ecu*m2_preds_ecu + w3_ecu*m3_preds_ecu + w4_ecu*m4_preds_ecu
            predicted_ecu = predicted_ecu * (data_ecu['ecu'].max() - data_ecu['ecu'].min()) + data_ecu['ecu'].min()
            window['-ecc-'].update(np.round(predicted_ecc[0], 5))
            window['-fcc-'].update(np.round(predicted_fcc[0], 2))
            window['-fcu-'].update(np.round(predicted_fcu[0], 2))
            window['-ecu-'].update(np.round(predicted_ecu[0], 5))
        except Exception as e:
            sg.popup(f"Error: {e}\n\nInvalid input. Please make sure to enter numeric values.")
            continue
    elif event == 'EMAIL':
        OpenLink('mailto:tgwakjira@gmail.com')
    elif event == 'WEBSITE':
        OpenLink('http://www.tadessewakjira.com/Contact')

