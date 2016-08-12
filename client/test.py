import subprocess
import os
import time

filename = "testtesttest.txt"
subprocess.Popen("python ../server/server.py -s 'filesystem'", shell=True)
time.sleep(5)
subprocess.Popen("python dropbox_clon_main.py -f folder1 -l lida -p 123", shell=True)
time.sleep(5)


def test_add_file(filename):
    file = open("./folder1/" + filename, 'w+')
    time.sleep(5)


def test_delete_file(filename):
    os.system("rm ./folder1/" + filename)
    time.sleep(5)
	
	
def test_add():	
    test_add_file(filename)
    files = os.listdir("../server/folder1")
    assert(files[0] == filename)

	
def test_delete():	
    test_delete_file(filename)
    files = os.listdir("../server/folder1")
    print "test_delete!!!!!!!!!!!", files
    assert(files == [])

	
test_add()
time.sleep(5)
test_delete()

time.sleep(5)

#os.remove("./folder1")

#os.remove("../server/folder1")

#all_files = os.system("ls")

#print all_files