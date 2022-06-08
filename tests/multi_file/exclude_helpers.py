import os

# Excludes any file from the testing that does not have the same name as its directory
def exclude_helpers(config):
	for subdir, dirs, files in os.walk(os.path.dirname(__file__)):
		for file in files:
			if os.path.basename(file).endswith(".c") and os.path.basename(file)[:-2] != os.path.basename(subdir):
				config.excludes.add(os.path.basename(file))
