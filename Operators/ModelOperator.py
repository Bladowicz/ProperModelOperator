from BaseOperator import NoConfigException

# def ModelOperatorErrors(fun):
#
#     def wrapper(*args, **kwargs):
#         try:
#             out = fun(*args, **kwargs)
#             return out
#         except NoConfigException:
#             wrapper.called += 1
#             return None
#     wrapper.called = 0
#     wrapper.__name__ = fun.__name__
#     return wrapper


class ModelOperator(object):

    def __init__(self):
        self.operators = []
        self.tempfiles = []

    # @ModelOperatorErrors
    def register(self, operator, *args):
        o = operator(*args)
        if len(self.operators) > 0:
            o.setpredecesor(self.operators[-1])
        self.operators.append(o)

    def verify(self):
        for operator in self.operators:
            operator.verify()

    def run(self):
        for operator in self.operators:
            operator.run()