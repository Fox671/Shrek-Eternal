def function(argument1, argument2):
    def subfunction1():
        print(argument1)
    def subfunction2():
        print(argument2)
    subfunction1()
    subfunction2()

function("Hello,", "world!")