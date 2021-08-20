#!/usr/bin/env python
# -*- coding: utf-8 -*-

import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys
from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *
try:
    from python_qt_binding.QtWidgets import *
except ImportError:
    pass
import rviz

class MyViz( QWidget ):
    # 생성자를 통해 frame, button 등의 레이아웃을 추가한다.
    def __init__(self):
        QWidget.__init__(self)
        self.frame = rviz.VisualizationFrame()
        self.frame.setSplashPath( "" )
        self.frame.initialize()
        # rviz의 기본 프레임을 렌더링 창만 표기하도록 함

        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, "gridmap.rviz" )
        self.frame.load( config )
        # .rviz 파일을 읽어 환경으로 구성함
        
        self.setWindowTitle( config.mapGetChild( "Title" ).getValue() )

        self.frame.setMenuBar( None )
        self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( False )

        self.manager = self.frame.getManager()

        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 1 )
        
        layout = QVBoxLayout()
        layout.addWidget( self.frame )
        
        h_layout = QHBoxLayout()

        left_button = QPushButton( "LifeSaving" )
        left_button.clicked.connect( self.onLeftButtonClick )
        h_layout.addWidget( left_button )
        
        center_button = QPushButton( "Fire" )
        center_button.clicked.connect( self.onCenterButtonClick )
        h_layout.addWidget( center_button )

        right_button = QPushButton( "Path" )
        right_button.clicked.connect( self.onRightButtonClick )
        h_layout.addWidget( right_button )

        last_button = QPushButton( "ALL" )
        last_button.clicked.connect( self.onLastButtonClick )
        h_layout.addWidget( last_button )
        
        layout.addLayout( h_layout )
        
        self.setLayout( layout )

    def onLeftButtonClick( self ):
        if self.grid_display != None:
            self.grid_display.subProp( "Marker Topic" ).setValue("/group_localization")

        
    def onCenterButtonClick( self ):
        if self.grid_display != None:
            self.grid_display.subProp( "Marker Topic" ).setValue("/fire")

    def onRightButtonClick( self ):
        if self.grid_display != None:
            #self.grid_display.subProp( "Marker Topic" ).setValue("/planning_vis/trajectory/array")
            self.grid_display.subProp( "Marker Topic" ).setValue("/drone/position")
    def onLastButtonClick( self ):
        if self.grid_display != None:
            self.grid_display.subProp( "Marker Topic" ).setValue("/all")

    def switchToView( self, view_name ):
        view_man = self.manager.getViewManager()
        for i in range( view_man.getNumViews() ):
            if view_man.getViewAt( i ).getName() == view_name:
                view_man.setCurrentFrom( view_man.getViewAt( i ))
                return
        print( "Did not find view named %s." % view_name )

if __name__ == '__main__':
    app = QApplication( sys.argv )

    myviz = MyViz()
    myviz.resize( 500, 500 )
    myviz.show()

    app.exec_()
