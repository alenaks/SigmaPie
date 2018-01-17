l1 = ["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"]
#l2 = ["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]


def answer(l):
    new = []
    for i in l:
        if i.count(".") == 0:
            new.append([[i],["-1"],["-1"]])
        elif i.count(".") == 1:
            new.append(i.split(".") + ["-1"])
        else:
            new.append(i.split("."))
    print(new)
    return sorted(new, key=lambda x: (x[0], x[1], x[2]))





def answer33(n):
    
    count = 0
    while n >= 1:

        if n == 1: return count
        if n == 2: return count + 1
        if n == 3: return count + 2

        if n % 2 == 0: n = n/2
        elif n % 4 == 1: n = n - 1
        else: n += 1
        
        count += 1






def answer32(M,F):
    
    M,F = int(M), int(F)
    count = 0
    big = max([M,F])

    while True:
        
        if M < 1 or F < 1:
            return "impossible"
        elif big > 1:
            
            if M == big:
                if F != 1:
                    p = M // F
                    M = M - p*F
                else:
                    M = M - F
                    p = 1
            else:
                if M != 1:
                    p = F // M
                    F = F - p*M
                else:
                    F = F - M
                    p = 1
            count += p
            
            big = max([M,F])
        elif M == 1 and F == 1:
            return str(count)
            

##def answer33(n):
##    steps = 0
##    bp = find_power(n)
##    sp = bp - 1
##    bpd = 2**bp - n
##    spd = n - 2**sp
##    if bpd < spd:
##        steps += (bp + bpd)
##    else:
##        steps += (sp + spd)
##    return steps
##
##
##def find_power(n):
##    p = 0
##    while 2**p < n:
##        p += 1
##    return p


##def answer32(M, F):
##    count = 0
##    #M,F = int(M), int(F)
##    big = max([M,F])
##
##    while True:
##        print(M,F)
##        if M < 1 or F < 1:
##            return "impossible"
##        elif big > 1:
##            if M == big:
##                M = M - F
##            else:
##                F = F - M
##            big = max([M,F])
##            count += 1
##        elif M == 1 and F == 1:
##            return str(count)


        
##def answerS(n):
##    n = int(n)
##    return get_count(n,0)
##
##def get_count(n,count):
##    if n == 3:
##        return count+2
##    if n == 2:
##        return count+1
##
##    if n % 2 == 0:
##        return get_count(n/2, count+1)
##    else:
##        if n % 4 == 1:
##            return get_count(n-1, count+1)
##        elif n % 4 == 3:
##            return get_count(n+1, count+1)
