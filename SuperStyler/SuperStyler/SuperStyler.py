from aqt import mw
from aqt.qt import *
# my stuff
import selector
import utils

def ssLaunch():
    ss = SelectStyle(mw)

# create a new menu item
action = QAction("Super Styler", mw)
# set it to call ssLaunch when it's clicked
mw.connect(action, SIGNAL("triggered()"), ssLaunch)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


class SelectStyle(QDialog):

    def __init__(self, mw):
        # Form setup
        QDialog.__init__(self, mw)
        self.mw = mw
        self.form = selector.Ui_Dialog()
        self.form.setupUi(self)
        self.form.btnStart.setDisabled(True)

        # Add events for comboBox selection
        self.connect(self.form.comboModelSelect, SIGNAL('currentIndexChanged(QString)'), self.onModelSelect)
        self.connect(self.form.comboTmplSelect, SIGNAL('currentIndexChanged(QString)'), self.onTmplSelect)
        # Add event for Start button
        self.connect(self.form.btnStart, SIGNAL('clicked()'), self.onBtnStart)
                                
        # Make a combo box of all model names in the collection
        model_names = [model['name'] for model in mw.col.models.all()]
        self.form.comboModelSelect.addItems(model_names)

        # Select first item as a default
        self.form.comboModelSelect.setCurrentIndex(0)

        # Start UI (show it)
        self.exec_()


    def onModelSelect(self, model_name):
        print "On Model Select", model_name
        self.current_model = mw.col.models.byName(model_name)
        # Make a combo box of all templates (by name) in the chosen model
        tmpl_names = [tmpl['name'] for tmpl in self.current_model['tmpls']]
        self.form.comboTmplSelect.clear()
        self.form.comboTmplSelect.addItems(tmpl_names)

        # Select first item as a default
        self.form.comboTmplSelect.setCurrentIndex(0)
        
        # The first option will be selected by default, so enable the start button
        self.form.btnStart.setEnabled(True)
        

    def onTmplSelect(self, tmpl_name):
        print "On TMPL Select", tmpl_name
        tmpls = self.current_model['tmpls']
        for tmpl in tmpls:
            if tmpl['name'] == tmpl_name:
                self.current_tmpl = tmpl
                break

    # Start was clicked! We now need to do six things:
    # 1 - Grab the template and CSS data 
    # 2 - Start a small web server to serve that data
    # 3 - Create a new template to mess around with
    # 4 - Inject our magic javascript into the new template with our web server's
    #     IP address
    # 5 - Create a cram deck with that new template.
    # 6 - Sync the deck so it's available everywhere
    
    def onBtnStart(self):
        print "On Btn STart"       
        css = self.current_model['css']
        tmpl_q = self.current_tmpl['qfmt']
        tmpl_a = self.current_tmpl['afmt']
