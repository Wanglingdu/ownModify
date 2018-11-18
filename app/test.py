import os
folder_path = './app/static/upload/report'
# folder_path = 'app/static/upload/report'
local_service = 'http://127.0.0.1:5000/'
lst = os.listdir(folder_path)
name  = []
time  = []
label = []
queue = []

modifylabel = []
for one in lst:
    example_inqueue = []
    example_inqueue.append(one[:-20])
    example_inqueue.append(one[-19:-4])
    # path = local_service + os.path.join(folder_path, one).split('app')[-1]
    # path = local_service+ os.path.join(folder_path, one)

    modifypath = "D:/ForGit/ownModify/app" + os.path.join(folder_path, one).split('app')[-1]
    
    path = local_service + 'app' + os.path.join(folder_path, one).split('app')[-1]
    example_inqueue.append(path)
    example_inqueue.append(modifypath)
    queue.append(example_inqueue)


queue.sort(key=lambda x:x[1], reverse=True)
print(queue)
length = len(queue)
for i in range(length):
    name.append(queue[i][0])
    time.append(queue[i][1])
    label.append(queue[i][2])
    modifylabel.append(queue[i][3])
