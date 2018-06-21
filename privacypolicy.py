import random
import string


f = open(r'C:\Users\matan\OneDrive\מסמכים\fakebook\Privacy Policy')
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


def get_privacy_policy(l):
    str1 = ""
    if l == '1':
        str1 += start_lines[random.randint(0, len(start_lines) - 1)]
        str1 += first_lines[random.randint(0, len(first_lines) - 1)] + obj_lines[random.randint(0, len(obj_lines) - 1)] + end_lines[random.randint(0, len(end_lines) - 1)]

        str1 += ends_lines[random.randint(0, len(ends_lines) - 1)]
    elif l == '2':
        pat = []
        str1 += "\n\n\r PATCH NOTES \n"
        for i in range(random.randint(0,len(patchs)-1)):
            k = patchs[random.randint(0,len(patchs)-1)]
            if k not in pat:
                pat.append(k)
        for i in pat:
            str1 += i
        pat = []
        str1 += "-various bug fixes and improvements"
    elif l == '3':
        str1 += start_lines[random.randint(0, len(start_lines) - 1)]
        str1 += first_lines[random.randint(0, len(first_lines) - 1)] + obj_lines[random.randint(0, len(obj_lines) - 1)] + end_lines[random.randint(0, len(end_lines) - 1)]
        pat = []
        str1 += ends_lines[random.randint(0, len(ends_lines) - 1)]
        str1 += "\n\n\r PATCH NOTES \n"
        for i in range(random.randint(0, len(patchs) - 1)):
            k = patchs[random.randint(0, len(patchs) - 1)]
            if k not in pat:
                pat.append(k)
        for i in pat:
            str1 += i
        pat = []
        str1 += "-various bug fixes and improvements"

    return str1
