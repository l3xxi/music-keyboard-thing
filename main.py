import tkinter

'''
    TODO
    could probably use occlusion culling, if you want stupidly many keys i guess
    make keys have the correct note name on them
    make the keys interactable
    make the keys play sound
    add support for microtonal sound  ## MAYBE ##
'''




'''
    This fuction is genuinely of the worst ive ever written, I pray nobody ever sees this.
    : (

'''

def create_piano_dicts():
    global white_note_count
    white_note_count = 0
    for i in range(starting_note,total_notes+starting_note):
        note = i % notes_per_octave
        if note in [0,2,4,5,7,9,11]: # Just yeah
            white_keys.append({
            'x0': (white_note_width*white_note_count),
            'y0':  0,
            'x1': (white_note_width*white_note_count)+white_note_width,
            'y1': screen_height,
            'text': note_list[note]+str(i//notes_per_octave),
            'note_colour': 'white',
            'text_colour': 'black'})
            white_note_count += 1
        elif note in [1,3,6,8,10]:
            black_keys.append({
            'x0': (white_note_width*white_note_count)-black_note_width,
            'y0': 0,
            'x1': (white_note_width*white_note_count)+black_note_width,
            'y1': screen_height*5/8,
            'text': note_list[note]+str(i//notes_per_octave),
            'note_colour': 'black',
            'text_colour': 'white'})

def draw_piano_roll():
    for i in white_keys:
        x0 = i['x0']-offset; print(x0)
        x1 = i['x1']-offset; print(x1)
        y0 = i['y0']
        y1 = i['y1']

        canv.create_rectangle(x0,y0,x1,y1,fill=i['note_colour'])
        canv.create_text((x0+x1)/2,y1/1.2,text=i['text'],fill=i['text_colour'],font=('Arial', 25))
    for i in black_keys:
        x0 = i['x0']-offset;# print(x0)
        x1 = i['x1']-offset;# print(x1)
        y0 = i['y0']
        y1 = i['y1']

        canv.create_rectangle(x0,y0,x1,y1,fill=i['note_colour'])
        canv.create_text((x0+x1)/2,y1/1.2,text=i['text'],fill=i['text_colour'],font=('Arial', 25))

def update_piano_roll(index,new_value):
    for i in white_keys + black_keys:
        i[index] = new_value


def clear_piano_roll():
    global canv
    canv.delete("all")


def move_view(scale):
    global offset
    factor = abs(white_note_width*(white_note_count-7))
    offset = factor*(int(scale)/100)
    #print(offset)
    clear_piano_roll() 
    draw_piano_roll() 


# Initialise constants

screen_width = 1280
screen_height = 720

notes_per_octave = 12
total_notes = 88
note_scale = 7
offset = 0
starting_note = 9
note_list = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
white_note_count: int

white_note_width = screen_width//note_scale
black_note_width = white_note_width//3 # Magic number

white_keys = []
black_keys = []

# Tkinter stuff

root = tkinter.Tk()
root.geometry(f"{screen_width}x{screen_height}")
canv = tkinter.Canvas(root,width=screen_width,height=screen_height-80) # Oh theres another
slide = tkinter.Scale(root, from_=0,to=100,command=move_view,orient='horizontal',length=screen_width,showvalue=True)

canv.pack()
slide.pack()

create_piano_dicts()
draw_piano_roll()
root.mainloop()