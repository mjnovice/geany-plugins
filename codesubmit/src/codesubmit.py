import urllib2
import re#import error exception
from poster.encode import multipart_encode#import error exception
from poster.streaminghttp import register_openers#import error exception
import sys
import BeautifulSoup#import error exception
import gtk
import geany

class CodeSubmit(geany.Plugin):
	window=gtk.Window(type=gtk.WINDOW_TOPLEVEL)
	tools_menu_item= gtk.MenuItem("CodeSubmit")
	user_entry=gtk.Entry(max=0)
	pwd_entry=gtk.Entry(max=0)
	probid_entry=gtk.Entry(max=0)
	language_box=gtk.ComboBoxText()
	language_box.append_text("C")
	language_box.append_text("C++")
	language_box.append_text("BrainFuck")
	language_box.append_text("Python")
	server_box=gtk.ComboBoxText()
	server_box.append_text("SPOJ")
	server_box.append_text("CodeChef")
	submit_button=gtk.Button(label="_Submit!",stock=None,use_underline=True)
	save_button=gtk.Button(label="_Save!",stock=None,use_underline=True)
	conf_path = os.path.join(geany.app.configdir, "plugins","datafile.conf")
	langlist={"11" , "41", "10", "12"}
    __plugin_name__ = "CodeSubmit"
    __plugin_version__ = "1.0"
    __plugin_description__ = "A tool to submit code online SPOJ,Codechef etc."
    __plugin_author__ = "Mayank Jha (mjnovice@gmail.com)"

    def __init__(self):
        self.tools_menu_item.show()
        geany.main_widgets.tools_menu.append(self.menu_item)
        self.menu_item.connect("activate", self.on_hello_item_clicked)
		self.submit_button.connect("clicked",self.on_submit_button_clicked)
		self.save_button.connect("clicked",self.on_save_button_clicked)
		
    def cleanup(self):
        self.menu_item.destroy()

    def on_hello_item_clicked(widget, data,self):
		table = gtk.Table(rows=2, columns=2, homogeneous=False)	
        #creating the language box and the server box
        #geany.dialogs.show_msgbox("Hello World")
		table.attach(gtk.Label("User Name: "), 0, 1, 0, 1);
		table.attach(self.user_entry, 1, 2, 0, 1);
		table.attach(gtk.Label("Password : "), 0, 1, 1, 2);
		table.attach(self.pwd_entry, 1, 2, 1, 2);
		table.attach(gtk.Label("Problem ID: "), 0, 1, 2, 3);
		table.attach(self.probid_entry, 1, 2, 2, 3);
		table.attach(gtk.Label("Servers: "), 0, 1, 3, 4);
	    table.attach(self.server_box, 1, 2, 3, 4);
		table.attach(gtk.Label("Language: "), 0, 1, 4, 5);
		table.attach(self.language_box, 1, 2, 4, 5);
		table.attach(self.submit_button, 0, 1, 5, 6);
		table.attach(sel.save_button, 1, 2, 5, 6);
		#adding the table to the self.window
		window.add(window, table);
	
	
	def on_submit_button_clicked(widget,data,self):
		register_openers()
		username=user_entry.get_text()
		password=pwd_entry.get_text()
		filepath=(geany.document.get_current()).file_name
		probcode=probid_entry.get_text()
		datagen, headers = multipart_encode({'login_user':username,
			'password':password,"subm_file": open(filepath, "rb"),
			'lang':self.langlist[language_box.get_active()],
			'problemcode':probcode})
		url="http://www.spoj.com/submit/complete/"
		request = urllib2.Request(url, datagen, headers)
		if request['error']:
			geany.dialogs.show_msgbox("Problem could not be submitted!")
		#opening url exception
		m = re.search(r'"newSubmissionId" value="(\d+)"/>', urllib2.urlopen(request).read())
		submid=m.group(1)
		submid=str(submid)
		stats="statusres_"+submid
		memory="statusmem_"+submid
		time="statustime_"+submid
		data=urllib2.urlopen("https://www.spoj.com/status/").read()
		if response['error']:
			geany.dialogs.show_msgbox("Server could not be reached!")
		#opening url exception
		soup = BeautifulSoup.BeautifulSoup(data)
		tim=soup.find("td",{"id":time})
		mem=soup.find("td",{"id":memory})
		sta=soup.find("td",{"id":stats})
		final="Submission id: "+submid+"Status: "+str(sta)+"Time: "+str(tim)+"Memory: "+str(mem)
		soup = BeautifulSoup.BeautifulSoup(final)
		gy=''
		for node in soup.findAll('td'):
			gy+=''.join(node.findAll(text=True))
		y=str(gy)
		y=y.replace("google_ad_section_start(weight=ignore) ","")
		y=y.replace("google_ad_section_end","")
		y=y.replace("\n","")
		y=y.replace("  		","")
		y=y.replace("  		    	","")
		geany.msgwindow.msg_add(y)		#prints the result in a message window
		geany.dialogs.show_msgbox(y)	#adds the result to the compiler tab
		
		
	def on_save_button_clicked(widget,data,self):
		tobeadded=self.user_entry.get_text()+" "+self.pwd_entry.get_text()+" "
		tobeadded+=self.probid_entry.get_text()
		tobeadded+=" " 
		f=open(self.conf_path)
		print tobeadded
		print self.language_box.get_active()
		f.close()
		
	def config_load(self):
		
		#method for retrieving data from conf_path file


