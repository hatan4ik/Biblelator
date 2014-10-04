#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# EditWindow.py
#   Last modified: 2014-10-04 (also update ProgVersion below)
#
# xxx program for Biblelator Bible display/editing
#
# Copyright (C) 2013-2014 Robert Hunt
# Author: Robert Hunt <Freely.Given.org@gmail.com>
# License: See gpl-3.0.txt
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
xxx to allow editing of USFM Bibles using Python3 and Tkinter.
"""

ShortProgName = "EditWindow"
ProgName = "Biblelator Edit Window"
ProgVersion = "0.14"
ProgNameVersion = "{} v{}".format( ProgName, ProgVersion )

debuggingThisModule = True


import sys, os.path, configparser, logging
from gettext import gettext as _
import multiprocessing

from tkinter import Toplevel, Text, Menu #, StringVar, messagebox
from tkinter import NORMAL, DISABLED, LEFT, RIGHT, BOTH, YES, END
from tkinter.ttk import Style, Frame #, Button, Combobox

# BibleOrgSys imports
sourceFolder = "../BibleOrgSys/"
sys.path.append( sourceFolder )
import Globals
import USFMBible #, USFMStylesheets

# Biblelator imports
from BiblelatorGlobals import MINIMUM_RESOURCE_X_SIZE, MINIMUM_RESOURCE_Y_SIZE, editModeNormal, editModeUSFM
from ResourceWindows import ResourceFrame
from BibleResourceWindows import InternalBibleResourceFrame


def t( messageString ):
    """
    Prepends the module name to a error or warning message string
        if we are in debug mode.
    Returns the new string.
    """
    try: nameBit, errorBit = messageString.split( ': ', 1 )
    except ValueError: nameBit, errorBit = '', messageString
    if Globals.debugFlag or debuggingThisModule:
        nameBit = '{}{}{}: '.format( ShortProgName, '.' if nameBit else '', nameBit )
    return '{}{}'.format( nameBit, _(errorBit) )



class TextEditFrame( ResourceFrame ):
    pass



class USFMEditFrame( InternalBibleResourceFrame ):
    def __init__( self, parent, master, modulePath, editMode ):
        #if Globals.debugFlag: print( "USFMEditFrame.__init__( {}, {}, {}, {} )".format( parent, master, modulePath, editMode ) )
        self.USFMEditFrameParent, self.USFMEditMaster, self.editModulePath = parent, master, modulePath
        InternalBibleResourceFrame.__init__( self, parent, master, modulePath )
        if self.InternalBible is not None:
            self.textBox['background'] = "white"
            self.textBox['selectbackground'] = "red"
            self.textBox['highlightbackground'] = "orange"
            self.textBox['inactiveselectbackground'] = "green"
            self.editMode = editMode
            #self.createUSFMEditFrameWidgets()
            self.USFMEditFrameParent.title( "{} ({}) Editable".format( self.InternalBible.name, self.editMode ) )
        else: self.editMode = None
        #self.minimumXSize, self.minimumYSize = MINIMUM_RESOURCE_X_SIZE, MINIMUM_RESOURCE_Y_SIZE
        self.createMenuBar()
        self.createContextMenu()
    # end of USFMEditFrame.__init__


    def notWrittenYet( self ):
        messagebox.showerror( _("Not implemented"), _("Not yet available, sorry") )
    # end of Application.notWrittenYet


    def doHelp( self ):
        from Help import HelpBox
        hb = HelpBox( self.USFMEditFrameParent, ProgName, ProgNameVersion )
    # end of Application.doHelp


    def doAbout( self ):
        from About import AboutBox
        ab = AboutBox( self.USFMEditFrameParent, ProgName, ProgNameVersion )
    # end of Application.doAbout


    def createMenuBar( self ):
        self.menubar = Menu( self.USFMEditFrameParent )
        #self['menu'] = self.menubar
        self.USFMEditFrameParent.config( menu=self.menubar ) # alternative

        menuFile = Menu( self.menubar, tearoff=False )
        self.menubar.add_cascade( menu=menuFile, label='File', underline=0 )
        menuFile.add_command( label='New...', underline=0, command=self.notWrittenYet )
        menuFile.add_command( label='Open...', underline=0, command=self.notWrittenYet )
        menuFile.add_separator()
        submenuFileImport = Menu( menuFile )
        submenuFileImport.add_command( label='USX', underline=0, command=self.notWrittenYet )
        menuFile.add_cascade( label='Import', underline=0, menu=submenuFileImport )
        submenuFileExport = Menu( menuFile )
        submenuFileExport.add_command( label='USX', underline=0, command=self.notWrittenYet )
        submenuFileExport.add_command( label='HTML', underline=0, command=self.notWrittenYet )
        menuFile.add_cascade( label='Export', underline=0, menu=submenuFileExport )
        menuFile.add_separator()
        menuFile.add_command( label='Close', underline=0, command=self.closeEditor ) # close edit window

        menuEdit = Menu( self.menubar )
        self.menubar.add_cascade( menu=menuEdit, label='Edit', underline=0 )
        menuEdit.add_command( label='Undo...', underline=0, command=self.notWrittenYet )
        menuEdit.add_command( label='Redo...', underline=0, command=self.notWrittenYet )
        menuEdit.add_separator()
        menuEdit.add_command( label='Cut...', underline=2, command=self.notWrittenYet )
        menuEdit.add_command( label='Copy...', underline=0, command=self.notWrittenYet )
        menuEdit.add_command( label='Paste...', underline=0, command=self.notWrittenYet )
        menuEdit.add_separator()
        menuEdit.add_command( label='Find...', underline=0, command=self.notWrittenYet )
        menuEdit.add_command( label='Replace...', underline=0, command=self.notWrittenYet )

        menuGoto = Menu( self.menubar )
        self.menubar.add_cascade( menu=menuGoto, label='Goto', underline=0 )
        menuGoto.add_command( label='Previous book', underline=0, command=self.notWrittenYet )
        menuGoto.add_command( label='Next book', underline=0, command=self.notWrittenYet )
        menuGoto.add_command( label='Previous chapter', underline=0, command=self.notWrittenYet )
        menuGoto.add_command( label='Next chapter', underline=0, command=self.notWrittenYet )
        menuGoto.add_command( label='Previous verse', underline=0, command=self.notWrittenYet )
        menuGoto.add_command( label='Next verse', underline=0, command=self.notWrittenYet )
        menuGoto.add_separator()
        menuGoto.add_command( label='Forward', underline=0, command=self.notWrittenYet )
        menuGoto.add_command( label='Backward', underline=0, command=self.notWrittenYet )
        menuGoto.add_separator()
        menuGoto.add_command( label='Previous list item', underline=0, command=self.notWrittenYet )
        menuGoto.add_command( label='Next list item', underline=0, command=self.notWrittenYet )
        menuGoto.add_separator()
        menuGoto.add_command( label='Book', underline=0, command=self.notWrittenYet )

        menuView = Menu( self.menubar )
        self.menubar.add_cascade( menu=menuView, label='View', underline=0 )
        menuView.add_command( label='Whole chapter', underline=6, command=self.notWrittenYet )
        menuView.add_command( label='Whole book', underline=6, command=self.notWrittenYet )
        menuView.add_command( label='Single verse', underline=7, command=self.notWrittenYet )

        menuTools = Menu( self.menubar, tearoff=False )
        self.menubar.add_cascade( menu=menuTools, label='Tools', underline=0 )
        menuTools.add_command( label='Options...', underline=0, command=self.notWrittenYet )

        menuWindow = Menu( self.menubar, tearoff=False )
        self.menubar.add_cascade( menu=menuWindow, label='Window', underline=0 )
        menuWindow.add_command( label='Bring in', underline=0, command=self.notWrittenYet )

        menuHelp = Menu( self.menubar, name='help', tearoff=False )
        self.menubar.add_cascade( menu=menuHelp, label='Help', underline=0 )
        menuHelp.add_command( label='Help...', underline=0, command=self.doHelp )
        menuHelp.add_separator()
        menuHelp.add_command( label='About...', underline=0, command=self.doAbout )

        #filename = filedialog.askopenfilename()
        #filename = filedialog.asksaveasfilename()
        #dirname = filedialog.askdirectory()
        #colorchooser.askcolor(initialcolor='#ff0000')
        #messagebox.showinfo(message='Have a good day')
        #messagebox.askyesno( message='Are you sure you want to install SuperVirus?' icon='question' title='Install' )
    # end of ResourceWindow.createMenuBar


    def createContextMenu( self ):
        """
        """
        self.contextMenu = Menu( self, tearoff=0 )
        self.contextMenu.add_command( label="Cut", underline=2, command=self.notWrittenYet )
        self.contextMenu.add_command( label="Copy", underline=0, command=self.notWrittenYet )
        self.contextMenu.add_command( label="Paste", underline=0, command=self.notWrittenYet )
        self.contextMenu.add_separator()
        self.contextMenu.add_command( label="Close", underline=1, command=self.closeEditor )

        self.bind( "<Button-3>", self.showContextMenu ) # right-click
        #self.pack()
    # end of ResourceWindow.createContextMenu


    def showContextMenu(self, e):
        self.contextMenu.post( e.x_root, e.y_root )
    # end of ResourceWindow.showContextMenu


    #def createToolBar( self ):
        #toolbar = Frame( self, cursor='hand2', relief=SUNKEN ) # bd=2
        #toolbar.pack( side=BOTTOM, fill=X )
        #Button( toolbar, text='Halt',  command=self.quit ).pack( side=RIGHT )
        #Button( toolbar, text='Hide Resources', command=self.hideResources ).pack(side=LEFT )
        #Button( toolbar, text='Hide All', command=self.hideAll ).pack( side=LEFT )
        #Button( toolbar, text='Show All', command=self.showAll ).pack( side=LEFT )
        #Button( toolbar, text='Bring All', command=self.bringAll ).pack( side=LEFT )
    ## end of ResourceWindow.createToolBar


    def xxcreateUSFMEditFrameWidgets( self ):
        pass
        #self.label1 = Label( self, text=self.moduleAbbreviation )
        #self.label1.pack()

        #self.hi_there = Button( self )
        #self.hi_there['text'] = "Refresh"
        #self.hi_there["command"] = self.update
        #self.hi_there.pack(side="top")

        #self.bStyle = Style( self )
        #self.bStyle.configure( "Red.TButton", foreground="red", background="white" )
        #self.bStyle.map("Red.TButton",
                        #foreground=[('pressed', 'red'), ('active', 'blue')],
                        #background=[('pressed', '!disabled', 'black'), ('active', 'white')] )

        #self.textBox = ScrolledText( self, width=40, height=10 )
        #self.textBox['wrap'] = 'word'
        #verseText = SwordResources.getBCV( self.parent.bcv )
        #print( "vt", verseText )
        #self.textBox.insert( '1.0', verseText )
        #self.textBox.pack()
        #self.textBox['state'] = DISABLED # Don't allow editing

        #self.QUIT = Button( self, text="Close", style="Red.TButton", command=self.destroy)
        #self.QUIT.pack( side="bottom" )

        #Sizegrip( self ).grid( column=999, row=999, sticky=(S,E) )
    # end of USFMEditFrame.createUSFMEditFrameWidgets


    def update( self ): # Leaves in disabled state
        def displayVerse( firstFlag, BnameCV, verseDataList, currentVerse=False ):
            #print( "InternalBibleResourceFrame.displayVerse", firstFlag, BnameCV, [], currentVerse )
            haveC = None
            lastCharWasSpace = haveTextFlag = not firstFlag
            if verseDataList is None:
                print( "  ", BnameCV, "has no data" )
                self.textBox.insert( END, '--' )
            else:
                for entry in verseDataList:
                    marker, cleanText = entry.getMarker(), entry.getCleanText()
                    #print( "  ", haveTextFlag, marker, repr(cleanText) )
                    if marker.startswith( '¬' ): pass # Ignore these closing markers
                    elif marker == 'c': # Don't want to display this (original) c marker
                        #if not firstFlag: haveC = cleanText
                        #else: print( "   Ignore C={}".format( cleanText ) )
                        pass
                    elif marker == 'c#': # Might want to display this (added) c marker
                        if cleanText != BnameCV[0]:
                            if not lastCharWasSpace: self.textBox.insert( END, ' ', 'v-' )
                            self.textBox.insert( END, cleanText, 'c#' )
                            lastCharWasSpace = False
                    elif marker == 's1':
                        self.textBox.insert( END, ('\n' if haveTextFlag else '')+cleanText, marker )
                        haveTextFlag = True
                    elif marker == 'r':
                        self.textBox.insert( END, ('\n' if haveTextFlag else '')+cleanText, marker )
                        haveTextFlag = True
                    elif marker == 'p':
                        self.textBox.insert ( END, '\n  ' if haveTextFlag else '  ' )
                        lastCharWasSpace = True
                        if cleanText:
                            self.textBox.insert( END, cleanText, '*v~' if currentVerse else 'v~' )
                            lastCharWasSpace = False
                        haveTextFlag = True
                    elif marker == 'q1':
                        self.textBox.insert ( END, '\n  ' if haveTextFlag else '  ' )
                        lastCharWasSpace = True
                        if cleanText:
                            self.textBox.insert( END, cleanText, '*q1' if currentVerse else 'q1' )
                            lastCharWasSpace = False
                        haveTextFlag = True
                    elif marker == 'm': pass
                    elif marker == 'v':
                        if haveTextFlag:
                            self.textBox.insert( END, ' ', 'v-' )
                        self.textBox.insert( END, cleanText, marker )
                        self.textBox.insert( END, ' ', 'v+' )
                        lastCharWasSpace = haveTextFlag = True
                    elif marker in ('v~','p~'):
                        self.textBox.insert( END, cleanText, '*v~' if currentVerse else marker )
                        haveTextFlag = True
                    else:
                        logging.critical( t("USFMEditFrame.displayVerse: Unknown marker {} {}").format( marker, cleanText ) )
        # end of displayVerse

        if Globals.debugFlag: print( "USFMEditFrame.update()" )
        bibleData = self.getBibleData()
        self.clearText()
        if bibleData:
            verseData, previousVerse, nextVerses = self.getBibleData()
            if previousVerse:
                BnameCV, previousVerseData = previousVerse
                displayVerse( True, BnameCV, previousVerseData )
            displayVerse( not previousVerse, self.myMaster.BnameCV, verseData, currentVerse=True )
            for BnameCV,nextVerseData in nextVerses:
                displayVerse( False, BnameCV, nextVerseData )
        self.textBox['state'] = NORMAL # Allow editing
    # end of USFMEditFrame.update

    def closeEditor( self ):
        """
        """
        self.destroy()
    # end of USFMEditFrame.closeEditor
# end of USFMEditFrame class



class ESFMEditFrame( USFMEditFrame ):
    pass



def demo():
    """
    Demo program to handle command line parameters and then run what they want.
    """
    from tkinter import Tk
    if Globals.verbosityLevel > 0: print( ProgNameVersion )
    #if Globals.verbosityLevel > 1: print( "  Available CPU count =", multiprocessing.cpu_count() )

    if Globals.debugFlag: print( t("Running demo...") )
    #Globals.debugFlag = True

    tkRootWindow = Tk()
    tkRootWindow.title( ProgNameVersion )
    #settings = ApplicationSettings( 'BiblelatorData/', 'BiblelatorSettings/', ProgName )
    #settings.load()

    #application = Application( parent=tkRootWindow, settings=settings )
    # Calls to the window manager class (wm in Tk)
    #application.master.title( ProgNameVersion )
    #application.master.minsize( application.minimumXSize, application.minimumYSize )

    # Start the program running
    tkRootWindow.mainloop()
# end of EditWindow.demo


if __name__ == '__main__':
    import multiprocessing

    # Configure basic set-up
    parser = Globals.setup( ProgName, ProgVersion )
    Globals.addStandardOptionsAndProcess( parser )

    multiprocessing.freeze_support() # Multiprocessing support for frozen Windows executables


    if 1 and Globals.debugFlag and debuggingThisModule:
        from tkinter import TclVersion, TkVersion
        from tkinter import tix
        print( "TclVersion is", TclVersion )
        print( "TkVersion is", TkVersion )
        print( "tix TclVersion is", tix.TclVersion )
        print( "tix TkVersion is", tix.TkVersion )

    demo()

    Globals.closedown( ProgName, ProgVersion )
# end of EditWindow.py