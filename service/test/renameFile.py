import os




def rename_single(path=r"C:\Users\admin\Desktop\old"):
    i=0
    filelist = os.listdir(path)
    for files in filelist:
        i = i + 1
        Olddir = os.path.join(path, files)
        filename = os.path.splitext(files)[0]
        filetype = os.path.splitext(files)[1]
        # if filename[0]=="c":
        try:
            Newdir = os.path.join(path, "{0}{1}".format("j", str(i)) + filetype)
            print(Newdir)
            os.rename(Olddir, Newdir)
        except:pass



def test(path=r"C:\Users\admin\Desktop\new"):
    i=0
    filelist = os.listdir(path)
    result=set()
    for files in filelist:
        Olddir = os.path.join(path, files)
        filename = os.path.splitext(files)[0][:1]
        filetype = os.path.splitext(files)[1]
        # Newdir = os.path.join(path, "{0}{1}".format("j",str(i)) + filetype)
        # os.rename(Olddir, Newdir)
        result.add(filename)
    return result


def random_remove(path=r"C:\Users\admin\Desktop\old"):
    filelist = os.listdir(path)
    i=0
    for files in filelist:
        Olddir = os.path.join(path, files)
        i+=1
        if i%3!=0:
            os.remove(Olddir)


rename_single()