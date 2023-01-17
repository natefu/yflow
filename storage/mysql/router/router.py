class YFlowRouter:

    def db_for_read(self, model, **hints):
        print(model)
        print(hints)
        print('here')
        return 'slave'

    def db_for_write(self, models, **hints):
        print('there')
        return 'default'

    def all_relation(self, obj1, obj2, **hints):
        print('sad')
        return True
