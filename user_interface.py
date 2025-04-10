from tkinter import *
from tkinter import ttk
from algorithm import *

root = Tk()
root.title("Needleman Wunsch Algorithm")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

first_sentence = StringVar()
second_sentence = StringVar()
missmatch_penalty = StringVar()
gap_penalty = StringVar()
match_score = StringVar()

first_sentence_entry = ttk.Entry(mainframe, width=7, textvariable=first_sentence)
second_sentence_entry = ttk.Entry(mainframe, width=7, textvariable=second_sentence)
missmatch_penalty_entry = ttk.Entry(mainframe, width=7, textvariable=missmatch_penalty)
gap_penalty_entry = ttk.Entry(mainframe, width=7, textvariable=gap_penalty)
match_score_entry = ttk.Entry(mainframe, width=7, textvariable=match_score)

ttk.Label(mainframe, text="First sentence").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Second sentence").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Match score").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Missmatch penalty").grid(column=3, row=2, sticky=W)
ttk.Label(mainframe, text="Gap penalty").grid(column=1, row=3, sticky=W)

first_sentence_entry.grid(column=2, row=1, sticky=(W, E))
second_sentence_entry.grid(column=4, row=1, sticky=(W, E))
missmatch_penalty_entry.grid(column=4, row=2, sticky=(W, E))
gap_penalty_entry.grid(column=2, row=3, sticky=(W, E))
match_score_entry.grid(column=2, row=2, sticky=(W, E))

(ttk.Button(mainframe,
           text="Calculate",
           command=lambda: main(first_sentence.get(),
                                second_sentence.get(),
                                int(match_score.get()),
                                int(missmatch_penalty.get()),
                                int(gap_penalty.get())))
           .grid(column=1, row=5, columnspan=5, sticky=(W, E)))

# first_sentence second_sentence missmatch_penalty gap_penalty match_score
root.mainloop()