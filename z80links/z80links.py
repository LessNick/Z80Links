import os
import os.path
import sublime
import sublime_plugin
import re
import json

global labelsFileName, debugMode
labelsFileName = "labelsList.json"
debugMode = False

def debugLog(msg):
	if debugMode:
		print (msg)

def findProjectPath():

	projectPath = ""
	views = sublime.active_window().views()

	fileName = views[0].file_name()
	filePathA = fileName.split("\\")
	del filePathA[-1]
	fileDir = "\\".join(filePathA)
	
	searchDir = fileDir
	search = True
	found = False

	while search:
		# search project path
		for file in os.listdir(searchDir):
			if file.endswith(".sublime-project"):
				search = False
				found = True
		
		if search:
			searchDirA = searchDir.split("\\")

			if len(searchDirA) > 1:
				del searchDirA[-1]
				searchDir = "\\".join(searchDirA)
			else:
				search = False

	if found:
		projectPath = searchDir
		debugLog("Project found =" + projectPath)
	else:
		msg = "Project NOT found!"
		debugLog (msg);
		sublime.message_dialog(msg)

	return projectPath

class Z80Links(sublime_plugin.EventListener):
	def __init__(self):	
		self.labelsList = {}
		self.projectPath = findProjectPath()

	def on_load(self, view):
		self.view = view
		if self.projectPath == "":
			self.projectPath = findProjectPath()
			debugLog ("projectPath='" + self.projectPath + "'")

	def on_post_save(self, view):

		if view.file_name().endswith(".asm"):
			debugLog ("Z80 Links: Document save!")
			filename = view.file_name()
			savefn = filename.replace(self.projectPath + '\\', '')
			savefn = savefn.replace('\\', '/')

			debugLog("Doing action for: " + savefn)

			if self.projectPath != "":
				lfn = self.projectPath + '/' + labelsFileName

				if os.path.isfile(lfn):
					with open(lfn) as json_file:
						oldLabelsList = json.load(json_file)
						
						debugLog ("Labels loaded!")
						
						self.labelsList = {}
						for key in oldLabelsList:
							value = oldLabelsList[key]
							if value[0] != savefn:
								self.labelsList[key] = value

						savetext = view.substr(sublime.Region(0, view.size()))

						lines = savetext.split('\n')
						count = 0
						for l in lines:
							if re.match(r'^\w+', l):
								r = re.search(r'^(\w+)', l)
								label = r.group(0)
								fn = filename.replace(self.projectPath + '\\', '')
								fn = fn.replace('\\', '/')
								self.labelsList[label] = [fn, count]

							count = count + 1

						j = json.dumps(self.labelsList)
						f = open(self.projectPath + '/' + labelsFileName, 'w')
						f.write(j)
						f.close()

						debugLog ("Labels updated!")

				else:
					debugLog ("Labels not found!")

			else:
				debugLog ("Project not found!")

class Z80RebuildLinksCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		debugLog("Z80 Rebuild links")

		projectPath = findProjectPath()
		debugLog("Project found =" + projectPath)
		labelsList = {}

		result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(projectPath) for f in filenames if os.path.splitext(f)[1] == '.asm']

		debugLog("files in project=" + str(result))

		for filename in result:
			lines = open(filename).readlines()
			count = 0
			for l in lines:
				if re.match(r'^\w+', l):
					r = re.search(r'^(\w+)', l)
					label = r.group(0)
					fn = filename.replace(projectPath + '\\', '')
					fn = fn.replace('\\', '/')
					labelsList[label] = [fn, count]

				count = count + 1

		j = json.dumps(labelsList)
		f = open(projectPath + '/' + labelsFileName, 'w')
		f.write(j)
		f.close()

		sublime.message_dialog("Cached labels: " + str(len(labelsList)) + "\nScanned files: " + str(len(result)))

		debugLog ("Labels parsed!")



class DragSelectCallbackCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
		self.projectPath = ""

		self.labelsList = {}
		self.projectPath = findProjectPath()

		if self.projectPath != "":
			lfn = self.projectPath + '/' + labelsFileName

			if os.path.isfile(lfn):
				with open(lfn) as json_file:
					self.labelsList = json.load(json_file)
					debugLog ("Labels loaded!")
			else:
				debugLog ("Labels not found!")
		else:
			debugLog ("Project not found!")

	def run_(self, args):
		
		self.view.run_command("drag_select", args)

		try:

			w = sublime.active_window()
			v = w.views()

			debugLog("projectPath=" + self.projectPath)

			sel = self.view.sel()
			region1 = sel[0]
			selectionText = self.view.substr(region1)

			debugLog("selected=" + selectionText)

			if selectionText in self.labelsList.keys():
				filename = self.labelsList[selectionText][0]
				debugLog ("filename=" + filename)
				line = self.labelsList[selectionText][1]
				debugLog ("line="+str(line))

				w.open_file(self.projectPath + '/' + filename)

				w.active_view().run_command("goto_line", {"line": line} )
			else:
				msg = selectionText + " not found!"
				debugLog (msg);
				sublime.message_dialog(msg)

		except Exception as e:
			debugLog(e)

