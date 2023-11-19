from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need help.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

setup(
    name = "AutoRenameMMFC",
    version = "0.1",
    description = "Rename Zips which downloaded on MMFC library.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("auto_rename.py")]
)
