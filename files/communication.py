import datetime


def analize(data):
    try:
        if (data[0] == 9 and data[1] == 1 and data[2] == 1):
            return_text='Press finger'
            #print('##Press finger')
            return(return_text)
        elif (data[0] == 9 and data[1] == 2 and data[2] == 0):
            return_text = 'Press again'
            #print('##Press again')
            return (return_text)
        elif (data[0] == 9 and data[1] == 3 and data[2] == 0):
            return_text = 'Remove'
            #print('##Remove')
            return (return_text)
        elif (data[0] == 9 and data[1] == 4):
            return_text = f'Enroll succesfull. Id {data[2]} Fill your name and press FINISH'
            #print(f'##Enroll succesfull. Id {data[2]}')
            return (return_text)
        elif (data[0] == 9 and data[1] == 5 and data[2] == 0):
            return_text = 'Fail to capture finger#1'
            #print('##Fail to capture finger#1')
            return (return_text)
        elif (data[0] == 9 and data[1] == 6 and data[2] == 0):
            return_text = 'Fail to capture finger#2'
            #print('##Fail to capture finger#2')
            return (return_text)
        elif (data[0] == 9 and data[1] == 7 and data[2] == 0):
            return_text = 'Fail to capture finger#2'
            #print('##Fail to capture finger#2')
            return (return_text)
        elif (data[0] == 9 and data[1] == 8):
            return_text = f'Error code: {data[2]}'
            #print(f'##Error code: {data[2]}')
            return (return_text)
        else:
            pass
    except:
        pass
