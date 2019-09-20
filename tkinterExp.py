import tkinter as tk
import requests, re, csv
from tkinter.filedialog import asksaveasfile


reName = r'(?<=Name\ \ )[A-Z\ ]+|(?<=Name\ \ .)[A-Z\ ]+'
reGPA = r'(?<=\: )\d\.\d+|(?<=\: )\d(?=<)'
errorText = r'No such student exists in this database or the student has not given the particular semester exam'

def printProgress(labeltext, j, tot):
	labeltext.config(text = str(j)+' out of '+str(tot))

def printLB(labeltext, event):
	textName = event.get(tk.ANCHOR)
	labeltext.config(text = textName)

def info(labeltext, roll, sem):
	
	try:
		rollText = int(roll.get())
		semText = int(sem.get(tk.ANCHOR))
		r = requests.post(url = site, data = {'roll':rollText , 'sem': semText})
		data = r.text
		if not re.search(errorText, data):
			name = re.search(reName, data).group(0)
			GPA = re.findall(reGPA, data)
		labeltext.config(text = name.title()+'\n'+GPA[2])
	except ValueError:
		labeltext.config(text = 'Empty')	
	except:
		labeltext.config(text = 'Student does not exist')	

def save(sroll, eroll, sem):
	
	files = [('All Files', '*.*'),  
			('Python Files', '.py'), 
			('CSV Files', '*.csv')] 
	file = asksaveasfile(defaultextension = ".csv", title = "Select file", filetypes = files)

	if file:
		fieldNames = ['Name', 'SGPA_O', 'SGPA_E', 'YGPA']
		writer = csv.DictWriter(file, fieldnames = fieldNames)
		writer.writeheader()
		srollText = int(sroll.get())
		erollText = int(eroll.get())
		semText = int(sem.get(tk.ANCHOR))
		numroll = erollText - srollText + 1
		j = 0
		for i in range(srollText, erollText + 1):
			r = requests.post(url = site, data = {'roll':i , 'sem': semText})
			data = r.text
			# print(data)
			# print(re.search(errorText, data))
			if not re.search(errorText, data):
				name = re.search(reName, data).group(0)
				GPA = re.findall(reGPA, data)
				# print(name.title())
				# print(GPA)
				writer.writerow({'Name': name.title(), 'SGPA_O': GPA[0], 'SGPA_E': GPA[1], 'YGPA': GPA[2]})
				j+=1
				printProgress(labeltext, j, numroll)
				labeltext.update_idletasks()
		file.close()

site = "http://136.232.2.202:8084/heresult19.aspx"

response = requests.get(site)
# response.raise_for_status()

# print(response)

m = tk.Tk()

m.title('Counting')
# m.configure(bg="red")

tk.Label(m, text = 'Starting Roll no.').grid(row = 0)
e1 = tk.Entry(m)
e1.grid(row = 0, column = 1)

tk.Label(m, text = 'Ending Roll no.').grid(row = 1)
e2 = tk.Entry(m)
e2.grid(row = 1, column = 1)


semLabel = tk.Label(m, text = 'Sem').grid(row = 0, column = 2)
Lb = tk.Listbox(m, height = 4)
Lb.insert(1, '2') 
Lb.insert(2, '4') 
Lb.insert(3, '6') 
Lb.insert(4, '8')
Lb.grid(row = 1, column = 2)
# print(e1.get())
# button = tk.Button(m, text = 'Submit', width = 25, command = printE(e1))
# button.grid(row = 1)
labeltext = tk.Label(m)
labeltext.grid(row = 7, column = 1)



# r = requests.post(url = site, data = {'roll':12617001002 , 'sem': 4})
# data = r.text
# # print(data)
# # print(re.search(errorText, data))
# if not re.search(errorText, data):
# 	name = re.search(reName, data).group(0)
# 	GPA = re.findall(reGPA, data)

# buttonSub = tk.Button(m, text="Submit", command=lambda: info(labeltext, e1, Lb)).grid(row=3, column=0)
buttonSave = tk.Button(m, text="Save", command=lambda: save(e1,e2, Lb)).grid(row = 4, column = 0)

m.mainloop()