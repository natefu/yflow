class Base:

    def to_dict(self):
        return {key[1:]: value for key, value in self.__dict__.items()}
