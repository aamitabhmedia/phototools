def outer():

    def inner():
        print(outervar)
    
    outervar = "Hello World!!"
    inner()

def main():
    outer()

if __name__ == '__main__':
  main()