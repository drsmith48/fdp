from ....lib.utilities import isContainer


def postprocess(self, *args, **kwargs):
    print('in postprocess')
    if isContainer(self) and self._name == 'bes' and self.shot < 200000:
        print(type(self))
