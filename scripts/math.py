


def integral(f,a,b):
    s = 1/1000
    r = b-a
    out = 0

    x=0
    while (x < r):
               
        out =+ f(x + s/2)

        x = s + x

    return round(out,3)

def func(x):
    return x*x

print(integral(func,0,2))