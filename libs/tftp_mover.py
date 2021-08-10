from ftp_mover import FtpMover

mover = FtpMover()
print("connected")
mover.messages()
mover.upload("tst.msg")
print ("uploaded!")
