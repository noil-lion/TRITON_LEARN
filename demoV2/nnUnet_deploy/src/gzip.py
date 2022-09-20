#
list = []
Note=open('y.txt',mode='a')
dir = 'BraTS20_Validation_'
for id in range(1, 126):
    if id < 10:
        num = '00'+str(id)
    if id >= 10 and id < 100:
        num = '0'+str(id)
    if id >=100:
        num = str(id)
    Note.write(dir+num+'/ ')
Note.close()