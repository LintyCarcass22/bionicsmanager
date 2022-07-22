import tkinter as tk
from tkinter import messagebox

import tkinter.ttk as ttk
import functions as fn

# // GUI functions
loaded = ""
special = "`*~*`"
def cmd_load():
    dir, nme = fn.h_parse_dir(nme_stv)

    if not fn.f_find(dir):
        status_stv.set(f'could not find "{nme}" in instances folder.')
        return

    status_stv.set(f'succesfully loaded "{nme}".')
    global loaded
    loaded = nme
    fn.h_tk_ss("DISABLED", disable_lst)
    fn.h_tk_ss("ACTIVE", disable_lst_inv)

    dta = fn.f_read(dir)

    for cat in dta["bionics"]:
        bnc_trv.insert(parent='bionics', index="end", iid=  cat  , text=cat)
        bnc_trv.insert(parent= 'done'  , index="end", iid=cat+special, text=cat)
        for bnc in dta["bionics"][cat]:
            if dta["bionics"][cat][bnc] == 0: 
                bnc_trv.insert(parent=cat+special, index="end", iid=bnc, text=bnc)
            else:
                bnc_trv.insert(parent=cat, index="end", iid=bnc, text=bnc, values=dta["bionics"][cat][bnc])

    bnc_trv.item("bionics", open=True)
    bnc_trv.item("done", open=True)

    total, done, progress = fn.h_calc_prog(dir)
    prog_bar["value"] = progress
    prog_lb.config(text=f"({done}/{total}) {progress}%")

def cmd_unload():
    global loaded
    if loaded == '': return
    loaded = ''
    status_stv.set(f'succesfully unloaded instance.')

    cats = bnc_trv.get_children("bionics") + bnc_trv.get_children("done")
    for cat in cats:
        bnc_trv.delete(cat)
    fn.h_tk_ss("ACTIVE", disable_lst)
    fn.h_tk_ss("DISABLED", disable_lst_inv)

    prog_bar["value"] = 0
    prog_lb.config(text="(0/0) 0%")

def cmd_create():
    dir, nme = fn.h_parse_dir(nme_stv)
    if fn.f_find(dir):
        messagebox.showinfo(title="Instance already exists", message=f"""Found an existing instance called "{nme}".
Either delete it if you wish to create an instance with the same name, or choose a different name for your new instance.""")
        return
    fn.c_create(dir, amt_pns_int.get())
    cmd_load()

def cmd_delete():
    dir, nme = fn.h_parse_dir(nme_stv)
    if not fn.f_find(dir):
        status_stv.set(f'could not find "{nme}" in instances folder.')
        return
    if messagebox.askyesno(title="Delete instance?", message=f"Are you sure you want to delete instance \"{nme}\"?") == False: return

    if loaded == nme: cmd_unload()
    status_stv.set(f'succesfully deleted instance "{nme}".')
    fn.f_remove(dir)

def cmd_set():
    dir = fn.h_parse_dir(nme_stv)[0]
    amt = amt_bnc_int.get()
    bnc = bnc_trv.focus()

    status_stv.set(f'succesfully changed {bnc} amount to {amt}.')

    dta = fn.f_read(dir)
    
    for cat in dta["bionics"]:
        if bnc in dta["bionics"][cat]:
            if bnc_trv.parent(bnc).endswith(special) and amt: #check if in "done"
                bnc_trv.move(item=bnc, parent=cat, index="end")
            fn.c_change(dir, bnc, amt)
            if amt == 0:
                bnc_trv.move(item=bnc, parent=cat+special, index="end")
                amt = ''
            bnc_trv.item(bnc, values=amt)

    total, done, progress = fn.h_calc_prog(dir)
    prog_bar["value"] = progress
    prog_lb.config(text=f"({done}/{total}) {progress}%")
    
# // GUI itself
#0
root = tk.Tk()

# looks
im_load  =  fn.h_icon_loader( "load.png" )
im_create = fn.h_icon_loader("create.png")
im_unload = fn.h_icon_loader("unload.png")
im_delete = fn.h_icon_loader("delete.png")
im_set  =   fn.h_icon_loader( "set.png"  )
im_icon =   fn.h_icon_loader( "icon.png" )
root.iconphoto(True, im_icon)
root.title("Bionics manager")
root.geometry("380x850")
root.minsize(380, 850)
root.configure(bg="#DCDAD5")
s = ttk.Style()
s.theme_use("clam")

