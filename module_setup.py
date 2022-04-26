from distutils.core import setup, Extension

def main():
    setup(name="stackmem",
          version="1.0.0",
          description="Python interface for stack memory interfacing",
          author="<your name>",
          author_email="your_email@gmail.com",
          ext_modules=[Extension("stackmem", ["memory_manage.c"])])

if __name__ == "__main__":
    main()