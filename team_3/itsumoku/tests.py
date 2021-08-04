from django.test import TestCase
from app.getmov import exec_getmov
# Create your tests here.
def main ():
    movies =exec_getmov()


if __name__=='__main__':
    main()