#00
lf_cfg = ttk.Labelframe(root, text="Config management")
fr_cfg = ttk.Frame(lf_cfg)
fr_cfg.grid_columnconfigure(0, weight=1)
fr_cfg.grid(row=0, column=0, sticky='we')
#000
fr_nme = ttk.Frame(fr_cfg)
dir_lb = ttk.Label(fr_nme, text=str(fn.dir_root / "instances") + "\\")
json_lb = ttk.Label(fr_nme, text=".json")
nme_stv = tk.StringVar(fr_nme, "default")
nme_ntr = ttk.Entry(fr_nme, textvariable=nme_stv, width=10, )
#001
fr_amt_pns = ttk.Frame(fr_cfg)
amt_pns_lb = ttk.Label(fr_amt_pns, text="Amount of Pawns: ")
amt_pns_int = tk.IntVar(fr_amt_pns, 1)
amt_pns_spb = ttk.Spinbox(fr_amt_pns, from_=1, to=99, textvariable=amt_pns_int, width=2)
#002
fr_btns = ttk.Frame(fr_cfg)
load_btn  =  ttk.Button(fr_btns, text= "Load" , command= cmd_load , image= im_load , compound="bottom", width=8)
create_btn = ttk.Button(fr_btns, text="Create", command=cmd_create, image=im_create, compound="bottom", width=8)
unload_btn = ttk.Button(fr_btns, text="Unload", command=cmd_unload, image=im_unload, compound="bottom", width=8)
delete_btn = ttk.Button(fr_btns, text="Delete", command=cmd_delete, image=im_delete, compound="bottom", width=8)
#01
lf_bnc = ttk.LabelFrame(root, text="Bionic management")
set_btn = ttk.Button(lf_bnc, text="Set", command=cmd_set, image=im_set, compound="right", width=4)

bnc_trv = ttk.Treeview(lf_bnc, columns="#1", height=20)
bnc_trv.column("#0", width=10, minwidth=10, stretch=True)
bnc_trv.column("#1", width=30, minwidth=30, stretch=False, anchor='e')
bnc_trv.heading("#0", text="Bionic", anchor='w')
bnc_trv.heading("#1", text="#")
bnc_trv.insert(parent='', index="end", iid="bionics", text="Unfinished")
bnc_trv.insert(parent='', index="end", iid="done", text="Processed")
#010
fr_amt_bnc = ttk.Frame(lf_bnc)
amt_bnc_lb = ttk.Label(fr_amt_bnc, text="New amount of bionics:")
amt_bnc_int = tk.IntVar(fr_amt_bnc, value=0)
amt_bnc_cb = ttk.Spinbox(fr_amt_bnc, from_=0, to=999, textvariable=amt_bnc_int, width=3)
#02
fr_prog = ttk.Frame(root)
prog_lb = ttk.Label(fr_prog, text="(0/0) 0%")
prog_bar = ttk.Progressbar(fr_prog)
#99
fr_status = ttk.Frame(root)
statustxt_lb = ttk.Label(fr_status, text="Status:")
status_stv = tk.StringVar(fr_status, "Waiting for input...")
status_lb = ttk.Label(fr_status, textvariable=status_stv)

# // 
disable_lst = [nme_ntr, amt_pns_spb, load_btn, create_btn]
disable_lst_inv = [set_btn, amt_bnc_cb, unload_btn]
fn.h_tk_ss("DISABLED", disable_lst_inv)
#disable_lst_inv.pop()
#0
root.grid(widthInc=800, heightInc=800)
root.rowconfigure(index=1, weight=1)
root.columnconfigure(0, weight=1)
#00
lf_cfg.grid(row=0, column=0, padx=4, pady=4, sticky='we')
lf_cfg.columnconfigure(index=0, weight=1)
#000
fr_nme.grid(row=0, column=0, padx=4, pady=4, sticky='we')
fr_nme.columnconfigure(index=1, weight=1)
dir_lb.grid(row=0, column=0)
nme_ntr.grid(row=0, column=1, sticky='we')
json_lb.grid(row=0, column=2)
#001
fr_amt_pns.grid(row=1, column=0, padx=4, pady=4)
amt_pns_lb.grid(row=0, column=0)
amt_pns_spb.grid(row=0, column=1)
#002
fr_btns.grid(row=2, column=0, pady=4, sticky='we')
fr_btns.columnconfigure(index=0, weight=1)
fr_btns.columnconfigure(index=1, weight=1)
load_btn.grid  (row=0, column=0, padx=2, pady=4, sticky='we')
create_btn.grid(row=0, column=1, padx=2, pady=4, sticky='we')
unload_btn.grid(row=1, column=0, padx=2, sticky='we')
delete_btn.grid(row=1, column=1, padx=2, sticky='we')
#01
lf_bnc.grid(row=1, column=0, padx=4, pady=4, sticky='wnse')
lf_bnc.columnconfigure(index=0, weight=1)
lf_bnc.rowconfigure(index=1, weight=1)
set_btn.grid(row=0, column=2, padx=4, pady=4, sticky='e')
bnc_trv.grid(row=1, columnspan=3, padx=4, pady=4, sticky='nwse')
#010
fr_amt_bnc.grid(row=0, column=0, padx=4, pady=4)
amt_bnc_lb.grid(row=0, column=0)
amt_bnc_cb.grid(row=0, column=1)
#02
fr_prog.grid(row=2, column=0, padx=4, pady=4, sticky='we')
fr_prog.columnconfigure(index=1, weight=1)
prog_lb.grid(row=0, column=0, padx=4, pady=4, sticky='we')
prog_bar.grid(row=0, column=1, padx=4, pady=4, sticky='we')
#99
fr_status.grid(row=99, column=0, padx=4, pady=4, sticky='sw')
statustxt_lb.grid(row=0, column=0)
status_lb.grid(row=0, column=1)

root.mainloop()