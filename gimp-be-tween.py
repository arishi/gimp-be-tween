#!/usr/bin/env python

from gimpfu import *
import gtk
import copy

# (c) 2020 Arishi

class LayerAnimator(gtk.Window):
	def __init__ (self, img, *args):
		super(LayerAnimator, self).__init__()

		self.layerlist = []
		self.img = img

		self.set_title("Layer Animator")
		self.set_size_request(250, 80)
		self.set_position(gtk.WIN_POS_CENTER)

		vbox = gtk.VBox(False, 2)

		table = gtk.Table(1, 2, True)

		frameCount = gtk.Entry()
		self.frameCount = frameCount

		btnMove = gtk.Button("Move")
		btnRender = gtk.Button("Render")

		label = gtk.Label()
		self.numlayers = label

		label.set_text("None")

		table.attach(btnMove, 0, 1, 0, 1)
		table.attach(frameCount, 1, 3, 0, 1)
		table.attach(btnRender, 3, 4, 0, 1)

		vbox.pack_start(label, False, False, 0)
		vbox.pack_end(table, True, True, 0)

		self.add(vbox)

		self.connect("destroy", gtk.main_quit)
		self.show_all()

		btnMove.connect("clicked", self.clickedMove)
		btnRender.connect("clicked", self.clickedRender)

		thisFrame = {}
		thisFrame["layers"] = self.saveLayers(self.img.layers)
		thisFrame["frameCount"] = 0
		self.layerlist.append(thisFrame)

	def clickedMove(self, event):
		frameBox = self.frameCount.get_text()

		if frameBox and frameBox.isdigit():
			thisFrame = {}
			thisFrame["layers"] = self.saveLayers(self.img.layers)
			thisFrame["frameCount"] = int(frameBox)
			self.layerlist.append(thisFrame)
			self.numlayers.set_text(str(len(self.layerlist)))
			print self.frameCount.get_text()

	def saveLayers(self, layers):
		newLayers = []

		for layer in layers:
			thisLayer = {}
			thisLayer["handle"] = layer
			thisLayer["position"] = copy.deepcopy(layer.offsets)
			newLayers.append(thisLayer)

		return newLayers

	def clickedRender(self, event):
		print len(self.layerlist)

		chooser = gtk.FileChooserDialog(
			title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,
			buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK)
		)
		response = chooser.run()
		if response != gtk.RESPONSE_OK:
			chooser.destroy()
			return

		baseFileName = chooser.get_filename()
		baseFileNameSplit = baseFileName.split('.')
		chooser.destroy()

		frameNumber = 0
		for walkFrames in range(len(self.layerlist) - 1):
			thisFrame = self.layerlist[walkFrames]

			difflayers = []
			nextFrame = self.layerlist[walkFrames + 1]
			layers = thisFrame["layers"]
			nextLayers = nextFrame["layers"]
			for walkLayers in range(len(layers)):
				thisLayer = layers[walkLayers]
				nextLayer = nextLayers[walkLayers]

				if (thisLayer["position"][0] != nextLayer["position"][0]) or (thisLayer["position"][1] != nextLayer["position"][1]):
#					print "Layer ID moved " + thisLayer["handle"].name
					difflayers.append(walkLayers)

#			print "Found layers different: " + repr(difflayers)

			frameCount = nextFrame["frameCount"]
			sx = {}
			sy = {}
			dx = {}
			dy = {}

			for walkLayers in difflayers:
				thisLayer = layers[walkLayers]
				nextLayer = nextLayers[walkLayers]

				sx[walkLayers] = thisLayer["position"][0]
				sy[walkLayers] = thisLayer["position"][1]
				dx[walkLayers] = (nextLayer["position"][0] - sx[walkLayers]) / (frameCount - 1)
				dy[walkLayers] = (nextLayer["position"][1] - sy[walkLayers]) / (frameCount - 1)

#				print "Layer init: " + thisLayer["handle"].name + ", " + str(sx[walkLayers]) + "," + str(sy[walkLayers]) + " - " + str(dx[walkLayers]) + "," + str(dy[walkLayers])

			for walkFrames in range(frameCount):
				frameNumber = frameNumber + 1

				for walkLayers in difflayers:
					thisLayer = layers[walkLayers]
					nextLayer = nextLayers[walkLayers]

#					print "Layer: " + thisLayer["handle"].name + ", " + str(walkFrames) + " " + str(sx[walkLayers]) + "," + str(sy[walkLayers])
					thisLayer["handle"].set_offsets(sx[walkLayers], sy[walkLayers])

					sx[walkLayers] = sx[walkLayers] + dx[walkLayers]
					sy[walkLayers] = sy[walkLayers] + dy[walkLayers]

				fileName = baseFileNameSplit[0] + str(frameNumber).zfill(3) + '.' + baseFileNameSplit[1]
				newLayer = pdb.gimp_layer_new_from_visible(self.img, self.img, "layer_animator_tmp")
				pdb.file_png_save_defaults(self.img, newLayer, fileName, fileName)
				gimp.delete(newLayer)

def layer_animator (img, drw):
	LayerAnimator(img)
	gtk.main()

register(
		 "layer_animator",
		 "Basic tweening for one or more layers",
		 "Basic tweening for one or more layers",
		 "Arishi",
		 "Arishi",
		 "2020",
		 "<Image>/Layer/GIMP-be-tween",
		 "*",
		 [],
		 [],
		 layer_animator)

main()
