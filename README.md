# gimp-be-tween
A very basic attempt at providing tweening functionality for GIMP

We wanted to make some simple animations for a slide deck recently, but wanted to do it based on some layered images we had in GIMP. There didn't seem to be anything providing some simple (linear) tweening capabilities that would generate a series of frames, so here's our first go at making something for it.

This isn't perfect, but it kinda works. Kinda.

You can install it by dropping the Python script in to your GIMP plugins folder. On a Linux system running GIMP 2.10, you can put it in a folder such as ~/.config/GIMP/2.10/plug-ins and then (re)start GIMP to try it out.

If you select the "GIMP-be-tween" option from the Layers menu, you'll get a popup window with a text box in the middle and a "Move" and "Render" button. Simply enter the number of frames to tween through and then shift one or more of your layers around. Click the "Move" button to register the movement and then repeat that process until you're done. You can then click the "Render" button to generate the frames for each movement. You'll be prompted for a base filename (eg. "myframes.png") and it will then automatically append the padded frame numbers to each one.

You can then use something like ffmpeg to turn that in to a video. Frames are saved as PNG so you can generate videos with alphas in them.

This has been built and tested only on Linux and with GIMP 2.10. You're welcome to try on other versions and platforms but your mileage may vary ;)

We hope you find this at least moderately useful.

Team Arishi

www.arishi.agency
