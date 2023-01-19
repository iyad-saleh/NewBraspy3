from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext # 2
from multiTelnetDic import autoTelnet ,create_threads
import threading
from mytools import get_credentials
from tkinter import messagebox as mBox
pattern= re.compile(r"([a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4})")
header = ['BRAS-IP', 'BRAS-Name','Search Result']
brasIp =open("Router.txt").read().split("\n") 
smallfont =  ("verdana",10,'bold')
midifont =  ("verdana",13,'bold')
bigfont =  ('Courier', 18, 'bold')

'''#result{
			"HOST":10.100.?.?,
			"bras":"BrasName",
			"MAC":mac,
			"UserNotOnline":"No online user",
			"Final_output":BigData,
			"MacNotOnline":"No online mac",
			"Fault":excp}
'''
result=[]
	

def main(root):
	def _msgBoxinfo(tit,text):
		mBox.showinfo(tit,text)

	def OnDoubleClick( event):
		x=table.item(table.selection())['values'][0]
		scr.delete('1.0', END)
		try:
			# print(result)
			for oneDic in result:

				if oneDic["HOST"]== x:

					if "bras" in oneDic:
						scr.insert(INSERT, oneDic["bras"]+"  "+oneDic["HOST"]+"\n")
					else:
						scr.insert(INSERT, oneDic["HOST"]) 
					if "UserNotOnline" in oneDic:
						scr.insert(INSERT, oneDic["UserNotOnline"] )
					if "MacNotOnline" in oneDic:
						scr.insert(INSERT, oneDic["MacNotOnline"] )	
					if "Final_output" in oneDic:
						scr.insert(INSERT, oneDic["Final_output"] )
					if "Fault" in oneDic:
						scr.insert(INSERT, oneDic["Fault"] )
					break		
		except Exception as e:
			pass
		
	def delete():
		try:
			selected_item = table.selection()[0] ## get selected item
			if selected_item :   
				table.delete(selected_item)
		except Exception as e:
			pass
		

	def start_new_thread(orginal,*arg):
		thread = threading.Thread(target=orginal,args=(*arg,))
		thread.start()	

	# def Refresh_List(newList):
		# print(table.item(table.selection())['text'])
		

	def Refresh_List():

		for item in table.get_children():
			table.detach(item)
		for item in brasIp:
			table.insert('', 'end', values=item, tags=('items',))	

	def clickMe():
		scr.delete('1.0', END)
		target=usertarget.get()
		if not target:
			_msgBoxinfo("wait","First of all Enter your target!!")
			return
		action.config(background='orange red')	#'green yellow'
		ipBras=[]
		for x in table.get_children():
			ipBras.append(table.item(x)['values'][0])
		for item in table.get_children():# delete old result from tree
			table.detach(item)
		for item in ipBras:  # create new tree 
			table.insert('', 'end', values=item, tags=('items',))	

		Username , Password = get_credentials()
		if   re.search(pattern,target):
			cmd_level=2#serach for mac 
		else :
			cmd_level=1	# search for user account
		global result
		result.clear()
		result =create_threads(Username , Password, target, cmd_level, ipBras)#create_threads(Username , Password, target, cmd_level, ipBras):
		for item in table.get_children():# delete old result from tree
			table.detach(item)
		for oneDic in 	result:# create new tree  with new result
			# print(oneDic)
			try:
				if "UserNotOnline" in oneDic:
					oneList=[oneDic["HOST"],oneDic["bras"],oneDic["UserNotOnline"]]
				elif "MAC"  in oneDic:	
					oneList=[oneDic["HOST"],oneDic["bras"],oneDic["MAC"]]
				elif "Fault" in oneDic:
					oneList=[oneDic["HOST"],"Sorry",oneDic["Fault"]]
				elif "MacNotOnline"	in oneDic:
					oneList=[oneDic["HOST"],oneDic["bras"],oneDic["MacNotOnline"]]
				elif "Final_output" in oneDic and "MAC"  not in oneDic:
					oneList=[oneDic["HOST"],oneDic["bras"],target]
					scr.delete('1.0', END)
					scr.insert(INSERT, oneDic["Final_output"] )	
				table.insert('', 'end', values=oneList, tags=('items',))
			except Exception as e:
				print(e) 	
		action.config(background='green yellow')	#'green yellow'	


	frame = ttk.Frame(root)
	frame.pack( expand=YES, fill=BOTH)
	leftFrame=ttk.Frame(frame)
	leftFrame.pack(side="left", expand=NO, fill=Y)
	rightFrame=ttk.Frame(frame)
	rightFrame.pack(side="top", expand=YES, fill=BOTH)
	
	table = ttk.Treeview(leftFrame, columns=header, show="headings",height=20)
	table.column('BRAS-IP',minwidth=0,width=100, stretch=NO)
	table.column('BRAS-Name',minwidth=0,width=200, stretch=NO) 
	table.column('Search Result',minwidth=0,width=150, stretch=NO) 
	table.pack(side="top",padx=5,anchor=N+W, fill=Y)
	table.bind("<Double-1>", OnDoubleClick)
	for col in header:
		table.heading(col, text=col.title())
	for item in brasIp:
		table.insert('', 'end', values=item, tags=('items',))

	button_del = Button(leftFrame, text="del-Item", command=delete)
	button_del.pack(side="left",padx=5,anchor=N+W)
	button_ed = Button(leftFrame, text="Refresh-List", command=Refresh_List)
	button_ed.pack(side="left",padx=5,anchor=N+W)

	usertarget =StringVar()
	Label(rightFrame,text="Enter User Account or MAC Address:",font=midifont).grid(row=0, column=0, sticky='W')
	userEntered=Entry(rightFrame, bd=5,relief= RIDGE,font=smallfont,textvariable=usertarget)
	userEntered.grid(row=0,column=1,sticky="W",columnspan=1)
	userEntered.focus() # Place cursor into target Entry
	
	def paste(event_obj):
		try:
			userEntered.delete(0, END)
			text2paste=userEntered.selection_get(selection='CLIPBOARD')
			userEntered.insert('insert',text2paste)
			userEntered.focus()
		except Exception as e:
			pass
		

	def PressRetutn(event_obj):
		start_new_thread(clickMe)

	userEntered.bind("<Button-3>",paste)
	userEntered.bind('<Return>',PressRetutn )

	action = Button(rightFrame, text="Start Search",width=20,background='green yellow', command=lambda  fun=clickMe:start_new_thread(fun)) # 7
	action.grid(column=2, row=0,padx=5,sticky='E')
	separator = Frame(frame,height=2, bd=3, relief=SUNKEN)
	separator.pack(side="top", expand=YES, fill=X,pady=3)

	ResultSearch=LabelFrame(frame, relief="raise",text="Result",font=midifont)	
	ResultSearch.pack(side="right", expand=YES, fill=BOTH)
	scrolW = 73 # 4
	scrolH = 33 # 5
	scr = scrolledtext.ScrolledText(ResultSearch, width=scrolW, height=scrolH, wrap=WORD,font=smallfont) # 6
	scr.grid(column=0, row=2,padx=5,columnspan=4)

	root.mainloop()

if __name__ == '__main__':
	root = Tk()
	root.title('Search Bras')

	root.iconbitmap(r'pyc.ico')
	main(root)
