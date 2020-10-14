# coding:utf-8
#!/user/bin/python3

import os.path
import os
import sys
import shutil

def doc2docx2(docfile):
    cmd = 'libreoffice --headless --convert-to docx '+ docfile
    print(cmd)
# popen返回文件对象，跟open操作一样
    f = os.popen(r""+cmd, "r")
    d = f.read()  # 读文件
    f.close()


def doc2docx(docfile):
    cmd = 'libreoffice --headless --convert-to docx '+ docfile
    print(cmd)
    ret = os.system(r""+cmd)
    if ret == 0:
        print("translate to docx successful!")
    else:
        print("fail to translate!")


def main( argv ):
    if len(argv) < 2:
        print("doc2docx docfilename | doc2docx doc_path")
        return
    if os.path.exists("./docx"):
        print("./docx is exist, please rename to backup!")
        return
    else:
        os.mkdir("./docx")

    fargv = argv[1]
    if os.path.isfile( fargv ):
        if (fargv.find('.doc') > 0 or fargv.find('.DOC') > 0) and ( fargv.find('-EN-') > 0 or fargv.find('-en-') > 0  ) :
            doc2docx2(fargv)
            f_src = "" 
            if fargv.find('.doc') > 0 :
                f_src = fargv+"x"
            elif fargv.find('.DOC') > 0 :
                f_src = fargv + "X"
            f_src = os.path.basename( f_src )
            f_src = f_src.replace(".DOCX", ".docx")
            if os.path.exists(f_src):
                shutil.move(f_src, "./docx/")
                print( f_src + " is successful!")
            else:
                print( f_src + " is not exist!")
        # is file
    elif os.path.isdir(fargv):
        dirs = os.listdir(fargv)
        for farg in dirs:
            if (farg.find('.doc') > 0 or farg.find('.DOC') > 0) and ( farg.find('-EN-') > 0 or farg.find('-en-') > 0  ) :
                fname = os.path.join(fargv, farg)
                doc2docx2( fname )
                f_src = "" 
                if farg.find('.doc') > 0 :
                    f_src = farg+"x"
                elif farg.find('.DOC') > 0 :
                    f_src = farg + "X"
                f_src = os.path.basename( f_src )
                f_src = f_src.replace(".DOCX", ".docx")
                if os.path.exists(f_src): 
                    shutil.move( f_src, "./docx/")
                    print( f_src + " is successful!")
                else:
                    print( f_src+ " is not exist!")
 

###################################  MAIN

if __name__ == "__main__":
    # execute only if run as a script
    main( sys.argv)

