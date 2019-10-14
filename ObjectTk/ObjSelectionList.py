class AndSelection:
    def __init__(self, option1, option2=None):
        self.result = []
        self.result.append(option1)
        if option2 is not None:
            self.result.append(option2)

    def add_option(self, new_option):
        self.result.append(new_option)

    def get_selection(self):
        return self.result
