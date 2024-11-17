import tkinter

'''
    TODO
    could probably use occlusion culling, if you want stupidly many keys i guess[NOT NEEDED FOR NOW]
    make keys have the correct note name on them[DONE]
    make the keys interactable [DIBE]
    make the keys play sound
    add support for microtonal sound  ## MAYBE ##
'''


class Note:
    def __init__(self, x0,y0,x1,y1,text,note_colour,text_colour):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.text = text
        self.note_colour = note_colour
        self.text_colour = text_colour
        self.default_colour = note_colour
    def click(self,x2,y2):
        if (x2 > self.x0 and x2 < self.x1) and (y2 > self.y0 and y2 < self.y1):
            return True



def create_piano_dicts():
    global white_note_count
    global white_keys
    global black_keys
    white_keys = []
    black_keys = []
    white_note_count = 0
    for i in range(starting_note,total_notes+starting_note):
        note = i % notes_per_octave
        if note in [0,2,4,5,7,9,11]: # Just yeah
            white_keys.append(Note(
            x0 = (white_note_width*white_note_count),
            y0 =  0,
            x1 = (white_note_width*white_note_count)+white_note_width,
            y1 = canv_height,
            text = note_list[note]+str(i//notes_per_octave),
            note_colour = 'white',
            text_colour = 'black'))
            white_note_count += 1
        elif note in [1,3,6,8,10]:
            black_keys.append(Note(
            x0 = (white_note_width*white_note_count)-black_note_width,
            y0 = 0,
            x1 = (white_note_width*white_note_count)+black_note_width,
            y1 = canv_height*5/8,
            text = note_list[note]+str(i//notes_per_octave),
            note_colour = '#000000',
            text_colour = 'white'))


def change_key_colour(key, new_colour):
    key.note_colour = new_colour
    clear_piano_roll()
    draw_piano_roll()


def click_check(pos):
    for i in black_keys:
        if i.click(pos.x+scrollbar_offset,pos.y):
            change_key_colour(i, '#999999')
            root.after(colour_change_duration, lambda : change_key_colour(i,i.default_colour))
            return
    for i in white_keys:
        if i.click(pos.x+scrollbar_offset,pos.y):
            change_key_colour(i, '#999999')
            root.after(colour_change_duration, lambda : change_key_colour(i,i.default_colour))
            return


def draw_piano_roll():
    for i in white_keys:
        x0 = i.x0-scrollbar_offset+draw_offset
        x1 = i.x1-scrollbar_offset+draw_offset
        y0 = i.y0+draw_offset
        y1 = i.y1+draw_offset

        canv.create_rectangle(x0,y0,x1,y1,fill=i.note_colour,width=5)
        canv.create_text((x0+x1)/2,y1/1.2,text=i.text,fill=i.text_colour,font=('Arial', font_size))
    for i in black_keys:
        x0 = i.x0-scrollbar_offset+draw_offset
        x1 = i.x1-scrollbar_offset+draw_offset
        y0 = i.y0+draw_offset
        y1 = i.y1+draw_offset

        canv.create_rectangle(x0,y0,x1,y1,fill=i.note_colour,width=5)
        canv.create_text((x0+x1)/2,y1/1.2,text=i.text,fill=i.text_colour,font=('Arial', font_size))


def clear_piano_roll():
    global canv
    canv.delete("all")


def move_view(scale):
    global scrollbar_offset
    scale_num = int(scale)
    factor = abs(white_note_width*(white_note_count-7))
    scrollbar_offset = factor*(scale_num/100)+draw_offset
    clear_piano_roll() 
    draw_piano_roll() 


def change_note_scale(scale):
    global note_scale
    global white_note_width
    global black_note_width
    global font_size
    note_scale = int(scale)*(7/12)
    white_note_width = canv_width//note_scale
    black_note_width = white_note_width//3
    font_size = int((screen_width/note_scale)**0.6)
    create_piano_dicts()
    clear_piano_roll()
    draw_piano_roll()

# Initialise constants

screen_width = 1280
screen_height = 720

canv_width = 1280
canv_height = screen_height-60

notes_per_octave = 12
total_notes = 88
note_scale = 12
scrollbar_offset = 0
draw_offset = 5
starting_note = 9
note_list = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
white_note_count = 0

white_note_width = canv_width//note_scale
black_note_width = white_note_width//3 # Magic number

colour_change_duration = 50
font_size = int((screen_width/note_scale)**0.6)

white_keys = []
black_keys = []

# Tkinter stuff

root = tkinter.Tk()
root.geometry(f"{screen_width}x{screen_height}")
root.bind('<Button-1>',click_check)

canv = tkinter.Canvas(root,width=canv_width,height=canv_height+draw_offset,border=0) # Oh theres another
view_move = tkinter.Scale(root, from_=0,to=100,command=move_view,orient='horizontal',length=screen_width,showvalue=False)
view_move.set(50)
note_scale_slide = tkinter.Scale(root, from_=1,to=total_notes,command=change_note_scale,orient='horizontal',length=screen_width,showvalue=True)
note_scale_slide.set(note_scale)

canv.pack()
view_move.pack()
note_scale_slide.pack()

create_piano_dicts()
draw_piano_roll()
root.mainloop()