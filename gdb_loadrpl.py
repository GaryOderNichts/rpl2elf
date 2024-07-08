# gdb_loadrpl.py
# Created in 2023 by GaryOderNichts
import gdb
import os
import subprocess
import shutil

class LoadRPL(gdb.Command):
    """Load a RPL/RPX file"""

    tmp_dir = None

    def __init__(self):
        super(LoadRPL, self).__init__("loadrpl", gdb.COMMAND_FILES, gdb.COMPLETE_FILENAME)

        # create temporary directory
        self.tmp_dir = "/tmp/.gdb_loadrpl"

        try:
            os.mkdir(self.tmp_dir)
        except FileExistsError:
            pass

    def invoke(self, arg, from_tty):
        if len(arg) == 0:
            gdb.write("Usage: loadrpl [file]\n")
            return

        # create path for temporary .elf file
        tmp_file = self.tmp_dir + '/' + os.path.basename(arg) + '.elf'

        rpl2elf = shutil.which("rpl2elf")
        if not rpl2elf:
            gdb.write("loadrpl: rpl2elf not found in PATH\n")
            return

        # convert .rpx to .elf
        process = subprocess.run([rpl2elf, arg, tmp_file])
        if process.returncode != 0:
            gdb.write("loadrpl: rpl2elf failed with: " + str(process.returncode) + '\n')
            return

        # load the file
        gdb.execute("file " + tmp_file)
    
LoadRPL()
