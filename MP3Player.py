from utime import sleep_ms, sleep
from dfplayermini import DFPlayer
player=DFPlayer(0, 0, 1) #Uart instance, tx pin and rx pi
player.setVolume(30) #Set the volume of the speaker, volume can be between 0-30

player.playTrack(1,2) #Playing track 002.mp3 in folder 01
sleep(10) #Let the track play for 10 seconds

player.nextTrack() #Playing the next track - 003
sleep(10) #Let the track play for 10 seconds

player.prevTrack()
player.prevTrack() #Playing 2 tracks previous - 001
sleep(10) #Let the song play for 10 seconds

player.pause()#Pause the track
sleep(2)
player.resume()#Resume the track
sleep(2)

player.reset() #Reset the MP3 player
