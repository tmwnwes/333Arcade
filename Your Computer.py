import platform
machine = platform.machine()
version = platform.version()
release = platform.release()
platformType = platform.platform()
system = platform.system()
processor = platform.processor()

print("You are on a %s machine, running release %s of version %s on the %s platform, using the %s operating system, with a %s processor" %(machine, release, version, platformType, system, processor))