class foo:
    def __init__(self, name=None, pk=None, *args, **kwargs):
        self.name = name
        self.pk = pk
        self.args = args
        self.kwargs = kwargs


    def show_all(self):
        print(self.name)
        print(self.pk)
        print(self.args)
        print(self.kwargs)


x1 = foo(pk=1)
x1.show_all()