import random
import string

f = open(r'C:\Users\matan\Desktop\FakeBook\Privacy Policy')
all = f.read()
l = all.split('/%&/%&')
start_lines = l[0].split('$$')

first_lines = l[1].split('$$')
obj_lines = l[2].split('$$')

end_lines = l[3].split('$$')

ends_lines = l[4].split('$$')
patchs = l[5].split('$$')
pat = []


def random_initials(min=3, max=5):
    init = ""
    for _ in xrange(random.randint(min, max)):
        init += unichr(random.randint(65, 90))
    return init


while 1:
    l = raw_input('>>> ')
    if l == '1':
        print '|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
        print start_lines[random.randint(0, len(start_lines) - 1)]
        print first_lines[random.randint(0, len(first_lines) - 1)], obj_lines[random.randint(0, len(obj_lines) - 1)] , end_lines[random.randint(0, len(end_lines) - 1)]

        print ends_lines[random.randint(0, len(ends_lines) - 1)]
    elif l == '2':
        print "\n\n\r PATCH NOTES"
        for i in xrange(random.randint(0,len(patchs)-1)):
            k = patchs[random.randint(0,len(patchs)-1)]
            if k not in pat:
                pat.append(k)
        for i in pat:
            print i
        pat = []
        print "-various bug fixes and improvements"
    elif l == '3':
        print '|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
        print start_lines[random.randint(0, len(start_lines) - 1)]
        print first_lines[random.randint(0, len(first_lines) - 1)], obj_lines[random.randint(0, len(obj_lines) - 1)], \
        end_lines[random.randint(0, len(end_lines) - 1)]

        print ends_lines[random.randint(0, len(ends_lines) - 1)]
        print "\n\n\r PATCH NOTES"
        for i in xrange(random.randint(0, len(patchs) - 1)):
            k = patchs[random.randint(0, len(patchs) - 1)]
            if k not in pat:
                pat.append(k)
        for i in pat:
            print i
        pat = []
        print "-various bug fixes and improvements"

