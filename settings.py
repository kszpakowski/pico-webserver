class Settings:
    
    settings_file_name = ""
    
    def __init__(self, settings_file_name):
        self.settings_file_name = settings_file_name
    
    def get_settings(self):
        with open(self.settings_file_name) as f:
            lines = f.readlines()
            settings = {}
            for line in lines:
                k, v = line.strip("\n").split(";")
                settings[k] = v
        return settings
        
    
    def save_settings(self, settings):
        print('saving settings')
        lines = []
        for k, v in settings.items():
            lines.append("%s;%s\n" % (k, v))
        with open(self.settings_file_name, "w") as f:
            f.write(''.join(lines))
        