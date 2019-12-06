#!/usr/bin/env python

import sys
import os
import shutil
import re

dstDir = sys.argv[1]
srcDir = dstDir + ".orig"
if not os.path.exists(srcDir):
  shutil.copytree(dstDir, srcDir)

for curDir, dirs, files in os.walk(srcDir):
  for basename in files:
    srcPath = os.sep.join([curDir, basename])
    dstPath = os.sep.join([dstDir, curDir[len(srcDir):], basename])
    print [srcPath, dstPath]
    if not basename.endswith("toolchain.ninja"):
      shutil.copy2(srcPath, dstPath)
    else:
      srcFD = open(srcPath, "r")
      lines = srcFD.readlines()
      srcFD.close()

      dstFD = open(dstPath, "w")

      currentRule = ""
      llvmDir = ""
      for aLine in lines:
        if aLine.startswith("rule "):
          currentRule = re.split(r'\s', aLine)[1]
          dstFD.write(aLine)

        elif not aLine.startswith(" "):
          currentRule = ""
          dstFD.write(aLine)

        elif aLine.find("command =") > -1:
          directive = re.split("=", aLine, 1)[0]
          toks = re.split(r'\s*=\s*', aLine.rstrip("\r\n"), 1).pop().split(" ")

          quoteMark = ""
          if len(toks[0]) < 2:
            toks[0] = toks[0]
          elif toks[0][0] == '"' and toks[0][-1] == '"':
            quoteMark = '"'
            toks[0] = toks[0][1:-1]
          elif toks[0][0] == "'" and toks[0][-1] == "'":
            quoteMark = "'"
            toks[0] = toks[0][1:-1]
            
          prog = os.path.basename(toks[0])
          progDir = os.path.dirname(toks[0])
          progBase, progExt = os.path.splitext(prog)

          llvmVerStr = progBase.split("-").pop()
          if not re.match(r'^[0-9]+$', llvmVerStr):
            llvmVerStr = ""

          if progExt.lower() == ".exe":
            progPath = os.sep.join([progDir, progBase])
          else:
            progPath = toks[0]

          args = toks[1:]

          print [currentRule, aLine, currentRule, progPath]

          if currentRule == "cc" or currentRule == "cxx":
            llvmDir = progDir
            toks[0] = quoteMark + progPath + quoteMark
            toks.extend(["-Wno-unused-return", "-Wno-shadow-field", "-Wno-extra-semi-stmt"])
            dstFD.write( " ".join([directive, "=", " ".join(toks)]) + "\n")
          elif currentRule == "alink":
            if len(progDir) > 0 and llvmDir.lower().find("llvm") > 0:
              toks[0] = os.sep.join([llvmDir, "llvm-lib"])
            elif len(llvmVerStr) > 0:
              toks[0] = "-".join(["llvm-lib", llvmVerStr])
            else:
              toks[0] = "llvm-lib"
            print [quoteMark, toks[0], quoteMark]
            toks[0] = quoteMark + toks[0] + quoteMark
            dstFD.write( " ".join([directive, "=", " ".join(toks)]) + "\n")
          elif currentRule == "solink" or currentRule == "link":
            if len(progDir) > 0 and llvmDir.lower().find("llvm") > 0:
              toks[0] = os.sep.join([llvmDir, "lld-link"])
            elif len(llvmVerStr) > 0:
              toks[0] = "-".join(["lld-link", llvmVerStr])
            else:
              toks[0] = "llvm-lib"
            # toks[0] = quoteMark + "lld-link" + quoteMark
            dstFD.write( " ".join([directive, "=", " ".join(toks)]) + "\n")
          else:
            dstFD.write(aLine)

        else:
          dstFD.write(aLine)

      dstFD.close()
